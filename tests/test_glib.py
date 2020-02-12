import unittest
from textscript.glib import *


class TestGlib(unittest.TestCase):

    def test_check_directory(self):

        # Pass tests directory which must exist
        result = check_directory('tests')

        # Assert test directory exists
        assert result is True

    def test_create_folder(self):

        # Test Directory
        test_directory = 'tests/test_folder'

        # Create Test Directory
        create_folder(test_directory)

        # Assert tests/test_folder exists
        assert os.path.isdir(test_directory)

        # Delete test_directory
        parent_dir = os.getcwd()
        delete_dir = os.path.join(parent_dir, test_directory)
        os.removedirs(delete_dir)

    def test_list_subdirectories(self):
        pass

    def test_list_files(self):
        pass

    def test_list_shortcuts(self):
        pass

    def test_print_shortcuts(self):
        pass


if __name__ == '__main__':
    unittest.main()
