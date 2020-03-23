import os
import sys
sys.path.append(os.path.abspath('textscript'))

# from TextController import WordCatcher, KeyboardEmulator

"""
This testing is pending resolution of issue #59 on the repository. The above import is disabled to prevent the build
from failing. At this time, if you import WordCatcher or KeyboardEmulator, the pynput library tries to use X, which 
produces an error on Travis CI. 
"""

def test_basic():
    pass