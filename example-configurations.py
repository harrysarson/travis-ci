#!/usr/bin/env python3
import argparse
import enum
import fileinput
import re
import subprocess
import urllib.request

BRANCH_PREFIX = 'example-ci'
USER = 'harrysarson'

parser = argparse.ArgumentParser(description='Update configuration table')
parser.add_argument('--readme',
                    metavar='FILE',
                    nargs=1,
                    help='update README file')
parser.add_argument('--run_ci',
                    metavar='TOKEN',
                    nargs=1,
                    help='re run all examples in CI')


class State(enum.Enum):
    BEFORE = enum.auto()
    DURING = enum.auto()
    AFTER = enum.auto()


def print_table(examples):
    print('')
    print('| Name | Status | Configuration file |')
    print('| ---- | ------ | ------------------ |')
    for example in examples:
        with urllib.request.urlopen(
                'https://raw.githubusercontent.com/{}/travis-ci/{}/{}/.travis.yml'
                .format(USER, BRANCH_PREFIX, example)) as response:

            assert response.getcode() == 200
            config = response.read().decode('utf-8').strip()
            badge_url = 'https://travis-ci.com/{}/travis-ci.svg?branch={}%2F{}'.format(
                USER, BRANCH_PREFIX, example)
            print('| {} | {} | {} |'.format(
                example.replace('-', ' '),
                '[![Build Status]({})](https://travis-ci.com/{}/travis-ci/branches)'
                .format(badge_url, USER),
                '<pre>{}</pre>'.format(config.replace('\n', '<br/>'))))


def run_ci(examples, token):
    for example in examples:
        body = """{{
            "request": {{
                "branch":"{}/{}"
            }}
        }}""".format(BRANCH_PREFIX, example)

        request = urllib.request.Request(
            'https://api.travis-ci.com/repo/{}%2Ftravis-ci/requests'.format(
                USER),
            data=bytes(body, 'utf-8'),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Travis-API-Version": "3",
                "Authorization": "token {}".format(token),
            },
            origin_req_host=None,
            unverifiable=False,
            method='POST')
        with urllib.request.urlopen(request) as response:
            assert (response.getcode() // 100) * 100 == 200


def update_readme(examples, file):
    with fileinput.FileInput(args.readme[0], inplace=True) as file:
        state = State.BEFORE
        for line in file:
            if state is State.BEFORE:
                print(line, end='')
                if line.startswith('## Example configurations'):
                    print_table(examples)
                    state = State.DURING
            elif state is State.DURING:
                if line.startswith('##'):
                    print(line, end='')
                    state = State.AFTER
            else:
                assert state == State.AFTER
                print(line, end='')


args = parser.parse_args()

git_remote_branches = subprocess.run([
    'git', 'ls-remote', '--exit-code',
    'https://github.com/{}/travis-ci'.format(USER)
],
                                     capture_output=True,
                                     check=True,
                                     encoding='utf-8')

assert git_remote_branches.stderr == ''

examples = list(
    map(
        lambda m: m.group(1),
        filter(
            lambda s: s is not None,
            map(lambda s: re.search(r'^.*/{}/(.*)$'.format(BRANCH_PREFIX), s),
                git_remote_branches.stdout.splitlines()))))

assert len(examples) > 0

if args.readme is not None:
    update_readme(examples, args.readme[0])

if args.run_ci is not None:
    run_ci(examples, args.run_ci[0])
