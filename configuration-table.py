#!/usr/bin/env python3
import argparse
import enum
import fileinput
import re
import subprocess
import urllib.request

USER = 'harrysarson'

parser = argparse.ArgumentParser(description='Update configuration table')
parser.add_argument('file', metavar='FILE', help='README file to update')

args = parser.parse_args()

git_remote_branches = subprocess.run([
    'git', 'ls-remote', '--exit-code',
    'https://github.com/{}/travis-ci'.format(USER)
],
                                     capture_output=True,
                                     check=True,
                                     encoding='utf-8')

assert git_remote_branches.stderr == ''


class State(enum.Enum):
    BEFORE = enum.auto()
    DURING = enum.auto()
    AFTER = enum.auto()


def print_table():
    examples = map(
        lambda m: m.group(1),
        filter(
            lambda s: s is not None,
            map(lambda s: re.search(r'^.*/example-ci/(.*)$', s),
                git_remote_branches.stdout.splitlines())))

    print('')
    print('| Name | Status | Configuration file |')
    print('| ---- | ------ | ------------------ |')
    for example in examples:
        config = urllib.request.urlopen(
            'https://raw.githubusercontent.com/{}/travis-ci/example-ci/{}/.travis.yml'
            .format(USER, example)).read().decode('utf-8').strip()
        badge_url = 'https://travis-ci.com/{}/travis-ci.svg?branch=example-ci%2F{}'.format(
            USER, example)
        print('| {} | {} | {} |'.format(
            example.replace('-', ' '),
            '[![Build Status]({})](https://travis-ci.com/{}/travis-ci/branches)'
            .format(badge_url, USER),
            '<pre>{}</pre>'.format(config.replace('\n', '<br/>'))))


with fileinput.FileInput(args.file, inplace=True) as file:
    state = State.BEFORE
    for line in file:
        if state is State.BEFORE:
            print(line, end='')
            if line.startswith('## Example configurations'):
                print_table()
                state = State.DURING
        elif state is State.DURING:
            if line.startswith('##'):
                print(line, end='')
                state = State.AFTER
        else:
            assert state == State.AFTER
            print(line, end='')
