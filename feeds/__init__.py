from feedreader.utils.proxy import Proxy

class InvalidFeed(Exception): pass

class BetterObject(object):
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self)

class Tag(BetterObject, Proxy):
    def __unicode__(self):
        return unicode(self.__instance__).strip()

class Author(BetterObject):
    def __init__(self, name=None, email=None, link=None):
        self.name, self.email, self.link = name, email, link

    def __str__(self):
        if self.email:
            return "%s <%s>" % (self.name, self.email)
        elif self.name:
            return str(self.name)
        return str(self.link)

class Enclosure(BetterObject):
    media = None
    
    def __init__(self, href, type=None):
        self.type, self.href = type and unicode(type) or None, unicode(href)
    
    def __str__(self):
        if self.type:
            return '%s:%s' % (self.type, self.href)
        return self.href

    @property
    def link(self):
        return self.href

class Image(Enclosure):
    media = 'image'

class Thumbnail(Image):
    media = 'thumbnail'

class Feed(BetterObject):
    __feed__ = ''
    
    author = Author()
    is_valid = False
    
    def __init__(self, node):
        self._xml = node
        if not self.is_valid:
            raise InvalidFeed
    
    def __str__(self):
        return self.feed

    def __getattr__(self, attr, default=None):
        result = getattr(self._xml, attr, default)
        if result is not None:
            result = Tag(result)
        return result
    
    @property
    def entries(self):
        raise NotImplementedError
    
    @property
    def feed(self):
        return self.__feed__

class Item(BetterObject):
    author = Author()
    enclosures = []

    def __init__(self, node):
        self._xml = node

    def __getattr__(self, attr, default=None):
        return getattr(self._xml, attr, default)

    def __str__(self):
        return str(self.id or self.title)