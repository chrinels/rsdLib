""" individualised library module
    commonly required functions import via rgrLib
                                                 rgr26mar17
"""
from __future__ import print_function
import os, sys

# ------------------ commnad line helpers -----------------
def pwd():
    """show the current directory name"""
    print(os.path.abspath(os.path.curdir))

def m_path():
    """show the search path used by python to import modules"""
    print(os.linesep.join(sys.path))

def s_path():
    """show the seach path used by the shell to find executables"""
    print(os.linesep.join(os.environ['PATH'].split(';')))

def changeExt(file_name, new_ext, override=False):
    """return a new file.extension, override True to change anyexisting ext"""
    (root, ext) = os.path.splitext(file_name)
    _separator = os.path.extsep
    if override or len(ext)==0 or ext==_separator:
        if new_ext.find(_separator)==-1:
            ext = _separator + new_ext
        else:
            ext = new_ext
    return root+ext

# from StackOverflow:
# https://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
import ctypes

def is_hidden(filepath):
    """return whether a file is hidden for the os in use"""
    name = path.basename(path.abspath(filepath))
    return name.startswith('.') or has_hidden_attribute(filepath)

def has_hidden_attribute(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result
