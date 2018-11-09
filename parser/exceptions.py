#!/usr/bin/python3

class WikiError(Exception):
    """Base class for exceptions in this module"""
    def __init__(self, msg):
        super(WikiError, self).__init__()
        self.msg = msg
        