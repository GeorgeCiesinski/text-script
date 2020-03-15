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


def test_list_shortcuts():

    sample_file_list = ["#example.txt", "#example2.txt", "#test.txt", "#test2.txt"]
    expected_shortcut_list = ["#example", "#example2", "#test", "#test2"]
    shortcut_list = glib.list_shortcuts(sample_file_list)
    for shortcut in shortcut_list:
        assert shortcut in expected_shortcut_list
        assert shortcut not in sample_file_list

def test_shortcut_compatibility_check():

    sample_passing_shortcuts = ["#example", "!example2", "#test1", "!test2"]
    sample_failing_shortcuts = ["#example#", "!example!", "#example!", "!example#", "#te#st", "#te!st2"]
    for sample in sample_passing_shortcuts:
        result = glib._shortcut_compatibility_check(sample)
        assert result is True
    for sample in sample_failing_shortcuts:
        result = glib._shortcut_compatibility_check(sample)
        assert result is False

def test_print_shortcuts():

    # This function relies on the print() function which is expected to work
    pass
