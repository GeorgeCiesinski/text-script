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
    Lists all files and subdirectories in the directory.

    :param directory:
    :return:
    """

    file_list = list()

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))

    print(file_list)


text_block_dir = 'Textblocks/'
list_subdirectories(text_block_dir)

list_files(text_block_dir)
