# ------------------------------------------------------------------------------
from appy.pod.xhtml import tags, visitors
from appy.shared.xml_parser import XmlEnvironment, XmlParser, Escape

# ------------------------------------------------------------------------------
CHUNK_NOT_WITH_FILE = 'Cannot parse a file when chunk=True, only a string.'

# ------------------------------------------------------------------------------
class XhtmlEnvironment(XmlEnvironment):
    def __init__(self):
        # Call the base constructor
        XmlEnvironment.__init__(self)
        # The parsing result will store a root Tag instance
        self.r = None
        # The currently walked tag (a tags.Tag or sub-class' instance)
        self.current = None
        # The current content (a tags.Content instance)
        self.content = None
        # Tags encountered so far, by type
        self.tags = {}
        # The main parser (see below)
        self.parser = None

    def addTag(self, tag):
        '''A new p_tag has been encountered. Add it in the environment's local
           data structures.'''
        # Store it as the current tag
        if not self.r:
            # It is the root tag
            self.r = tag
            isRoot = True
        else:
            isRoot = False
        self.current = tag
        # Store it in self.tags if walkable. Do not store the root tag: it is a
        # tag that was artificially added to ensure there is a single root tag.
        klass = tag.__class__
        if not isRoot and klass.walkable:
            name = klass.__name__
            if name in self.tags:
                self.tags[name].append(tag)
            else:
                self.tags[name] = [tag]

# ------------------------------------------------------------------------------
class XhtmlParser(XmlParser):
    '''Creates a tree of Tag elements from a chunk of XHTML code as a string'''

    def __init__(self, env=None, caller=None, chunk=False, encoded=False,
                 compress=True, normalizeTables=True, optimizeTables=False,
                 keepWithNext=0, removeTrailingParas=None):
        # Define a default environment if p_env is None
        env = env or XhtmlEnvironment()
        # Call the base constructor
        XmlParser.__init__(self, env, caller)
        # If the XHTML to parse is not a complete, single-root-tag XML, but,
        # instead, a chunk of XHTML potentially containing several tags at the
        # root level, p_chunk is True and the XHTML chunk will be surrounded by
        # a faxe "x" tag.
        self.chunk = chunk
        # The parser will output UTF-8 in a unicode string. If you need it to be
        # encoded as a str, specify p_encoded being True.
        self.encoded = encoded
        # By default, "compress" is True: the parser will remove ignorable
        # whitespace to produce a shorter output. If it is a requirement to keep
        # the general formatting of the input XHTML, set p_compress to False.
        self.compress = compress
        # Define the visitors that will walk the tree of tags we will build
        activated = []
        if normalizeTables:
            activated.append(visitors.TablesNormalizer())
        if optimizeTables:
            activated.append(visitors.TablesOptimizer())
        if keepWithNext:
            activated.append(visitors.KeepWithNext(keepWithNext))
        if removeTrailingParas is not None:
            cleaner = visitors.Cleaner(removeTrailingParas=removeTrailingParas)
            activated.append(cleaner)
        self.visitors = activated
        # This flag is True if the input XHTML has been modified by at least one
        # visitor.
        self.updated = False

    def parse(self, xml, source='string'):
        '''Surrounds p_xml with a fake root tag if p_self.chunk is True, before
           calling the base method.'''
        # Surrounding with a fake tag is only possible if p_source is "string"
        chunk = self.chunk
        if chunk:
            if source == 'string':
                xml = '<x>%s</x>' % xml
            else:
                raise Exception(CHUNK_NOT_WITH_FILE)
        # Call the base method
        return XmlParser.parse(self, xml, source=source)

    def startElement(self, elem, attrs):
        '''Manages the start of a tag'''
        env = self.env
        # Clean current content
        env.content = None
        # Create the corresponding Tag instance
        tag = tags.get(elem)(elem, attrs, parent=env.current)
        env.addTag(tag)

    def endElement(self, elem):
        '''Manages the end of a tag'''
        env = self.env
        # Clean current content
        env.content = None
        # We are back to p_elem's parent
        env.current = env.current.parent

    def characters(self, text):
        '''Manages text encountered within the current tag'''
        env = self.env
        # Ignore p_text if directly contained in a tag that is not supposed to
        # directly contain content. In that case, p_text is probably ignorable
        # whitespace. Avoid doing this if p_self.compress is False.
        if env.current.structural and self.compress: return
        # Xhtml-escape p_text and store it on the environment
        text = Escape.xml(text)
        if env.content:
            env.content.text += text
        else:
            # Create a Content instance to store p_text
            content = env.content = tags.Content(text)
            # Add content as child of the current tag
            tag = env.current
            if tag.children:
                tag.children.append(content)
            else:
                tag.children = [content]

    def endDocument(self):
        '''Converts p_self.env.r into a chunk of ODF code and store it in
           p_self.res.'''
        env = self.env
        # Accept the visitors
        for visitor in self.visitors:
            updated = visitor.visit(env)
            self.updated = self.updated or updated
        self.res = env.r.asXhtml()
        if self.chunk:
            # Remove the base tag
            self.res = self.res[3:-4]
        if self.encoded:
            self.res = self.res.encode('utf-8')
# ------------------------------------------------------------------------------
