"""
Atom 1.0 Support
"""

from feedreader.utils.dates import parse_date
from feedreader.feeds import Feed, Item, Author, Image, Enclosure

class Atom10Item(Item):
    _enclosures = None
    _published = None
    _updated = None
    _link = None
    _author = None
    
    def _process_links(self):
        self._enclosures = []
        for link in self._xml.iterchildren(tag='link'):
            if link.attrib['rel'] == 'alternate':
                self._link = link.attrib['href']
            elif link.attrib['rel'] == 'enclosure':
                if link.attrib['type'].startswith('image/'):
                    cls = Image
                else:
                    cls = Enclosure
                self._enclosures.append(cls(link.attrib['href'], link.attrib['type']))
    
    @property
    def author(self):
        if self._author is None:
            author = self._xml.author
            self._author = Author(
                name=getattr(author, 'name', None),
                email=getattr(author, 'email', None),
                link=getattr(author, 'uri', None),
            )
        return self._author
    
    @property
    def link(self):
        if self._link is None:
            self._process_links()
        return self._link
    
    @property
    def enclosures(self):
        if self._enclosures is None:
            self._process_links()
        return self._enclosures
    
    media = enclosures
    
    @property
    def description(self):
        return unicode(self._xml.description).strip()
    
    @property
    def published(self):
        if self._published is None:
            try:
                datestr = self._xml.published
            except AttributeError:
                self._published = self.updated
            else:
                self._published = parse_date(datestr)
        return self._published

    @property
    def updated(self):
        if self._updated is None:
            try:
                datestr = self._xml.updated
            except AttributeError:
                self._updated = None
            else:
                self._updated = parse_date(datestr)
        return self._updated

class Atom10Feed(Feed):
    _published = None
    _updated = None
    
    __feed__ = 'Atom 1.0'
    
    @property
    def published(self):
        if self._published is None:
            try:
                datestr = self._xml.feed.published
            except AttributeError:
                self._published = self.updated
            else:
                self._published = parse_date(datestr)
        return self._published

    @property
    def updated(self):
        if self._updated is None:
            try:
                datestr = self._xml.feed.updated
            except AttributeError:
                self._updated = None
            else:
                self._updated = parse_date(datestr)
        return self._updated
    
    @property
    def is_valid(self):
        # <feed xmlns="http://www.w3.org/2005/Atom">
        return self._xml.tag == '{http://www.w3.org/2005/Atom}feed'
    
    @property
    def entries(self):
        return [Atom10Item(item) for item in self._xml.iterchildren(tag='{http://www.w3.org/2005/Atom}entry')]