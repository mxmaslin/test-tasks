from bs4 import BeautifulSoup
from pprint import pprint

from django.test import Client, TestCase

from .html_to_json import HTMLtoJSONParser as dictifier

from .fixtures.menus import (absent,
                             empty,
                             no_subbranches,
                             single_subbranch1,
                             single_subbranch2,
                             single_subbranch3,
                             multiple_subbranches)


class MenuTagTestCase(TestCase):
    fixtures = ['menu_tag']

    def setUp(self):
        client = Client()
        html_bytes = client.get('/menu_tag/').content
        html = html_bytes.decode('utf-8')
        self.soup = BeautifulSoup(html, 'lxml')

    def get_menu_content(self, menu_id):
        return str(self.soup.find('ul', {'id': menu_id}))

    def test_absent_menu(self):
        menu_html = self.get_menu_content('meniu0')
        menu_dict = dictifier.to_json(menu_html)
        self.assertEqual(menu_dict, absent)

    def test_empty_menu(self):
        menu_html = self.get_menu_content('meniu1')
        menu_dict = dictifier.to_json(menu_html)
        self.assertEqual(menu_dict, empty)

    def test_only_top(self):
        menu_html = self.get_menu_content('meniu2')
        menu_dict = dictifier.to_json(menu_html)
        self.assertEqual(menu_dict, no_subbranches)

    def test_single_subbranch1(self):
        menu_html = self.get_menu_content('meniu3')
        menu_dict = dictifier.to_json(menu_html)
        self.assertEqual(menu_dict, single_subbranch1)

    def test_single_subbranch2(self):
        menu_html = self.get_menu_content('meniu4')
        menu_dict = dictifier.to_json(menu_html)
        self.assertEqual(menu_dict, single_subbranch2)

    def test_single_subbranch3(self):
        menu_html = self.get_menu_content('meniu5')
        menu_dict = dictifier.to_json(menu_html)
        self.assertEqual(menu_dict, single_subbranch3)

    def test_multiple_subbranches(self):
        menu_html = self.get_menu_content('meniu6')
        menu_dict = dictifier.to_json(menu_html)
        self.assertEqual(menu_dict, multiple_subbranches)
