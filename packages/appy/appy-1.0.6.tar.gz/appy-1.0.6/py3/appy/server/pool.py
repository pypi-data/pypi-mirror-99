'''Pool of threads used by the Appy HTTP server'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2021 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from itertools import count
import os, queue, atexit, time, ctypes, threading

from appy.model.utils import Object as O

# Errors - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# THR = thread * WK = worker * SHUTD = shutdown

INITIAL_WK    = 'Initial worker'
ADDED_WK      = 'Worker added in response to lack of idle workers'
WK_KILLED     = 'Worker added for replacing killed thread %s'
WK_REPLACED   = 'Voluntary replacement for thread %s'
WORK_DONE     = ' > handled by thread %s (%i tasks queued).'
CHECK_ADD_THR = 'No idle workers for task; checking if we need to make ' \
                'more workers'
SPAWNING      = 'No idle tasks and only %d busy task(s): adding %d more workers'
NO_SPAWNING   = 'No extra workers needed (%d busy worker(s))'
CULL_WORKERS  = 'Culling %s extra workers. %s idle workers present: %s'
CULL_KILLED   = 'Killed thread %s no longer around'
KILL_KO       = 'PyThreadState_SetAsyncExc failed'
KILLING_THR   = 'Killing thread with ID=%s...'
KILLED_HUNGED = 'Workers killed forcefully'
WK_TO_KILL    = 'Killing thread "%s"... (working on task for %i seconds)'
HUNG_STATUS   = "killHungThreads status: %d threads (%d working, %d idle, " \
                "%d starting), average time %s, maxTime %.2fsec, killed %d " \
                "worker(s)."
ZOMBIES_FOUND = 'Zombie thread(s) found: %s.'
EXITING       = 'Exiting process because %s zombie threads is more than %s limit.'
NEW_WORKER    = 'Started new worker %s: %s'
STOPPING_THR  = 'Thread %s processed %i requests (limit %s); stopping it'
SHUTD_RECV    = 'Worker %s is asked to shutdown'
SHUTD_POOL    = 'Shutting down the threadpool (%d threads)'
SHUTD_HUNG    = "%s worker(s) didn't stop properly, and %s zombie(s)"
SHUTD_OK      = 'All workers stopped'
SHUTD_FORCED  = 'Forcefully exiting process'
SHUTD_F_OK    = 'All workers eventually killed'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class ThreadPool:
    '''Pool of threads for efficiently managing incoming client requests'''

    # This excellent code was initially copied from the Paste project, many many
    # thanks. https://github.com/cdent/paste/blob/master/paste/httpserver.py

    # This pool manages a list of thread workers managing cliet requests via a
    # queue of callables.

    # The pool keeps a notion of the status of its worker threads.
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # If...  | The worker thread ...
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # idle   | does nothing
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # busy   | is doing its job
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # hung   | has been doing a job for too long
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # dying  | is a hung thread that has been killed, but hasn't died quite yet
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # zombie | that we've tried to kill but isn't dead yet
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # The pool also maintains, in attribute "tracked", a dictionary with these
    # keys and lists of thread IDs that fall in that status. All keys will be
    # present, even if they point to emty lists.

    # Hung threads are threads that have been busy more than
    # config.hungThreadLimit seconds. Hung threads are killed when they live
    # longer than config.killThreadLimit seconds. A thread is then considered
    # dying for config.dyingLimit seconds, if it is still alive after that it is
    # considered a zombie.

    # When there are no idle workers and a request comes in, another worker
    # *may* be spawned. If there are less than config.spawnIfUnder threads in
    # the busy state, another thread will be spawned.  So if the limit is 5, and
    # there are 4 hung threads and 6 busy threads, no thread will be spawned.

    # When there are more than config.maxZombieThreadsBeforeDie zombie threads,
    # a SystemExit exception will be raised, stopping the server. Use 0 or None
    # to never raise this exception. Zombie threads *should* get cleaned up, but
    # killing threads is no necessarily reliable. This is turned off by default,
    # since it is only a good idea if you've deployed the server with some
    # process watching from above (something similar to daemontools or zdaemon).

    # Each worker thread only processes config.maxRequests tasks before it dies
    # and replaces itself with a new worker thread.

    SHUTDOWN = object()

    # This flag specifies if, when the server terminates, all in-progress client
    # connections should be droppped.
    daemon = False

    def __init__(self, server, config):
        '''Initialise the pool's data stuctures'''
        # A reference to the p_server
        self.server = server
        self.logger = server.loggers.app
        # The server config
        self.config = config
        # The Queue object allowing inter-thread communication
        self.queue = queue.Queue()
        # The list of Thread instances
        self.workers = []
        self.workersCount = count()
        # Dict storing info about thread's statuses
        self.tracked = {} # ~{i_threadId: (i_timeStarted, info)}~
        # IDs of threads being idle
        self.idleWorkers = []
        # Dict of threads having been killed, but maybe aren't dead yet
        self.dyingThreads = {} # ~{i_threadId: (i_time, Thread)}~
        # This is used to track when we last had to add idle workers
        # (storing time.time()); we shouldn't cull extra workers until some time
        # has passed (config.hungThreadLimit) since workers were added.
        self.lastAddedNewIdleWorkers = 0
        # Number of requests received since last check for hunged threads
        self.requestsSinceLastHungCheck = 0
        if not ThreadPool.daemon:
            atexit.register(self.shutdown)
        # Create the threads
        for i in range(config.threads):
            self.addWorker(message=INITIAL_WK)

    def debug(self, message):
        '''Logs a message'''
        self.logger.debug(message)

    def addTask(self, task):
        '''Adds a task to the queue'''
        # Kill hung threads if it's time to do it
        cfg = self.config
        if cfg.hungCheckPeriod:
            self.requestsSinceLastHungCheck += 1
            if self.requestsSinceLastHungCheck > cfg.hungCheckPeriod:
                self.requestsSinceLastHungCheck = 0
                self.killHungThreads()
        # Add workers when relevant
        if not self.idleWorkers and cfg.spawnIfUnder:
            # spawnIfUnder can come into effect. Count busy threads.
            busy = 0
            now = time.time()
            self.debug(CHECK_ADD_THR)
            for worker in self.workers:
                # Ignore uninitialized threads
                if not hasattr(worker, 'thread_id'): continue
                started, info = self.tracked.get(worker.thread_id, (None,None))
                if started is not None:
                    if (now - started) < cfg.hungThreadLimit:
                        busy += 1
            if cfg.spawnIfUnder > busy:
                delta = cfg.spawnIfUnder - busy
                self.debug(SPAWNING % (busy, delta))
                self.lastAddedNewIdleWorkers = time.time()
                for i in range(delta):
                    self.addWorker(message=ADDED_WK)
            else:
                self.debug(NO_SPAWNING % busy)
        # Kill supernumerary workers when relevant
        idle = len(self.idleWorkers)
        if (len(self.workers) > cfg.threads) and (idle > 3) and \
           ((time.time()-self.lastAddedNewIdleWorkers) > cfg.hungThreadLimit):
            # We've spawned workers in the past, but they aren't needed anymore;
            # kill off some.
            kill = len(self.workers) - cfg.threads
            self.debug(CULL_WORKERS % (kill, idle, self.idleWorkers))
            for i in range(kill):
                self.queue.put(self.SHUTDOWN)
        # Add the task to the queue
        self.queue.put(task)

    def cullThreadIfDead(self, id):
        '''Cull thread with this p_id if it does not exist anymore. Return True
           if the thread has been culled.'''
        if self.threadExists(id): return
        self.debug(CULL_KILLED % id)
        try:
            del self.dyingThreads[id]
            return True
        except KeyError:
            pass

    def getTracked(self, formatted=True):
        '''Returns a dict summarizing info about the threads in the pool'''
        r = O(idle=[], busy=[], hung=[], dying=[], zombie=[])
        now = time.time()
        cfg = self.config
        for worker in self.workers:
            # Ignore threads not being fully started up
            if not hasattr(worker, 'thread_id'): continue
            started, info = self.tracked.get(worker.thread_id, (None, None))
            if started is not None:
                attr = 'hung' if (now-started) > cfg.hungThreadLimit else 'busy'
            else:
                attr = 'idle'
            getattr(r, attr).append(worker)
        # Add dying and zombies
        for id, (killed, worker) in self.dyingThreads.items():
            culled = self.cullThreadIfDead(id)
            if culled: continue
            attr = 'zombie' if now - killed > cfg.dyingLimit else 'dying'
            getattr(r, attr).append(worker)
        if formatted:
            # Return it as a XHTML table
            rows = []
            for name, threads in r.items():
                info = []
                for thread in threads:
                    info.append('%s - %s' % (thread.getName(), thread.ident))
                rows.append('<tr><th>%s</th><td>%s</td></tr>' % \
                            (name, '<br/>'.join(info)))
            r = '<table class="small"><tr><th>Type</th><th>Threads</th></tr>' \
                '%s</table>' % '\n'.join(rows)
        return r

    def killWorker(self, id):
        '''Removes from the pool, the worker whose thread ID is p_id and
           replaces it with a new worker thread.'''
        # This should only be done for mis-behaving workers
        thread = threading._active.get(id)
        # Kill the thread by raising SystemExit
        tid = ctypes.c_long(id)
        r = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
              ctypes.py_object(SystemExit))
        if r == 0:
            pass # Invalid thread id: it has died in the mean time
        elif r != 1:
            # If it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError(KILL_KO)
        # Remove any reference to the thread in the pool
        try:
            del self.tracked[id]
        except KeyError:
            pass
        self.debug(KILLING_THR % id)
        if thread in self.workers:
            self.workers.remove(thread)
        self.dyingThreads[id] = (time.time(), thread)
        self.addWorker(message=WK_KILLED % id)

    def addWorker(self, *args, **kwargs):
        index = next(self.workersCount)
        worker = threading.Thread(target=self.workerMethod, args=args,
                                  kwargs=kwargs, name=("worker %d" % index))
        worker.setDaemon(ThreadPool.daemon)
        worker.start()

    def threadExists(self, id):
        '''Returns True if a thread with this p_id exists'''
        return id in threading._active

    def killHungThreads(self):
        '''Tries to kill any hung thread'''
        cfg = self.config
        # No killing should occur in that case
        if not cfg.killThreadLimit: return
        now = time.time()
        maxTime = totalTime = idle = starting = working = killed = 0
        for worker in self.workers:
            # Ignore uninitialized threads
            if not hasattr(worker, 'thread_id'):
                starting += 1
                continue
            id = worker.thread_id
            started, info = self.tracked.get(id, (None, None))
            if started is None:
                # Must be idle
                idle += 1
                continue
            lifetime = now - started
            working += 1
            maxTime = max(maxTime, lifetime)
            totalTime += lifetime
            if lifetime > cfg.killThreadLimit:
                self.logger.warn(WK_TO_KILL % (worker.getName(), lifetime))
                self.killWorker(id)
                killed += 1
        average = '%.2fsec' % (totalTime / working) if working else 'N/A'
        self.debug(HUNG_STATUS % ((idle + starting + working), working, idle, \
                                  starting, average, maxTime, killed))
        self.checkMaxZombies()

    def checkMaxZombies(self):
        '''Checks if we've reached cfg.maxZombieThreadsBeforeDie; if so, kill
           the entire process.'''
        cfg = self.config
        if not cfg.maxZombieThreadsBeforeDie: return
        found = []
        now = time.time()
        for id, (killed, worker) in self.dyingThreads.items():
            culled = self.cullThreadIfDead(id)
            if culled: continue
            if (now - killed) > cfg.dyingLimit:
                found.append(id)
        if found:
            self.debug(ZOMBIES_FOUND % ', '.join(found))
        count = len(found)
        if count > cfg.maxZombieThreadsBeforeDie:
            self.logger.error(EXITING % (count, cfg.maxZombieThreadsBeforeDie))
            self.shutdown(10)
            raise SystemExit(3)

    def workerMethod(self, message=None):
        '''Method executed by a worker thread'''
        cfg = self.config
        thread = threading.currentThread()
        id = thread.thread_id = threading.get_ident()
        self.workers.append(thread)
        self.idleWorkers.append(id)
        processed = 0 # The number of processed requests
        replace = False # Must we replace the thread ?
        self.debug(NEW_WORKER % (id, message))
        try:
            while True:
                # Stop myself if I have managed the maximum number of requests
                max = cfg.maxRequests
                if max and (processed > max):
                    # Replace me then die
                    self.debug(STOPPING_THR % (id, processed, max))
                    replace = True
                    break
                # Get the job I have to do
                runnable = self.queue.get()
                if runnable is ThreadPool.SHUTDOWN:
                    # This is not a job, but a shutdown command
                    self.debug(SHUTD_RECV % id)
                    break
                # Note myself as working
                try:
                    self.idleWorkers.remove(id)
                except ValueError:
                    pass
                self.tracked[id] = [time.time(), None]
                processed += 1
                # Perform my task
                runnable()
                self.debug(WORK_DONE % (id, self.queue.qsize()))
                # Note myself again as being "idle"
                try:
                    del(self.tracked[id])
                except KeyError:
                    pass
                self.idleWorkers.append(id)
        finally:
            try:
                del(self.tracked[id])
            except KeyError:
                pass
            try:
                self.idleWorkers.remove(id)
            except ValueError:
                pass
            try:
                self.workers.remove(thread)
            except ValueError:
                pass
            try:
                del(self.dyingThreads[id])
            except KeyError:
                pass
            if replace:
                self.addWorker(message=WK_REPLACED % id)

    def shutdown(self, forceQuitTimeout=0):
        '''Shutdown the queue (after finishing any pending requests)'''
        count = len(self.workers)
        self.debug(SHUTD_POOL % count)
        # Add a shutdown request for every worker
        for i in range(count):
            self.queue.put(ThreadPool.SHUTDOWN)
        # Wait for each thread to terminate
        hung = []
        for worker in self.workers:
            worker.join(0.5)
            if worker.is_alive():
                hung.append(worker)
        zombies = []
        for id in self.dyingThreads:
            if self.threadExists(id):
                zombies.append(id)
        if hung or zombies:
            self.debug(SHUTD_HUNG % (len(hung), len(zombies)))
            if hung:
                for worker in hung:
                    self.killWorker(worker.thread_id)
                self.debug(KILLED_HUNGED)
            if forceQuitTimeout:
                timedOut = False
                needForceQuit = bool(zombies)
                for worker in self.workers:
                    if not timedOut and worker.is_alive():
                        timedOut = True
                        worker.join(forceQuitTimeout)
                    if worker.is_alive():
                        # Worker won't die
                        needForceQuit = True
                if needForceQuit:
                    # Remove the threading atexit callback
                    for callback in list(atexit._exithandlers):
                        func = getattr(callback[0], 'im_func', None)
                        if not func:
                            continue
                        globs = getattr(func, 'func_globals', {})
                        mod = globs.get('__name__')
                        if mod == 'threading':
                            atexit._exithandlers.remove(callback)
                    atexit._run_exitfuncs()
                    self.debug(SHUTD_FORCED)
                    os._exit(3)
                else:
                    self.debug(SHUTD_F_OK)
        else:
            self.debug(SHUTD_OK)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
