from unittest import TestCase
from wax.wax_dsl import Keys


class TestKeys(TestCase):
    def test_success(self):
        obj = [{'aa': 1, 'bb': [{'aa': 2, 'bb': 3}]}] - Keys('aa', 'bb.bb')
        self.assertListEqual(obj, [{'bb': [{'aa': 2}]}])
        obj = [[{'aa': 1}]] - Keys('aa')
        self.assertListEqual(obj, [[{'aa': 1}]])
