# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Planned Updates]
- Check for duplicate shortcuts & handle
- Ability to correct shortcut typos using arrow keys instead of just backspace
- GUI support

## [Unreleased] - Date TBA
# Added
- Last clipboard item is preserved during textblock paste
- OSX is now supported. Text-script identifies your OS and uses the correct paste shortcut. 
# Changed
- Improved testing so that modules are correctly imported now. 

## [1.3.1] - 2020-03-12
#Added
- Implemented Continuous Integration 
- Added command delimiter (!)
- Added functions to predict the codec and decode textblocks with greater accuracy. This should
resolve bugs encountered when using non unicode textblocks.
- Added better compatibility check for textblock naming convention.
#Changed
- Updated logging to better capture errors which occur during textblock decoding
- Moved commands from shortcut delimiter (#) to command delimiter (!)

## [1.3.0] - 2020-02-21
# Changed
- Added reload function which adds shortcuts without restarting the program
- Added mechanism to update config file and repair broken sections
- Added better exception handling for issues in config file
- Added contributions file
- Moved source files into textscript subdirectory and refactored code
- Added notifications for added or removed textblocks
- Reorganized classes so that methods make more sense
- Renamed internal use methods according to PEP-8
- Renamed Settings.py as ConfigUtils.py as this is more accurate

## [1.2.0] - 2020-01-23
### Added
- Support for three directories: default, local, and remote
- Usage statistic printout during program start

## [1.1.0] - 2020-01-17
### Added
- Statistics tracking for shortcuts used, total shortcut characters typed, and total textblock characters pasted
- Help and Exit commands have been added

## [1.0.0] - 2020-01-16
### Added
- App prints all of the shortcuts and directories during start
### Changed
- Debugging print lines removed
- Better logging to track potential issues

## [0.0.1] - 2020-01-14
### Added
- Created first basic version
- Functional textblock printing and shortcut recognition
- Released as alpha for testing purposes