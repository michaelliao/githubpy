#!/usr/bin/env python3
# -*-coding: utf8 -*-

'''
Get, create, update issues.

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

    # get all issues: https://docs.github.com/rest/issues/issues#list-repository-issues
    all = gh.repos(user)(repo).issues.get(state='all', page=1, per_page=100)
    print_json('all issues:', all)

    sleep()

    # get open issues: https://docs.github.com/rest/issues/issues#list-repository-issues
    opens = gh.repos(user)(repo).issues.get(state='open', page=1, per_page=100)
    print_json('open issues:', opens)

    for oi in opens:
        sleep()

        if oi.comments < 1:
            # make a comment: https://docs.github.com/rest/issues/comments#create-an-issue-comment
            comment = gh.repos(user)(repo).issues(oi.number).comments.post(
                {
                    'body': 'Me too'
                }
            )
            print_json('comment:', comment)
        else:
            # update an issue: https://docs.github.com/rest/issues/issues#update-an-issue
            closed = gh.repos(user)(repo).issues(oi.number).patch(
                {
                    'state': 'closed'
                }
            )
            print_json('closed issue:', closed)

    sleep()
    # create an issue: https://docs.github.com/rest/issues/issues#create-an-issue
    issue = gh.repos(user)(repo).issues.post(
        {
            'title': 'Found a bug at ' + now(),
            'body': 'Having a problem with githubpy.',
            'labels': ['bug', 'question'],
            'assignees': ['michaelliao']
        }
    )
    print_json(f'created issue:', issue)


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
