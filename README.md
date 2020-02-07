# >text-script

![Python Version](https://img.shields.io/badge/Python-3.7-blue)
![License Information](https://img.shields.io/github/license/GeorgeCiesinski/text-script)

![Dependencies](https://img.shields.io/requires/github/GeorgeCiesinski/text-script)
![Open Issues](https://img.shields.io/github/issues/GeorgeCiesinski/text-script)

An app that allows users to save shortcuts and textblocks. Typing a shortcut automatically replaces said shortcut with the content of the saved textblock. This app runs in the background and improves typing efficiency.

## Motivation
I came up with this idea when I discovered there was a lack of quality open source applications to fulfill this function. As a tech support agent, I find myself repeatedly copying the same blocks of text, such as signatures, instructions, and templates, and pasting them into emails. This is a common task in any tech support role, so I wanted to write an app to help my colleagues, and anybody else working in a similar role. 

## Built With
- Pynput
- Pyperclip

## Prerequisites
- Python 3.8 (I do not know if versions below 3.6 will work)
- Dependencies from requirements.txt

## Installing

At this time, the program is still in early development, so I recommend always downloading the latest version as it will usually contain fixes for large bugs or issues. 

### Executable installation steps

1. Go to the releases section of this repository.
2. Download the top file in the latest release.
3. Extract the text-script folder within this zip file. The whole folder is needed for the installation.
4. Open the Config folder, and the config.ini file within this. Here, you can link the local or remote directories you will use to store your textblocks. 
5. Create your shortcuts and textblocks in one of these directories. 
6. Click text-script.exe to run the program. You may need to allow the program to run.

### Source Code

1. Download or clone the repository.
2. Install the dependencies from requirements.txt (virtual environment is recommended).
3. Run the app.py file. 
4. Optionally, follow steps 4 & 5 from teh Executable Installation Steps to configure text-script.

## Screenshots
TBA

## Planned future updates
- Save whatever the latest clipboard item is and replace it after shortcut is used. Currently the last textblock used fills the last clipboard spot
- Create #reload command which reloads the shortcut list with all the latest updates
- A notification should advise users of any added or removed textblocks every time the app is ran
- Optional usage tracking to advise the user which textblocks see the most use and which do not

## Features

### Save Shortcuts & Textblocks
text-script lets you create shortcuts which are used to quickly and easily recall textblocks later. Once you have configured the textblock directory, you can create unicode text files containing your textblocks. Within this directory, you simply need to name them #_______.txt where the blank is the shortcut you will type, and save the file using the unicode encoding. Future plans for text-script include creating a GUI which streamlines the shortcut/textblock creation process.

### Supports Local and Remote Shortcuts
text-script allows both local and remote shortcuts to be used. Remote shortcuts can be created by a manager or supervisor and can be shared with the whole team on the network drive. While using these remote shortcuts, you can also create your own local shortcuts that only you can see and use.

### Runs in the background
This application runs in the background and does not need to be maximized or in focus. Simply starting the app and minimizing it is enough for it to recognize your shortcuts. 

### Textblock directory can contain many subdirectory levels
It is possible to make folders within the textblock directory to better organize your textblocks. Even these folders can contain more folders so that a complex organizational system is possible. 

### Privacy
text-script is being designed specifically with privacy in mind. As I intend for this application to be used free of charge by any individual or corporation, it is important to me that this application does not collect any private data. The contents of the textblocks are stored locally or within the user's network, and text-script does not duplicate or send this information anywhere. 

Throughout the development of text-script, I will always keep privacy in mind and will continue to strengthen the capability of text-script to remain anonymous and private. If you have any concerns about this, please feel free to open an issue so that any potential risk can be swiftly resolved. 

### Logs
text-script contains anonymous logging capabilities which generate up to six log files. A new log file is created whenever text-script is started, or whenever the current log file becomes too large. These logs may help to resolve any bugs that you experience while using text-script. 

Special care has been taken to keep the logs as anonymous as possible. The log files contain only program flow debugging messages, and only track characters that text-script believes are part of a shortcut. Specifically, whenever the delmiter (# key) is pressed, text-script logs the keys entered until space, tab, or enter is perssed, which indicates the shortcut is complete. Outside of the shortcut, no other keys are enterred into the logs, and neither are the contents of your textblocks. Despite limiting the effectiveness of the logs, this program is being written primarily with privacy in mind.

The logs are manually created and have to be manually provided when bugs are encountered. You can find these logs in the Logs/ folder within the text-script directory. Simply zip the contents of this folder, or the specific log file in question, and create a new issue if one doesn't exist for the bug you encountered. 

## Credits
George Ciesinski (Lead Developer)

## License
TBA
