import datetime
import unittest
import responses

from menu import GuckenheimerMenu


class TestMenu(unittest.TestCase):

    def setUp(self):
        self.menu = GuckenheimerMenu('twitterseattle')

    @responses.activate
    def test_get_identifier(self):
        with open('resources/tests/fssredirect') as file:
            # NOTE: do not include ?OpenPage when using responses
            responses.add(responses.GET, 'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/fssredirect',
                      body=file.read(), status=200,
                      content_type='text/html')

        self.assertEqual('9L7P2S', self.menu.get_identifier())

    @responses.activate
    def test_get_categories(self):
        with open('resources/tests/cafehome.htm') as file:
            responses.add(responses.GET,
                      'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/weeklyMenuLaunch/9L7P2S~01-04-2016/$file/cafehome.htm',
                      body=file.read(), status=200,
                      content_type='text/html')

        with open('resources/tests/fssredirect') as file:
            # NOTE: do not include ?OpenPage when using responses
            responses.add(responses.GET, 'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/fssredirect',
                      body=file.read(), status=200,
                      content_type='text/html')

        categories = self.menu.get_categories()

        self.assertIn('breakfastentree', categories)
        self.assertEqual(categories['breakfastentree'], 'Breakfast~entree')

        self.assertIn('entreefeature1', categories)
        self.assertEqual(categories['entreefeature1'], 'Entree Feature 1')


    @responses.activate
    def test_category_search(self):
        with open('resources/tests/fssredirect') as file:
            # NOTE: do not include ?OpenPage when using responses
            responses.add(responses.GET, 'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/fssredirect',
                      body=file.read(), status=200,
                      content_type='text/html')

        with open('resources/tests/cafehome.htm') as file:
            responses.add(responses.GET,
                      'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/weeklyMenuLaunch/9L7P2S~01-04-2016/$file/cafehome.htm',
                      body=file.read(), status=200,
                      content_type='text/html')

        with open('resources/tests/day1.htm') as file:
            responses.add(responses.GET,
                      'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/weeklyMenuLaunch/9L7P2S~01-04-2016/$file/day1.htm',
                      body=file.read(), status=200,
                      content_type='text/html')

        with open('resources/tests/day2.htm') as file:
            responses.add(responses.GET,
                      'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/weeklyMenuLaunch/9L7P2S~01-04-2016/$file/day2.htm',
                      body=file.read(), status=200,
                      content_type='text/html')

        with open('resources/tests/day3.htm') as file:
            responses.add(responses.GET,
                      'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/weeklyMenuLaunch/9L7P2S~01-04-2016/$file/day3.htm',
                      body=file.read(), status=200,
                      content_type='text/html')

        with open('resources/tests/day4.htm') as file:
            responses.add(responses.GET,
                      'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/weeklyMenuLaunch/9L7P2S~01-04-2016/$file/day4.htm',
                      body=file.read(), status=200,
                      content_type='text/html')

        with open('resources/tests/day5.htm') as file:
            responses.add(responses.GET,
                      'http://dining.guckenheimer.com/clients/twitterseattle/fss/fss.nsf/weeklyMenuLaunch/9L7P2S~01-04-2016/$file/day5.htm',
                      body=file.read(), status=200,
                      content_type='text/html')

        self.menu.populate(datetime.datetime(2016, 1, 10))

        self.assertEqual('soupstewchili', self.menu.find_category('SOUP ~ STEW ~ CHILI'))