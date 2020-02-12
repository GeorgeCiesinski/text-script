"""
Contains non-class or miscellaneous methods
"""

import os


def check_directory(directory):
    """
    Checks directory to see if folder exists
    """

    # Return true if directory exists
    if os.path.isdir(directory):
        return True
    else:
        return False
        print("Missing log directory.")


def create_folder(directory):
    """
    Creates directory in project folder
    """

    parent_dir = os.getcwd()
    folder_dir = os.path.join(parent_dir, directory)

    try:
        os.mkdir(folder_dir)
    except OSError as error:
        print("Unable to create Log directory in project folder due to the following error:")
        print(error)


def list_subdirectories(_directory):
    """
    Lists all subdirectories.

    :param _directory:
    :return directory_list:
    :rtype list:
    """

    directory_list = list()

    for _root, _dirs, _files in os.walk(_directory, topdown=False):
        for name in _dirs:
            directory_list.append(os.path.join(_root, name))

    return directory_list


def list_files(_directory):
    """
    Lists all files and subdirectories in the directory. Returns list

    :param _directory:
    :return _file_list, _file_dir_list:
    :rtype list:
    """

    _file_list = list()
    _file_dir_list = list()

    for root, dirs, files in os.walk(_directory, topdown=False):
        for name in files:
            _file_list.append(name)
            _file_dir_list.append(os.path.join(root, name))

    return _file_list, _file_dir_list


def list_shortcuts(_file_list):
    """
    list_shortcuts creates a list of the raw shortcut strings the user would be typing in

    :param _file_list:
    :return _shortcut_list:
    :rtype list:
    """

    _shortcut_list = list()

    for f in _file_list:
        f = f.split(".")
        _shortcut_list.append(f[0])

    return _shortcut_list


def print_shortcuts(_file_dirs, _shortcuts):

    for _file_dir in _file_dirs:
        index = _file_dirs.index(_file_dir)
        print(f"Shortcut: {_shortcuts[index]}   - - -    Directory: {_file_dir}")


if __name__ == "__main__":

    text_block_dir = '../textblocks/'

    file_list = list_files(text_block_dir)

    shortcut_list = list_shortcuts(file_list)


