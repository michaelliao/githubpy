import setuptools

import github

setuptools.setup(
    name = 'githubpy',
    version = github.__version__,
    description = 'Github REST API Python3 SDK',
    long_description = 'githubpy is a simple Python3 client for GitHub REST API.',
    author = 'Michael Liao',
    author_email = 'askxuefeng@gmail.com',
    url = 'https://github.com/michaelliao/githubpy',
    download_url = 'https://github.com/michaelliao/githubpy',
    py_modules = ['github'],
    python_requires = '>=3.5',
    install_requires = [],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
