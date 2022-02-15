from django.test import TestCase
from .views import margin


def mod(x):
    return x % 3


class Tests(TestCase):
    def test_mod(self):
        self.assertEqual(mod(4), 1)



