"""
George's Library
Contains non-class methods for this program.
"""

import os


def list_subdirectories(directory):
    """
    Lists all subdirectories.

    :param directory:
    :return directory_list:
    :rtype list:
    """

    directory_list = list()

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))

    return directory_list


def list_files(directory):
    """
    Lists all files and subdirectories in the directory. Returns list

    :param directory:
    :return file_list, file_dir_list:
    :rtype list:
    """

    file_list = list()
    file_dir_list = list()

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_list.append(name)
            file_dir_list.append(os.path.join(root, name))

    return file_list, file_dir_list


def list_shortcuts(file_list):
    """
    list_shortcuts creates a list of the raw shortcut strings the user would be typing in

    :param file_list:
    :return shortcut_list:
    :rtype list:
    """

    shortcut_list = list()

    for f in file_list:
        f = f.split(".")
        shortcut_list.append(f[0])

    return shortcut_list


def print_shortcuts(file_dir_list, shortcut_list):

    for file_dir in file_dir_list:
        index = file_dir_list.index(file_dir)
        print(f"Shortcut: {shortcut_list[index]}   - - -    Directory: {file_dir}")


if __name__ == "__main__":

    text_block_dir = 'Textblocks/'

    file_list = list_files(text_block_dir)

    shortcut_list = list_shortcuts(file_list)


