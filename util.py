#!/usr/bin/python

import datetime
import time
import sys

class Utilities:
    @staticmethod
    def is_file(fp):
        try:
            file = open(fp, "r", 1)
        except IOError:
            return False
        file.close()
        return True

    @staticmethod
    def open_file(fp):
        try:
            file = open(fp, "r", 1)
        except IOError:
            Utilities.log("File '%s' cannot be opened", (fp), sys.stderr)
            return None
        return file
        
    @staticmethod
    def log(format, string_list = (), file = sys.stdout):
        time_stamp = ts = time.time()
        time_string = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        if (string_list != ""):
            file.write(time_string + ": " + format % string_list + "\n" )
        else:
            file.write(time_string + ": " + format + "\n" )
        
    @staticmethod
    def strip_white_space(string):
        ret = string.rstrip()
        ret = ret.lstrip()
        return ret
        
    # If a string has single or double quotes around it, remove them.
    # If a matching pair of quotes is not found, return the string unchanged.
    @staticmethod
    def dequote(s):
        # "(s[0] == s[-1])" makes sure the pair of quotes match.
        if s.startswith( ("'", '"') ) and s.endswith( ("'", '"') ) and (s[0] == s[-1]):
            s = s[1:-1]
        return s



