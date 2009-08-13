import unittest
import os.path
import itertools

from feedreader import from_file

DIR = os.path.abspath(os.path.dirname(__file__))

RSS_FILES = (
    ('rss/reddit.xml', {
        'title': 'reddit.com: what\'s new online!',
        'link': 'http://www.reddit.com/',
        'description': '',
        'entries': (
            {
                'title': 'the answer to the energy crisis is donuts [solar cells from donuts]',
                'link': 'http://www.reddit.com/r/science/comments/86yb2/the_answer_to_the_energy_crisis_is_donuts_solar/',
            },
            {
                'title': 'Do no evil my ass, google is now supporting domain squatters',
                'link': 'http://www.reddit.com/r/reddit.com/comments/86297/do_no_evil_my_ass_google_is_now_supporting_domain/',
            },
            {
                'title': u'The Best 10 \u201cThe Best \u2026 of 2008\u2033 of 2008',
                'link': 'http://www.reddit.com/r/pics/comments/7m2sa/the_best_10_the_best_of_2008_of_2008/',
            }
        )
    }),
    ('rss/digg.xml', {
        'title': 'digg / kevinrose / history',
        'link': 'http://digg.com/users/kevinrose/history',
        'description': 'A history of kevinrose\'s activity at digg.com',
        'entries': (
            {
                'title': 'Tea Measurements: What is the best way to measure loose tea?',
                'link': 'http://digg.com/food_drink/Tea_Measurements_What_is_the_best_way_to_measure_loose_tea',
                'author': 'kevinrose',
            },
            # Digg has some screwy feeds with empty items
            {
                'title': '',
                'link': 'http://digg.com/users/kevinrose/friends/view',
            },
            {
                'title': '',
                'link': 'http://digg.com/users/kevinrose/friends/view',
            },
            {
                'title': '',
                'link': 'http://digg.com/users/kevinrose/friends/view',
            },
            {
                'title': 'Palm webOS 1.1 now available, fixes iTunes 8.2.1 syncing',
                'link': 'http://digg.com/gadgets/Palm_webOS_1_1_now_available_fixes_iTunes_8_2_1_syncing',
                'description': 'Time to update your Pre, as Palm has released webOS 1.1.0. Quite a bit of changes here, and most importantly, the patch notes say that it "Resolves an issue preventing media sync from working with latest version of iTunes (8.2.1)."',
                'author': 'kevinrose',
            },
        )
    }),
    ('rss/deviantart.xml', {
        'title': 'Sooper-Deviant\'s Gallery',
        'link': 'http://browse.deviantart.com/?order=5&q=gallery%3ASooper-Deviant',
        'description': 'deviantART RSS for  sort:time gallery:Sooper-Deviant',
        'entries': (
            {
                'title': 'Small Universe 9848',
                'link': 'http://Sooper-Deviant.deviantart.com/art/Small-Universe-9848-130937420',
                'enclosures': (
                    {
                        'href': 'http://th04.deviantart.net/fs48/300W/f/2009/207/d/7/d7400f45d945d29fa1edba98531bc887.jpg',
                        'media': 'thumbnail',
                    },
                ),
            },
        )
    }),
)

class RSSTestCase(unittest.TestCase):
    def testParsing(self):
        for fname, test_data in RSS_FILES:
            fp = open(os.path.join(DIR, fname), 'r')
            parsed = from_file(fp)

            self.assertEquals(parsed.tag, 'channel')
            self.assertEquals(parsed.feed, 'RSS 2.0')
            self.assertEquals(parsed.title, test_data['title'])
            self.assertEquals(parsed.link, test_data['link'])
            self.assertEquals(parsed.description, test_data['description'])
            # Test the first one:
            for entry, test_req in itertools.izip(parsed.entries[:len(test_data['entries'])], test_data['entries']):
                self.assertEquals(entry.tag, 'item')
                self.assertEquals(entry.guid, entry.id)
                for field in ('author', 'title', 'link', 'description', 'id'):
                    if field in test_req:
                        self.assertEquals(unicode(getattr(entry, field)), test_req[field])
                enclosures = test_req.get('enclosures', [])
                # THere is a bug with entry.enclosures not working if you slice it first
                for enclosure, test_req in itertools.izip(entry.enclosures[:len(enclosures)], enclosures):
                    for field in ('href', 'type'):
                        if field in test_req:
                            self.assertEquals(unicode(getattr(enclosure, field)), test_req[field])

if __name__ == '__main__':
    unittest.main()