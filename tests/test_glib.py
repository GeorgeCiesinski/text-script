import pytest
from textscript import glib

def test_check_directory():
    assert not glib.check_directory('fasfbabfabflrfb')
    assert glib.check_directory('.github')


def test_list_subdirectories():

    expected_list = ['./.github', './assets', './tests', './textscript']
    dir_list = glib.list_subdirectories('.')
    for dir in expected_list:
        assert dir in dir_list


def test_list_files():


    expected_file_names = ['glib.py', 'README.md', '.gitignore', 'pull_request_template.md']
    expected_file_paths = ['./textscript/glib.py', './README.md', './.gitignore', './.github/pull_request_template.md']
    file_list, dir_list = glib.list_files('.')
    for file in expected_file_names:
        assert file in file_list
    for file_path in expected_file_paths:
        assert file_path in dir_list