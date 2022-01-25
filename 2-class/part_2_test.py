import unittest

from part_2 import Person


class TestPerson(unittest.TestCase):
    def test_last_name_is_returned(self):
        p = Person('john adams', 25, 'dev', [])
        self.assertEqual(p.last_name(), 'adams')

    def test_no_last_name(self):
        p = Person('john', 25, 'dev', [])
        self.assertEqual(p.last_name(), '')

    def test_has_kids_with_kids(self):
        p = Person('james adams', 30, 'dev', ['john'])
        self.assertTrue(p.has_kids())

    def test_has_kids_with_no_kids(self):
        p = Person('james', 30, 'dev', [])
        self.assertFalse(p.has_kids())


if __name__ == '__main__':
    unittest.main()
