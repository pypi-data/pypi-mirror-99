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
import os, re, io, time, copy, collections, pathlib
from appy.model.utils import Object as O
from appy.utils.string import produceNiceMessage

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
poHeaders = '''msgid ""
msgstr ""
"Project-Id-Version: Appy-%s\\n"
"POT-Creation-Date: %s\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=1; plural=0\\n"
"Language-code: %s\\n"
"Language-name: %s\\n"
"Preferred-encodings: utf-8 latin1\\n"
"Domain: %s\\n"
%s

'''
fallbacks = {'en': 'en-us en-ca',
             'fr': 'fr-be fr-ca fr-lu fr-mc fr-ch fr-fr'}

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Message:
    '''Represents a i18n message (po format)'''
    def __init__(self, id, msg, default, fuzzy=False, comments=[],
                 niceDefault=False):
        self.id = id
        self.msg = msg
        self.default = default
        if niceDefault: self.produceNiceDefault()
        # True if the default value has changed in the pot file: the msg in the
        # po file needs to be translated again.
        self.fuzzy = fuzzy 
        self.comments = comments

    def update(self, newMsg, isPot, language):
        '''Updates me with new values from p_newMsg. If p_isPot is True (which
           means that the current file is a pot file), I do not care about
           filling self.msg.'''
        if isPot:
            self.msg = ""
            if not self.default:
                self.default = newMsg.default
                # It means that if the default message has changed, we will not
                # update it in the pot file. We will always keep the one that
                # the user may have changed in the pot file. We will write a
                # default message only when no default message is defined.
        else:
            # newMsg comes from a pot file or from a base po file (like a
            # standard Appy po file). We must update the corresponding
            # message in the current po file.
            oldDefault = self.default
            if self.default != newMsg.default:
                # The default value has changed in the pot file
                oldDefault = self.default or ''
                self.default = newMsg.default
                self.fuzzy = False
                if self.msg.strip():
                    self.fuzzy = True
                    # We mark the message as "fuzzy" (=may need to be rewritten
                    # because the default value has changed) only if the user
                    # has already entered a message. Else, this has no sense to
                    # rewrite the empty message.
                    if not oldDefault.strip():
                        # This is a strange case: the old default value did not
                        # exist. Maybe was this PO file generated from some
                        # tool, but simply without any default value. So in
                        # this case, we do not consider the label as fuzzy.
                        self.fuzzy = False
            # If p_newMsg contains a message, and no message is defined for
            # self, copy it.
            if newMsg.msg and not self.msg:
                self.msg = newMsg.msg
            # For english, the the default value from a pot file can be used as
            # value for the po file.
            if (language == 'en'):
                if not self.msg:
                    # Put the default message into msg for english
                    self.msg = self.default
                if self.fuzzy and (self.msg == oldDefault):
                    # The message was equal to the old default value. It means
                    # that the user did not change it, because for English we
                    # fill by default the message with the default value (see
                    # code just above). So in this case, the message was not
                    # really fuzzy.
                    self.fuzzy = False
                    self.msg = self.default

    def produceNiceDefault(self):
        '''Transforms self.default into a nice msg'''
        self.default = produceNiceMessage(self.default)

    def generate(self):
        '''Produces myself as I must appear in a po(t) file'''
        res = ''
        for comment in self.comments:
            res += comment + '\n'
        if self.default is not None:
            res = '#. Default: "%s"\n' % self.default
        if self.fuzzy:
            res += '#, fuzzy\n'
        res += 'msgid "%s"\n' % self.id
        res += 'msgstr "%s"\n' % self.msg
        return res

    def __repr__(self):
        return '<i18n msg id="%s", msg="%s", default="%s">' % \
               (self.id, self.msg, self.default)

    def get(self):
        '''Returns self.msg, but with some replacements'''
        # Basically, the main Appy interface is the web UI. So, when formatting
        # needs to be integrated into messages as written in "po" files, we
        # expect them to be expressed in XHTML. With one exception: carriage
        # returns. Appy, for the sake of conciseness, tolerates the presence of
        # "\n" and will replace them with an XHTML carriage return "<br/>".
        # Moreover, because double quotes escaping is required due to the format
        # of "po" files, we perform such escaping too.
        return self.msg.replace('\\n', '<br/>').replace('\\"', '"')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Header:
    '''A header within a po file'''
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def generate(self):
        '''Generates the representation of myself into a po(t) file'''
        return '"%s: %s\\n"\n' % (self.name, self.value)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class File:
    '''Represents a i18n "po" file'''
    def __init__(self, path, messages=None):
        self.path = path
        self.isPot = path.suffix == '.pot'
        # Messages, ordered and keyed by their ID
        self.messages = messages or collections.OrderedDict()
        # Headers, ordered and keyed by their ID
        self.headers = collections.OrderedDict()
        # Get application name, domain name and language from fileName
        self.applicationName = ''
        self.language = ''
        self.domain = ''
        parts = path.stem.split('-')
        if self.isPot:
            if len(parts) == 1:
                self.applicationName = self.domain = parts[0]
            else:
                self.applicationName, self.domain = parts
        else:
            if len(parts) == 1:
                self.applicationName = self.domain = ''
                self.language = parts[0]
            elif len(parts) == 2:
                self.applicationName = self.domain = parts[0]
                self.language = parts[1]
            else:
                self.applicationName, self.domain, self.language = parts
        # This flag will become True during the generation process, once this
        # file will have been generated
        self.generated = False

    def __repr__(self):
        '''String representation'''
        return '<%s: %d message(s)>' % (self.path.name, len(self.messages))

    def addMessage(self, message, needsCopy=True):
        '''Adds p_message among this file's messages'''
        if needsCopy:
            message = copy.copy(message)
        self.messages[message.id] = message
        return message

    def addHeader(self, header):
        '''Adds p_message among this file's headers'''
        self.headers[header.name] = header

    def update(self, newMessages, removeNotNew=False, keepOrder=True):
        '''Updates the existing messages with p_newMessages.
           If p_removeNotNew is True, all messages in self.messages
           that are not in p_newMessages will be removed. If p_keepOrder is
           False, self.messages will be sorted according to p_newMessages. Else,
           p_newMessages that are not yet in self.messages will be appended to
           the end of self.messages.'''
        # The method returns the list of added and removed messages (IDs)
        moves = O(added=[], removed=[])
        if removeNotNew:
            for id in self.messages.keys():
                if id not in newMessages:
                    moves.removed.append(id)
        for id in moves.removed: del self.messages[id]
        # Add new messages among existing messages
        if keepOrder:
            # Update existing messages and add inexistent messages to the end
            for message in newMessages:
                if message.id in self.messages:
                    msg = self.messages[message.id]
                else:
                    msg = self.addMessage(message)
                    moves.added.append(message.id)
                msg.update(message, self.isPot, self.language)
        else:
            # Remove, from self.messages, all messages not being in new
            # messages. We will append them at the end of the new messages.
            if not removeNotNew:
                notNew = [msg for msg in self.messages.values() \
                          if msg.id not in newMessages]
                for msg in notNew: del self.messages[msg.id]
            # Keep existing messages and start with a fresh dict
            existing = self.messages
            self.messages = collections.OrderedDict()
            for message in newMessages.values():
                if message.id in existing:
                    msg = existing[message.id]
                    self.messages[message.id] = msg
                else:
                    msg = self.addMessage(message)
                    moves.added.append(message.id)
                msg.update(message, self.isPot, self.language)
            # Append the list of old messages to the end
            if not removeNotNew:
                for message in notNew: self.messages[message.id] = message
        return moves

    def generateHeaders(self, f):
        if not self.headers:
            creationTime = time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())
            fb = ''
            if not self.isPot:
                # I must add fallbacks
                if self.language in fallbacks:
                    fb = '"X-is-fallback-for: %s\\n"' % fallbacks[self.language]
            f.write(poHeaders % (self.applicationName, creationTime,
                                 self.language, self.language, self.domain, fb))
        else:
            # Some headers were already found, we dump them as is
            f.write('msgid ""\nmsgstr ""\n')
            for header in self.headers.values():
                f.write(header.generate())
            f.write('\n')

    def generate(self, inFile=True):
        '''Generates the corresponding po(t) file on disk if p_inFile is True,
           in a io.StringIO else. In this latter case, the StringIO instance is
           returned.'''
        if inFile:
            f = open(str(self.path), 'w')
        else:
            f = io.StringIO()
        self.generateHeaders(f)
        for msg in self.messages.values():
            f.write(msg.generate())
            f.write('\n')
        if inFile:
            f.close()
        self.generated = True
        return f

    def getPoFileName(self, language):
        '''Gets the name of the po file that corresponds to this pot file and
           the given p_language.'''
        if self.applicationName == self.domain:
            r = '%s-%s.po' % (self.applicationName, language)
        else:
            r = '%s-%s-%s.po' % (self.applicationName, self.domain, language)
        return r

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Parser:
    '''Parse a translation file in po(t) format. The result is produced in
       self.res as a File instance.'''
    def __init__(self, path):
        self.res = File(path)

    # Regular expressions for msgIds, msgStrs and default values.
    rexDefault = re.compile('#\.\s+Default\s*:\s*"(.*)"')
    rexFuzzy = re.compile('#,\s+fuzzy')
    rexId = re.compile('msgid\s+"(.*)"')
    rexMsg = re.compile('msgstr\s+"(.*)"')

    def parse(self):
        '''Parse all i18n messages from the file and return the corresponding
           File instance.'''
        f = open(str(self.res.path), encoding='utf-8')
        # Currently parsed values
        msgDefault = msgFuzzy = msgId = msgStr = None
        comments = []
        # Walk every line of the po(t) file
        for line in f:
            lineContent = line.strip()
            if lineContent and (not lineContent.startswith('"')):
                r = self.rexDefault.match(lineContent)
                if r:
                    msgDefault = r.group(1)
                else:
                    r = self.rexFuzzy.match(lineContent)
                    if r:
                        msgFuzzy = True
                    else:
                        r = self.rexId.match(lineContent)
                        if r:
                            msgId = r.group(1)
                        else:
                            r = self.rexMsg.match(lineContent)
                            if r:
                                msgStr = r.group(1)
                            else:
                                if lineContent.startswith('#'):
                                    comments.append(lineContent.strip())
                if msgStr is not None:
                    if not ((msgId == '') and (msgStr == '')):
                        poMsg = Message(msgId, msgStr, msgDefault, msgFuzzy,
                                        comments)
                        self.res.addMessage(poMsg, needsCopy=False)
                    msgDefault = msgFuzzy = msgId = msgStr = None
                    comments = []
            if lineContent.startswith('"'):
                # It is a header value
                name, value = lineContent.strip('"').split(':', 1)
                if value.endswith('\\n'):
                    value = value[:-2]
                self.res.addHeader(Header(name.strip(), value.strip()))
        f.close()
        return self.res

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def load(path=None, pot=True, languages=None):
    '''Loads all "po" and "pot" files (or only "po" files if p_pot is False)
       wihin p_path, or within appy/tr/po if p_path is None. If p_languages is
       not None, we only read "po[t]" files related to these languages.'''
    r = {} # ~{s_fileName: File}~
    # Determine the path where to find po[t] files: the app's "tr" sub-folder or
    # Appy's "tr/po" sub-folder.
    path = path or pathlib.Path(__file__).parent
    # Search "po" files only, or "po" and "pot" files
    suffix = '*' if pot else ''
    # Browse files
    for poFile in path.glob('*.po%s' % suffix):
        # Dismiss temp files, ie .po.swp
        if poFile.suffix not in ('.po', '.pot'): continue
        if languages:
            # Bypass this file if its language is not among p_languages
            stem = poFile.stem
            language = stem if '-' not in stem else stem.rsplit('-', 1)[-1]
            if language not in languages: continue
        parser = Parser(poFile)
        r[poFile.name] = parser.parse()
    return r
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
