Feedreader
----------

A universal feed parser designed to operate on top of the lxml interface.

This is a VERY rough readme, and this project is very early in development. It however, is used to power Lifestrm.com.

Our mission was simple:

- Don't write an XML parser (we use lxml)
- Keep it transparent, but allow easy access to underlying objects.
- Support as many services as possible, and make accessing their media easy.

Features
--------

- RSS 2.0 (incl. media enclosures)
- Atom 1.0 (incl. link enclosures)

Installation
------------

- http://codespeak.net/lxml/
- http://labix.org/python-dateutil

Usage
-----

There are several methods which are usable to parse a feed::

	from feedreader import from_url
	parsed = from_url('http://www.domain.com/rss.xml')

	from feedreader import from_string
	parsed = from_string(open('my.rss', 'r').read())

	from feedreader import from_file
	parsed = from_file(open('my.rss', 'r'))

Once you have initialized the parser, you will be able to access supported elements
via a natural property syntax::

	>>> parsed.title
	My feed title
	>>> parsed.link
	http://www.domain.com/rss.xml
	>>> parsed.published
	datetime.datetime(2009, 8, 13, 2, 53, 11, 867908)

For the entries in a feed, you may use the `entries` accessor::

	>>> parsed.entries
	[<Entry ...>, <Entry ...>, <Entry ...>]

And each entry also supports similar common attributes::

	>>> parsed.entries[0].title
	My Article Name
	>>> parsed.entries[0].link
	http://www.domain.com/my-article-name

Keeping with our goals of allowing access to underlying XML, feedreader is a simple proxy. What this means is that while we provide accessors for many common attributes across feeds, you can still get at any XML element fairly easily::

	>>> parsed.myUnsupportedXMLTag
	(Fill me in with whatever lxml would return)