from bs4 import BeautifulSoup

from django.test import Client, TestCase

from .fixtures.menus import (absent,
                             empty,
                             no_subbranches,
                             single_subbranch1,
                             single_subbranch2,
                             single_subbranch3,
                             multiple_subbranches1,
                             multiple_subbranches2)


class MenuTagTestCase(TestCase):
    fixtures = ['menu_tag']

    def setUp(self):
        self.client = Client()
        self.maxDiff = None

    def get_menu_content(self, url, menu_id):
        html_bytes = self.client.get(url).content
        html = html_bytes.decode('utf-8')
        self.soup = BeautifulSoup(html, 'lxml')
        return str(self.soup.find('ul', {'id': menu_id}))

    def test_absent_menu(self):
        url = '/menu_tag/'
        menu = self.get_menu_content(url, 'meniu0')
        self.assertEqual(menu, absent)

    def test_empty_menu(self):
        url = '/menu_tag/'
        menu = self.get_menu_content(url, 'meniu1')
        self.assertEqual(menu, empty)

    def test_only_top(self):
        url = '/menu_tag/'
        menu = self.get_menu_content(url, 'meniu2')
        self.assertEqual(menu, no_subbranches)

    def test_single_subbranch1(self):
        url = '/menu_tag/?item=meniu3-punkt1'
        menu = self.get_menu_content(url, 'meniu3')
        self.assertEqual(menu, single_subbranch1)

    def test_single_subbranch2(self):
        url = '/menu_tag/?item=meniu4-punkt2'
        menu = self.get_menu_content(url, 'meniu4')
        self.assertEqual(menu, single_subbranch2)

    def test_single_subbranch3(self):
        url = '/menu_tag/?item=meniu5-punkt3'
        menu = self.get_menu_content(url, 'meniu5')
        self.assertEqual(menu, single_subbranch3)

    def test_multiple_subbranches1(self):
        url = '/menu_tag/?item=meniu6-punkt2'
        menu = self.get_menu_content(url, 'meniu6')
        self.assertEqual(menu, multiple_subbranches1)

    def test_multiple_subbranches2(self):
        url = '/menu_tag/?item=meniu6-punkt3'
        menu = self.get_menu_content(url, 'meniu6')
        self.assertEqual(menu, multiple_subbranches2)
