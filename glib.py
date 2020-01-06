import os


def list_subdirectories(directory):

    directory_list = list()
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))

    print(directory_list)


text_block_dir = 'Textblocks/'
list_subdirectories(text_block_dir)
