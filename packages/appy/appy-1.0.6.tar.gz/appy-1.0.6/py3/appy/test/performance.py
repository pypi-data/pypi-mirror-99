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
import os, sys, re, urllib.parse, logging, time, random
from appy.utils.client import Resource

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Configuration options for executing performance tests on a Appy server'''
    LOG_TARGET_ERROR = 'If multiple clients are executed, stdout cannot be ' \
      'used as log target. Specify the name of a file to log to.'

    def __init__(self, url, login, password,
                 scenario=[], clients=1, logTarget='stdout', silent=False,
                 alternateUrls=[]):
        # The Appy server URL(s) (including port)
        self.urls = [url]
        # The credentials used to authenticate to this server
        self.login = login
        self.password = password
        # The scenario to apply. Every entry can be a (relative) URL (starting
        # with a "/", the root of the site being "/") as a string or a Hit
        # instance (see below).
        self.scenario = scenario
        # The number of processes to fork for simulating simultaneous users.
        # Every client will execute the same scenario as defined above.
        self.clients = clients
        # Where to log test output. Can be 'stdout' or the name of a file. When
        # clients is > 1, output can't be 'stdout': it must be a thread-safe
        # file (that we manage via the standard logging module).
        self.logTarget = logTarget
        # If "silent" is True, a single log entry will be dumped by the script,
        # allowing for minimalistic log when multiple processes are run.
        self.silent = silent
        # You can specify a list of alternate URLs allowing to hit the same
        # resource as the one specified by p_url. In that case, every client
        # will choose one URL among [p_url] + alternateUrls for contacting the
        # server.
        if alternateUrls:
            self.urls += alternateUrls

    def check(self):
        '''Returns an error message if this config is not correct'''
        # stdout cannot be used when multiple clients are run
        if (self.clients > 1) and self.logTarget == 'stdout':
            return self.LOG_TARGET_ERROR

    def getUrl(self, i=0):
        '''Get the server URL to be used by the p_ith client'''
        urlsCount = len(self.urls)
        # If there is a single URL, return it
        if urlsCount == 1: return self.urls[0]
        # Compute the index, within self.urls, of the URL to return
        if i >= urlsCount:
            j = i
            while j >= urlsCount:
                j -= urlsCount
        else:
            j = i
        return self.urls[j]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Hit:
    '''Represents a HTTP request on the server.
       If your scenario simply consists in a series of HTTP GET requests on the
       server, you do not need to use a Hit instance: simply define URLs as
       strings within Config.scenario. When things get more complex, use a Hit
       instance:
        * if you need to define a POST request;
        * if you need to define a URL by parsing the last (or a previous)
          request and finding your URL among it.
    '''
    # Regular expression for retrieving all "A" tags in a web page
    aRex = re.compile(b'<a\s+.*?href="(.*?)".*?>(.*?)</a>', re.S)

    def __init__(self, url, indexes=None, method='GET', comment=None,
                 id=None, baseHit=None):
        # The URL to hit on the tested server. If p_indexes is not None, this
        # URL is a regular expression that wil be applied to all "A" tags from
        # the last server response, to retrieve the URL to hit. Among all URLs
        # matching the regular expressions, those found at p_indexes will be
        # chosen.
        self.url = url
        self.indexes = indexes
        # GET or POST
        self.method = method
        # Some comment about this hit, that will be shown in the test report
        self.comment = comment
        # An identifier for this hit. This way, another hit will be able to
        # refer to this one
        self.id = id
        # The ID of the hit from which the URL for this one will be found. If
        # None, it means that the previous hit will be the base hit.
        self.baseHit = baseHit

    def cleanUrl(self, url):
        '''Removes any non-significative part in p_url'''
        parts = urllib.parse.urlparse(url)
        r = parts.path or '/'
        if parts.query:
            r += '?%s' % parts.query
        return r

    def sendOne(self, url, tester, comment='...', id=None):
        '''Called by m_send below to send a single request to the server. If an
           p_id(entifier) is given, it will be used to store the list of URLs
           found in the response body in tester.responseUrls. Returns a tuple
           (success, response).'''
        log = tester.log
        url = self.cleanUrl(url.decode())
        log('%s >> %s' % (url, comment))
        response = tester.server.get(url)
        log(response, 2)
        tester.countTime(response)
        if response.code != 200:
            log(' Error %d received.' % response.code)
            return False, response
        elif id:
            tester.responseUrls[id] = self.aRex.findall(response.body)
        return True, response

    def send(self, tester, previous):
        '''Send the request(s) corresponding to this hit to the tested server
           and returns a tuple (success, response) containing the result of
           executing the last request.'''
        log = tester.log
        if self.indexes:
            # Retrieve the URLs to get from the previous hit or a base hit
            if self.baseHit:
                if self.baseHit not in tester.responseUrls:
                    log('Hit "%s" was not found.' % self.baseHit, 2)
                    return False, None
                # Get the list of URLs retrieved by the base hit
                urls = tester.responseUrls[self.baseHit]
            else:
                # Get all "A" tags within previous body
                urls = self.aRex.findall(previous.body)
                if not urls:
                    log('No URL found in previous request.', 2)
                    return False, None
            # Apply regular expression "self.url" to match any URL from "urls"
            matched = []
            pattern = self.url
            for url, title in urls:
                if re.search(pattern, url):
                    matched.append((url, title))
            if not matched:
                log('Pattern "%s" not found among base hit.' % pattern, 2)
                return False, None
            # Get the URLs whose indexes are in self.indexes
            for i in self.indexes:
                # Check if this index is valid
                if i >= len(matched):
                    log('Wrong index %d (only %d URL(s) matched)' %
                        (i, len(matched)), 2)
                    return False, None
                # Build an ID corresponding to this index if this hit is
                # identified.
                id = '%s_%d' % (self.id, i) if self.id else None
                url, comment = matched[i]
                comment = comment.decode()
                success, response = self.sendOne(url, tester, comment, id)
                if not success: return False, None
            return True, response
        else:
            url = self.url
            comment = self.comment or '...'
            return self.sendOne(url, tester, comment, self.id)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Tester:
    '''Allows to execute performance tests on a Appy server by sending him a
       sequence of HTTP requests.'''

    def __init__(self, config):
        self.config = config
        self.server = None # Will be instantiated by m_runOne
        # The total time we have waited for server responses (seconds)
        self.duration = 0.0
        # Remember the list of URLs retrieved by every (identified) hit
        self.responseUrls = {} # ~{s_hitId: [(s_url, s_title)]}~
        if config.logTarget != 'stdout':
            logging.basicConfig(filename=config.logTarget, level=logging.DEBUG,
                                format='%(asctime)s: %(message)s')
        # These booleans indicate when to log to stdout and/or to the log file
        self.mustPrint = config.clients == 1
        self.mustLog = config.logTarget != 'stdout'

    def log(self, msg, blanks=0, level='info', force=False):
        '''Outputs on stdout and/or in a log file. p_blanks is the number of
           blanks that must be dumped at the start of the log entry.'''
        # Do not dump anything in silent mode, excepted if forced
        if self.config.silent and not force: return
        # Create the message to log and/or print
        msg = '%s%s' % (' '*blanks, msg)
        if self.config.clients > 1:
            msg = 'pid %d: %s' % (os.getpid(), msg)
        if self.mustPrint:
            print(msg)
        if self.mustLog:
            getattr(logging, level)(msg)

    def countTime(self, response):
        '''Count the time spent waiting for the server p_response'''
        self.duration += response.duration

    def sleep(self):
        '''Sleeps for a while. It is used at some early places in the scenario,
           to avoid processes to hit the server exactly at the same time.'''
        duration = random.random()
        time.sleep(duration)

    def authenticate(self):
        '''Logs into the p_server and returns a tuple (success, response):
           * "success"  is a boolean being True on sucessfull authentication;
           * "response" is the last HTTP response received by the server.
        '''
        server = self.server
        config = self.config
        log = self.log
        # Get the home page (so we know if the site is alive)
        self.sleep()
        log('*** Contacting %s as user "%s"...' % (server.url, config.login))
        log("/ >> site's home page... ")
        try:
            response = server.get()
            self.countTime(response)
        except Resource.Error as err:
            log('%s is unreachable (%s).' % (server.url, str(err)), 2)
            return False, None
        if response.code != 200:
            log('%s: got error %s.' % (server.url, response.code), 2)
            return False, None
        log(response, 2)
        # Define the parameters for the login
        data = {'js_enabled': 0, 'cookies_enabled': '', 'login_name': '',
                'pwd_empty': 0, '__ac_name': config.login,
                '__ac_password': config.password, 'submit': 'Connect'}
        logUrl = '/config/performLogin'
        log("%s >> logging in... " % logUrl)
        self.sleep()
        response = server.post(data, uri=logUrl)
        success = '_appy_' in server.cookies
        msg = '%s authenticated.' % config.login \
              if success else 'authentication failed.'
        log(response, 2)
        log(msg, 2)
        self.countTime(response)
        return success, response

    def runOne(self, i=0):
        '''Executes the test scenario once'''
        self.server = Resource(self.config.getUrl(i), measure=True, timeout=600)
        log = self.log
        config = self.config
        success, response = self.authenticate()
        if not success:
            log('*** Test aborted.')
            self.exit()
        # Apply the test scenario
        for hit in self.config.scenario:
            # Convert the hit to a Hit instance when relevant
            if isinstance(hit, str): hit = Hit(hit)
            success, response = hit.send(self, previous=response)
            if not success:
                self.terminate()
                log('*** Test aborted.')
                self.exit()
        self.terminate()
        log('*** Test successfully terminated.')
        log('%f second(s) waiting server responses.' % self.duration, 2,
            force=True)
        self.exit()

    def run(self):
        '''Executes the test scenario, potentially forking several child
           processes that will all execute the same scenario.'''
        config = self.config
        clients = config.clients
        if clients == 1:
            self.runOne()
        else:
            # Fork as many processes as required
            i = 0
            print('Forking %d processes...' % clients)
            while i < clients:
                pid = os.fork()
                if pid == 0:
                    # We are in the child: execute the scenario
                    self.runOne(i)
                else:
                    # We are in the parent
                    print('Child %d forked.' % pid)
                # m_runOne will exit. So here we are in the parent process.
                # Continue the loop.
                i += 1
            print('Check log in %s.' % config.logTarget)

    def terminate(self):
        '''Terminates the test by logging out of the tested server'''
        logoutUrl = '/config/performLogout'
        self.log("%s >> logging out... " % logoutUrl)
        self.server.get(logoutUrl)

    def exit(self):
        '''Exists the program'''
        return sys.exit(0)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
