from bs4 import BeautifulSoup
from pprint import pprint

from django.test import Client, TestCase

from .html_to_json import HTMLtoJSONParser as dictifier

from .fixtures.menus import only_top

class MenuTagTestCase(TestCase):
    fixtures = ['menu_tag']

    def setUp(self):
        client = Client()
        html_bytes = client.get('/menu_tag/').content
        html = html_bytes.decode('utf-8')
        self.soup = BeautifulSoup(html, 'lxml')

    def get_menu_content(self, menu_id):
        return str(self.soup.find('ul', {'id': menu_id}).contents)

    def test_only_top(self):
        menu_html = self.get_menu_content('meniu2')
        menu_dict = dictifier.to_json(menu_html)
        self.assertEqual(menu_dict, only_top)
