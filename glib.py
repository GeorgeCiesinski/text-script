"""
George's Library
Contains non-class methods for this program.
"""


import os


def list_subdirectories(directory):
    """
    Lists all subdirectories.

    :param directory:
    :return:
    """

    directory_list = list()

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))

    print(directory_list)


def list_files(directory):
    """
    Lists all files and subdirectories in the directory. Returns list

    :param directory:
    :return file_list:
    :rtype list:
    """

    file_list = list()
    file_dir_list = list()

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_list.append(name)
            file_dir_list.append(os.path.join(root, name))

    print(file_dir_list)

    return file_list, file_dir_list


def list_shortcuts(file_list):

    shortcut_list = list()

    for f in file_list:
        f = f.split(".")
        shortcut_list.append(f[0])

    return shortcut_list


if __name__ == "__main__":

    text_block_dir = 'Textblocks/'

    file_list = list_files(text_block_dir)

    shortcut_list = list_shortcuts(file_list)


