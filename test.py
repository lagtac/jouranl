import unittest
import main


class TestArgParser(unittest.TestCase):
    ''' Testing '''
    def test_list_parser(self):
        args = ['-a']
        self.assertEqual(main.parse_args(args), '')


if __name__=='__main__':
    unittest.main()
    #print(9)