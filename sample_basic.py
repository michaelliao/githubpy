#!/usr/bin/env python3
# -*-coding: utf8 -*-

'''
Get user, repo info.

Export token first before run this script:

$ export GITHUB_TOKEN=ghp_xxx
'''

import os, json, time, datetime
from github import GitHub

def main():
    # read token from env:
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print('could not read token from env.')
        exit(1)
    gh = GitHub(token, debug=True)
    user = 'michaelliao'
    repo = 'githubpy-test'

    # get a user: https://docs.github.com/rest/users/users#get-a-user
    u = gh.users(user).get()
    print_json('user:', u)

    sleep()

    # get repositories for a user: https://docs.github.com/rest/repos/repos#list-repositories-for-a-user
    repos = gh.users(user).repos.get(sort='updated', page=1, per_page=10)
    print_json('repos:', repos)

    for rp in repos:
        sleep()
        # list repository contributors: https://docs.github.com/rest/repos/repos#list-repository-contributors
        cs = gh.repos(user)(rp.name).contributors.get()
        print_json(f'contributors of repo {rp.name}', cs)

        if rp.name == repo:
            # update a repository: https://docs.github.com/rest/repos/repos#update-a-repository
            updated = gh.repos(user)(rp.name).patch(
                {
                    'description': 'Test repo for githubpy, updated at ' + now()
                }
            )
            print_json('updated repo:', updated)


def print_json(msg, obj):
    print(f'{msg}')
    print('----------------------------------------')
    print(json.dumps(obj, indent=2))
    print('----------------------------------------')


def sleep():
    time.sleep(1.5)


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


if __name__ == '__main__':
    main()
