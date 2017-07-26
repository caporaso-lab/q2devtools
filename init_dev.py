#!/usr/bin/env python

import os
import subprocess
import sys

import requests


def main(username):
    r = requests.get('https://api.github.com/orgs/qiime2/repos')
    response = r.json()

    for repo in response:
        repo_name = repo.get('name')
        repo_url = repo.get('svn_url')
        repo_ssh = repo.get('ssh_url')

        user_url = repo_url.replace('.com/qiime2/',
                                    '.com/{}/'.format(username))
        if requests.get(user_url).status_code != 200:
            print('No user fork found for {}.\n'.format(repo_name))
            continue

        user_url = repo_ssh.replace(':qiime2/',
                                    ':{}/'.format(username))
        if not os.path.exists(repo_name):
            # --progress was required, as omitting it and PIPE-ing would for
            # some reason swallow the repo. It would clone/show up and once
            # "complete" the directory would disappear.
            print('Cloning {}...'.format(repo_name))
            subprocess.run(['git', 'clone', user_url, '--progress'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print('Adding upstream...')
            subprocess.run(
                '(cd {} && git remote add upstream {})'.format(repo_name,
                                                               repo_ssh),
                shell=True)
            print('Successfully initialized {}\n'.format(repo_name))
        else:
            print('{} already exists.\n'.format(repo_name))


if __name__ == '__main__':
    try:
        username = sys.argv[1].strip()
    except IndexError:
        print('Usage: python init_dev.py USERNAME')
        sys.exit(1)

    main(username)
