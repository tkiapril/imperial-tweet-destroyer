#!/usr/bin/env python3
'''
imperial-tweet-destroyer.py

A script for destroying a batch of tweets,
based on your Twitter archive

by tki, Distributed with MIT License

Prerequisites:
Python package PyYAML, birdy
config.yaml based on config.yaml.example

Target Python version > 3.4

Intended users:
Mostly myself, but anyone able to read the code may use it.

usage: python imperial-tweet-destroyer.py <data.js> [<data2.js>...]
'''

import json
import pathlib
import pprint
import sys

from birdy.twitter import UserClient, TwitterClientError,\
                          TwitterApiError, TwitterRateLimitError
import yaml


if len(sys.argv) < 2:
    sys.exit('see usage.')

with pathlib.Path('config.yaml').open('r') as f:
    config = yaml.load(f)

client = UserClient(
    config['consumer_key'],
    config['consumer_secret'],
    config['access_token'],
    config['access_token_secret']
)

for arg in sys.argv[1:]:
    print('Working on file: ' + arg)
    tweet_file = pathlib.Path(arg)
    if not tweet_file.is_file:
        sys.exit('file does not exist or is not a file.')

    try:
        with tweet_file.open('r') as f:
            tweet_json = f.read()
    except:
        sys.exit('Error on reading file: ' + arg)

    try:
        if tweet_json.find('=') < tweet_json.find('['):
            tweet_json = tweet_json[tweet_json.find('=')+1:].strip()
    except:
        sys.exit('Error on parsing file: ' + arg)

    try:
        tweets = json.loads(tweet_json)
    except:
        sys.exit('Error on loading file: ' + arg)

    index = 0

    try:
        for i in range(0, len(tweets)):
            index = i
            while True:
                try:
                    r = client.api.statuses\
                                  .destroy[tweets[i]['id_str']].post()
                    pprint.pprint(r.headers)
                    print(
                        'Removed id: {}, status: {}\n'
                        '(index {}, total {})'.format(
                            tweets[i]['id'],
                            tweets[i]['text'],
                            index,
                            len(tweets)
                        )
                    )
                    break
                except TwitterClientError:
                    pass
                except TwitterApiError:
                    if 'retweeted_status' in tweets[i]:
                        break
    except TwitterRateLimitError:
        sys.exit('Rate limited, index: {}'.format(index))
