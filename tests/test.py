import unittest
from jouranl import cli
from jouranl import dateparse


class ArgParserTestCase(unittest.TestCase):

    def test_write_arguments(self):
        args = 'write --editor --meta --tags tag1 tag2 -- this is a note'
        namespace = cli.parse_args(args.split(' '))
        self.assertEqual(namespace.command, 'write')
        self.assertEqual(namespace.editor, True)
        self.assertEqual(namespace.meta, True)
        self.assertEqual(namespace.tags, ['tag1', 'tag2'])
        self.assertEqual(namespace.tags, ['tag1', 'tag2'])
        self.assertEqual(namespace.entry, ['this', 'is', 'a',  'note'])

    def test_list_arguments(self):
        args = 'list,--all'
        namespace = cli.parse_args(args.split(','))
        self.assertEqual(namespace.command, 'list')
        self.assertEqual(namespace.all, True)


if __name__ == '__main__':
    unittest.main()
    # print(9)
