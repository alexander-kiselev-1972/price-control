from django.test import TestCase
from .views import margin


class Test(TestCase):
    def test_margin(self):
        result100 = margin(100.00)
        result101 = margin(101.00)
        result500 = margin(500.00)
        result501 = margin(501.00)
        self.assertEqual(163.90, result100)
        self.assertEqual(153.32, result101)
        self.assertEqual(759.00, result500)
        self.assertEqual(672.34, result501)

