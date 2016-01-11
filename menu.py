import re
import datetime

import requests
from bs4 import BeautifulSoup


class GuckenheimerMenu(object):
    BASE_URL = "http://dining.guckenheimer.com/clients/"
    WEEKLY_PATH = "weeklyMenuLaunch"

    def __init__(self, client_name):
        self.client_name = client_name
        self.mapping = [{'name': 'Breakfast~entree', 'path': 'breakfastentree'}]
        self.categories = None
        self.results_by_category = {}
        self.results_by_day = {}
        self.populated = False

    def _get_url(self):
        return self.BASE_URL + self.client_name + '/fss/fss.nsf/'

    def fetch(self, url):
        request = requests.get(url)
        request.raise_for_status()

        return request.content

    @staticmethod
    def get_current_week(today=None):
        if today is None:
            today = datetime.date.today()

        monday = today + datetime.timedelta(days=-today.weekday())

        return monday.strftime("%m-%d-%Y")

    def _fetch_weekly(self, category, today=None):
        url = (self._get_url() + self.WEEKLY_PATH + '/' + self.get_identifier() + "~" +
               self.get_current_week(today) + "/$file/" + category + '.htm')

        return self.fetch(url)

    def _fetch_daily(self, day, today):
        url = (self._get_url() + self.WEEKLY_PATH + '/' + self.get_identifier() + "~" +
               self.get_current_week(today) + "/$file/" + day + '.htm')

        return self.fetch(url)

    def get_categories(self):
        if self.categories is not None:
            return self.categories

        self.categories = {}

        url = (self._get_url() + self.WEEKLY_PATH + '/' + self.get_identifier() +
               "~01-04-2016/$file/" + 'cafehome' + '.htm')

        soup = BeautifulSoup(self.fetch(url), 'html.parser')

        for category in soup.find("td", id="right").find_all('a', class_=None):
            self.categories[category.attrs['href'][:-4]] = category.contents[0]

        return self.categories

    def populate(self, today=None):
        self.get_categories()
        if not self.populated:
            self.populated = True

            for day in range(1, 6):
                self._get_daily_schedule(day, today)

    def find_category(self, name, contains=True):
        categories = self.get_categories()

        for category in categories:
            if str(categories[category]).lower() == str(name).lower():
                return category
            if contains and str(name).lower() in str(categories[category]).lower():
                return category
        return None

    def get_identifier(self):
        response = self.fetch(self._get_url() + 'fssredirect?OpenPage')

        return re.search('locid=(.*)&', str(response)).group(1)

    def _get_weekly_schedule(self, category):
        soup = BeautifulSoup(self._fetch_weekly(category))

        for entree in soup.find("td", id="center_text").find_all('div', class_=None):
            pass

    def _get_daily_schedule(self, day, today=None):
        soup = BeautifulSoup(self._fetch_daily('day' + str(day), today), 'html.parser')

        category = None
        new_day = {}

        for entree in soup.find("td", id="center_text").find_all('div'):
            if len(entree.attrs):
                category = entree.contents[0]
            else:
                if self.find_category(category) not in self.results_by_category:
                    self.results_by_category[self.find_category(category)] = []
                self.results_by_category[self.find_category(category)].append(str(entree.contents[0]).strip())

                new_day[self.find_category(category)] = str(entree.contents[0]).strip()

        self.results_by_day[day] = new_day

    def get_menu(self, category=None, day=None):
        self.populate()
        if category is not None and day is not None:
            return self.results_by_day[day][self.find_category(category)]
        elif category is not None:
            return self.results_by_category[self.find_category(category)]
        else:
            return self.results_by_day[day]
