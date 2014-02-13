from distutils.core import setup
import sys

import github

kw = dict(
    name = 'githubpy',
    version = github.__version__,
    description = 'Github v3 API Python SDK',
    long_description = open('README', 'r').read(),
    author = 'Michael Liao',
    author_email = 'askxuefeng@gmail.com',
    url = 'https://github.com/michaelliao/githubpy',
    download_url = 'https://github.com/michaelliao/githubpy',
    py_modules = ['github'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

setup(**kw)
