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

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))

    return file_list

def categorizer(file_list):
    """
    Creates internal list variable for categories

    :param file_list:
    :return:
    """

    pass

#TODO: Make a regex to recognize 'Textblocks/#hello.txt' & 'Textblocks/hello.txt'

#TODO: Make a regex to recognize 'Textblocks/Signatures\\#sig.txt' & 'Textblocks/Signatures\\sig.txt'

text_block_dir = 'Textblocks/'
list_subdirectories(text_block_dir)

list_files(text_block_dir)
