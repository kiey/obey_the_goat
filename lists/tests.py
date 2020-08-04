from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
import re
from django.template.loader import render_to_string


from lists.views import home_page

class HomePageTest(TestCase):

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')

        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')
        html = self.remove_csrf(response.content.decode())

        self.assertEqual(html, expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        html = self.remove_csrf(response.content.decode())

        self.assertIn('A new list item', html)
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(html, expected_html)



