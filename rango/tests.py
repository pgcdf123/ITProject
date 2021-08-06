from django.test import TestCase
from rango.models import Category
from rango.models import Page
from django.urls import reverse

# Create your tests here.

"""
    Testing whether two categories can have same slug.
    The expected result would be no, because we have set 
    the slug to be unique.
    Test report:
        django.db.utils.IntegrityError: UNIQUE constraint failed: rango_category.slug
    This is the result that we want, we cannot create same category and slug.
"""


class CategoryTests(TestCase):
    def test_slug_unique(self):
        category_1 = Category(name='Rango test')
        category_2 = Category(name='Rango test')
        category_1.save()
        category_2.save()

        self.assertEqual(category_1.slug, category_2.slug)


"""
    Test for whether the response is 200 correct or not
"""

class LoginTests(TestCase):

    def test_login_(self):
        response = self.client.get(reverse('rango:login'))
        self.assert_(response.status_code, 200)


"""
    Test for accessing register page.
"""
class RegisterTest(TestCase):

    def test_register(self):
        response = self.client.get(reverse('rango:register'))
        self.assert_(response.status_code, 200)
        self.assertContains(response, 'Register here!')









