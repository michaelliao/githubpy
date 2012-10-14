#!/usr/bin/env python
# -*-coding: utf8 -*-

'''
GitHub API Python Client.

Michael Liao (askxuefeng@gmail.com)
'''

import re, os, sha, time, hmac, base64, hashlib, urllib, urllib2, mimetypes

from datetime import datetime, timedelta, tzinfo
from StringIO import StringIO

def main():
    p = _Callable('')
    print str(p.repo('michaelliao')('githubpy').subscribers)
    print p.user.subscribers('michaelliao')('githubpy')

class GitHub(object):

    def __init__(self, username, password):
        self._auth = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))

class _Callable(object):

    def __init__(self, name):
        self._name = name

    def __call__(self, *args):
        if len(args)==0:
            return self
        name = '%s/%s' % (self._name, '/'.join(args))
        return _Callable(name)

    def __getattr__(self, attr):
        name = '%s/%s' % (self._name, attr)
        return _Callable(name)

    def __str__(self):
        return self._name

    __repr__ = __str__

if __name__ == '__main__':
    main()
