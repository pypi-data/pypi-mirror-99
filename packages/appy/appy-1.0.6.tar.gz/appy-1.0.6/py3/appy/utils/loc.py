'''Counting Lines Of Code (LOC)'''

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
from pathlib import Path

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class LanguageCounter:
    '''Counts lines of code for files written in a given language'''

    def __init__(self, name, spaces):
        # The name of the language
        self.name = name
        # The total number of analysed files
        self.numberOfFiles = 0
        # The number of empty lines within those files
        self.emptyLines = 0
        # The number of comment lines
        self.commentLines = 0
        # A code line is anything not being an empty or comment line
        self.codeLines = 0
        # The spaces to dump before printing anything to stdout
        self.spaces = spaces

    def numberOfLines(self):
        '''Computes the total number of lines within analysed files.'''
        return self.emptyLines + self.commentLines + self.codeLines

    def countAny(self, f, start, end, single=None):
        '''Analyses file p_f. p_start and p_end are delimiters for multi-line
           comments, while p_single is the symbol representing a single-line
           comment.'''
        inDoc = False
        firstDoc = False
        for line in f:
            stripped = line.strip()
            # Manage a single-line comment
            if not inDoc and single and line.startswith(single):
                self.commentLines += 1
                continue
            # Manage a comment
            if not inDoc and (start in line):
                if line.startswith(start):
                    self.commentLines += 1
                else:
                    self.codeLines += 1
                inDoc = True
                firstDoc = True
            if inDoc:
                if not firstDoc:
                    self.commentLines += 1
                if end in line:
                    inDoc = False
                firstDoc = False
                continue
            # Manage an empty line
            if not stripped:
                self.emptyLines += 1
            else:
                self.codeLines += 1

    def countJs(self, f): return self.countAny(f, '/*', '*/', single='//')
    countCss = countJs

    def countXml(self, f): return self.countAny(f, '<!--', '-->')

    # Doc separators in the Python language
    pythonDocSeps = ('"""', "'''")

    def isPythonDoc(self, line, start, isStart=False):
        '''Returns True if we find, in p_line, the start of a docstring (if
           p_start is True) or the end of a docstring (if p_start is False).
           p_isStart indicates if p_line is the start of the docstring.'''
        seps = LanguageCounter.pythonDocSeps
        if start:
            r = line.startswith(seps[0]) or line.startswith(seps[1])
        else:
            sepOnly = (line == seps[0]) or (line == seps[1])
            if sepOnly:
                # If the line contains the separator only, is this the start or
                # the end of the docstring ?
                r = not isStart
            else:
                r = line.endswith(seps[0]) or line.endswith(seps[1])
        return r

    def countPy(self, f):
        '''Analyses the Python file p_f'''
        # Are we in a docstring ?
        inDoc = False
        try:
            for line in f:
                stripped = line.strip()
                # Manage a line that is within a docstring
                inDocStart = False
                if not inDoc and self.isPythonDoc(stripped, start=True):
                    inDoc = True
                    inDocStart = True
                if inDoc:
                    self.commentLines += 1
                    if self.isPythonDoc(stripped, start=False, isStart=inDocStart):
                        inDoc = False
                    continue
                # Manage an empty line
                if not stripped:
                    self.emptyLines += 1
                    continue
                # Manage a comment line
                if line.startswith('#'):
                    self.commentLines += 1
                    continue
                # If we are here, we have a code line
                self.codeLines += 1
        except UnicodeDecodeError:
            print(self.spaces, '%s could not be read (unicode error).' % f.name)

    def countFile(self, path):
        '''Analyses file named p_path'''
        with path.open() as f:
            # Choose the method corresponding to the file extension
            method = 'count%s' % (path.suffix[1:].capitalize())
            getattr(self, method)(f)
        self.numberOfFiles += 1

    def printReport(self):
        '''Returns the analysis report as a string, only if there is at least
           one analysed line.'''
        lines = self.numberOfLines()
        if not lines: return
        commentRate = (self.commentLines / float(lines)) * 100.0
        blankRate = (self.emptyLines / float(lines)) * 100.0
        print(self.spaces,
              '%s: %d files, %d lines (%.0f%% comments, %.0f%% blank)' % \
              (self.name, self.numberOfFiles, lines, commentRate, blankRate))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Counter:
    '''Counts and classifies the lines of code within a folder hierarchy'''

    # Paths containing these chunks will be excluded from the analysis
    defaultExclude = ('/.svn/', '/tmp/', '/temp/', '/jscalendar/', '/doc/')

    # Files corresponding to these languages will be part of the analysis
    languages = {'py': 'Python', 'xml': 'XML', 'css': 'CSS', 'js': 'Javascript'}

    def __init__(self, folder, exclude=None, spaces=''):
        # The spaces to dump before printing anything to stdout
        self.spaces = spaces
        # The base folder into which lines of code will be counted
        self.folder = Path(folder) if isinstance(folder, str) else folder
        # Collect here info about the analysed files ~{s_ext: LanguageCounter}~
        self.counters = { ext: LanguageCounter(name, spaces) \
                          for ext, name in Counter.languages.items()}
        # Which paths to exclude from the analysis ?
        self.exclude = list(Counter.defaultExclude)
        if exclude: self.exclude += exclude

    def printReport(self):
        '''Displays on stdout a small analysis report about self.folder'''
        total = 0
        for ext, counter in self.counters.items():
            if counter.numberOfFiles:
                counter.printReport()
                total += counter.numberOfLines()
        print(self.spaces, 'Total (including commented and blank): ***',
              total, '***')

    def mustExclude(self, path):
        '''Must p_path be excluded from the analysis ?'''
        for excl in self.exclude:
            if excl in path.as_posix(): return True

    def run(self):
        '''Start the count'''
        # Launch one analysis per language
        for ext, counter in self.counters.items():
            # Browse all files of this type in p_self.folder
            for path in self.folder.glob('**/*.%s' % ext):
                # Ignore paths to exclude
                if self.mustExclude(path): continue
                # Analyse the file in "path"
                self.counters[ext].countFile(path)
        self.printReport()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
