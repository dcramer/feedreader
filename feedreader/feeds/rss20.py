"""
RSS 2.0 Support
"""

from feedreader.utils.dates import parse_date
from feedreader.feeds import Feed, Item, Tag, Author, Thumbnail, Image, Enclosure

class RSS20Item(Item):
    _published = None
    _enclosures = None
    
    @property
    def author(self):
        # TODO: implement parsing on this to at least support
        # standard author formats such as "Name <email.com>".
        if self._author is None:
            author = self._xml.author
            self._author = Author(
                name=author,
            )
        return self._author
    
    @property
    def description(self):
        return unicode(self._xml.description).strip()
    
    def _process_links(self):
        # <media:thumbnail url="http://th04.deviantart.net/fs48/300W/f/2009/207/d/7/d7400f45d945d29fa1edba98531bc887.jpg" height="399" width="300"/>
        # <media:content url="http://fc04.deviantart.com/fs48/f/2009/207/d/7/d7400f45d945d29fa1edba98531bc887.jpg" height="936" width="704" medium="image"/>
        # TODO: These need changed to namespaces
        self._enclosures = []
        for enclosure in self._xml.iterchildren(tag='thumbnail'):
            self._enclosures.append(Thumbnail(enclosure.attrib['url']))
        for enclosure in self._xml.iterchildren(tag='content'):
            if enclosure.attrib.get('medium') == 'image':
                self._enclosures.append(Image(enclosure.attrib['url']))
            else:
                self._enclosures.append(Enclosure(enclosure.attrib['url']))

    @property
    def enclosures(self):
        if self._enclosures is None:
            self._process_links()
        return self._enclosures
    
    media = enclosures
    
    @property
    def published(self):
        if self._published is None:
            try:
                self._published = parse_date(self._xml.pubDate)
            except AttributeError:
                self._published = None
        return self._published

    updated = published

    @property
    def id(self):
        return self._xml.guid

class RSS20Feed(Feed):
    _published = None
    _updated = None
    
    __feed__ = 'RSS 2.0'
    
    def __getattr__(self, attr, default=None):
        result = getattr(self._xml.channel, attr, default)
        if result is not None:
            result = Tag(result)
        return result
    
    @property
    def is_valid(self):
        return self._xml.tag == 'rss' and self._xml.attrib['version'] == '2.0'
    
    @property
    def published(self):
        if self._published is None:
            try:
                datestr = self._xml.channel.pubDate
            except AttributeError:
                self._published = None
            else:
                self._published = parse_date(datestr)
        return self._published

    @property
    def updated(self):
        if self._updated is None:
            try:
                datestr = self._xml.channel.lastBuildDate
            except AttributeError:
                self._updated = self.published
            else:
                self._updated = parse_date(datestr)
        return self._updated
    
    @property
    def entries(self):
        return [RSS20Item(item) for item in self._xml.channel.iterchildren(tag='item')]