from unittest import TestCase
from wax.utils import eafp


class TestEafp(TestCase):
    def test_success(self):
        result = eafp(lambda: [][1], default='error')
        self.assertEqual(result, 'error')
        result = eafp(lambda: [1, 2][1], default=0)
        self.assertEqual(result, 2)
