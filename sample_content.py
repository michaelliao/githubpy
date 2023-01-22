#!/usr/bin/env python3
# -*-coding: utf8 -*-

'''
Get, upload, update and delete content of repo.

Export token first before run this script:

$ export GITHUB_TOKEN=ghp_xxx
'''

import os, json, time, base64, datetime
from github import GitHub, ApiConflictError, ApiNotFoundError

def main():
    # read token from env:
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print('could not read token from env.')
        exit(1)
    gh = GitHub(token, debug=True)
    user = 'michaelliao'
    repo = 'githubpy-test'
    path = 'test/café.txt'

    try:
        # get exist file:
        exist = gh.repos(user)(repo).contents(path).get()
        print_json(f'exist file: {path}', exist)
    except ApiNotFoundError as e:
        # file not exist, upload new file: https://docs.github.com/rest/repos/contents#create-or-update-file-contents
        exist = gh.repos(user)(repo).contents(path).put(
            {
                'message': 'upload new file',
                'committer': committer(),
                'content': file_content()
            }
        )
        print_json(f'created file: {path}', exist)

    sleep()
    try:
        # update exist file with conflict, because sha is invalid: https://docs.github.com/rest/repos/contents#create-or-update-file-contents
        gh.repos(user)(repo).contents(path).put(
            {
                'message': 'update file',
                'committer': committer(),
                'content': file_content(),
                'sha': '1000000000200000000030000000004000000000' # invalid sha
            }
        )
    except ApiConflictError as e:
        print(e.code, e.url, 'Conflict error.')

    sleep()
    # update exist file: https://docs.github.com/rest/repos/contents#create-or-update-file-contents
    updated = gh.repos(user)(repo).contents(path).put(
        {
            'message': 'update file',
            'committer': committer(),
            'content': file_content(),
            'sha': get_sha(exist)
        }
    )
    print_json(f'updated file: {path}', updated)

    sleep()
    # delete file: https://docs.github.com/rest/repos/contents#delete-a-file
    deleted = gh.repos(user)(repo).contents(path).delete(
        {
            'message': 'delete exist file',
            'committer': committer(),
            'sha': get_sha(updated)
        }
    )
    print_json(f'deleted file: {path}', deleted)

    # try upload without permission: https://docs.github.com/rest/repos/contents#create-or-update-file-contents
    try:
        gh.repos('torvalds')('linux').contents('test-upload-without-permission.txt').put(
            {
                'message': 'upload new file',
                'committer': committer(),
                'content': file_content()
            }
        )
    except ApiNotFoundError as e:
        print(e.code, e.url, 'No permission.')


def print_json(msg, obj):
    print(f'{msg}')
    print('----------------------------------------')
    print(json.dumps(obj, indent=2))
    print('----------------------------------------')


def sleep():
    time.sleep(1.5)


def get_sha(obj):
    if hasattr(obj, 'sha'):
        return obj.sha
    if hasattr(obj, 'content'):
        return obj.content.sha
    raise ValueError('object has no attribute of \'sha\'')


def file_content():
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = bytes('Hello world!\nUpdated at ' + dt, 'utf-8')
    b64 = base64.b64encode(content)
    return b64.decode('utf-8')


def committer():
    return {
        'name': 'Michael',
        'email': 'askxuefeng@gmail.com'
    }


if __name__ == '__main__':
    main()
