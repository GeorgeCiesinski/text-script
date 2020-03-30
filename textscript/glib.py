"""
Contains non-class or miscellaneous functions, and Text-Script information
"""

import os


def get_version():
    """
    Current app version / / Ensure this is correct during updates

    :return current_version:
    :rtype string:
    """
    current_version = "1.3.1"

    return current_version


def help_text():
    """
    Contains the help text used by the program. This is located in one location so it is easier to edit.

    :return help_text:
    :rtype string:
    """

    help_text = """Help Menu:

How to make a shortcut:

1. Navigate to the program folder, and go to the Textblocks folder
2. Either navigate to an existing folder in Textblocks, or create a new one
3. Create a new text file here. The naming convention is #____.txt where ____ is the shortcut you will type
4. Open the text file and put your text block / signature / template in here
5. Click "Save As" and select the same text file, but change encoding to unicode

Note: Other formats may still work, but this is designed to read unicode text files.

To see this at any time, type: !help into a text input field.
To reload shortcuts, type: !reload
"""

    return help_text


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
            # Check if shortcut name is compatible
            if _shortcut_compatibility_check(name):
                # Append to _file_list and _file_dir_list if yes
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


def _shortcut_compatibility_check(_shortcut):
    """
    Checks if shortcut is formatted contains a second delimiter in the name. Return _is_compatible = False

    :param _shortcut:
    :rtype bool:
    """

    # Delimiter
    _shortcut_delimiter = "#"
    _command_delimiter = "!"

    _is_compatible = None

    # If the delimiter appears in the actual shortcut, return False
    if _shortcut_delimiter in _shortcut[1:] or _command_delimiter in _shortcut[1:]:

        _is_compatible = False

    else:

        _is_compatible = True

    return _is_compatible


def print_shortcuts(_file_dirs, _shortcuts):

    for _file_dir in _file_dirs:
        index = _file_dirs.index(_file_dir)
        print(f"Shortcut: {_shortcuts[index]}   - - -    Directory: {_file_dir}")


if __name__ == "__main__":

    pass
