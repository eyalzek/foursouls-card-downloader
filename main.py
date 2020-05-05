#!/usr/bin/env python3

import os
import json
import shutil
import argparse
from logger import logger
from urllib import request
from html.parser import HTMLParser


class CardParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.name = None
        self.check_data = False
        self.image_url = None

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            try:
                img = [attr[1] for attr in attrs if attr[0] == 'src'][0]
                cname = [attr[1] for attr in attrs if attr[0] == 'class'][0]
                if cname == 'img-responsive':
                    self.image_url = img
            except IndexError:
                pass

        if tag == 'h2' and not self.name:
            self.check_data = True

    def handle_data(self, data):
        if self.check_data:
            self.name = data
            self.check_data = False


def parse_args():
    parser = argparse.ArgumentParser(
        description='Binding of Isaac Four Souls card downloader')
    parser.add_argument('-j', '--file', type=str, default='cards.json',
                        help='JSON file to dump data to')
    parser.add_argument('-s', '--start', type=int, default=70,
                       help='ID of first card in range')
    parser.add_argument('-e', '--end', type=int, default=790,
                       help='ID of last card in range')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    fetch = subparsers.add_parser('fetch', help='fetch card data (do not download)',
                       formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                       description='Fetch card data and dump it to a file. '
                       'This file needs to exist before downloading cards is possible')
    fetch.add_argument('-f', '--force', action='store_true',
                       help='ignore existing json file file')
    download = subparsers.add_parser('download', help='download cards',
                       description='Download card art, specify either \'--all\', '
                       'or multiple \'--card\' arguments')
    cards = download.add_mutually_exclusive_group(required=True)
    cards.add_argument('-a', '--all', action='store_true',
                       help='download all available cards')
    cards.add_argument('-c', '--card', action='append',
                       nargs='+', type=str, help='name of card to download')
    return parser.parse_args()


def get_card(cid):
    base_url = 'http://pop-life.com/foursouls'
    with request.urlopen('%s/card.php?id=%d' % (base_url, cid)) as resp:
        r = resp.read()
    p = CardParser()
    p.feed(r.decode())
    return {'name': p.name, 'src': '%s/%s' % (base_url, p.image_url.replace('./', ''))}

def fetch_cards(args):
    cards = []
    for i in range(args.start, args.end + 1):
        cards.append(get_card(i))
    with open(args.file, 'w') as f:
        f.write(json.dumps(cards))

def need_fetch(args):
    if not os.path.exists(args.file):
        return True
    if args.command == 'fetch':
        if args.force:
            return True
        else:
            logger.info('\'fetch\' specified, but \'%s\' already exists -'
                        ' pass \'--force\' to override' % args.file)
    return False

def match_cards(args):
    with open(args.file, 'r') as f:
        cards = json.loads(f.read())
    if args.all:
        return cards
    matched = []
    for c in args.card:
        matched += [x for x in cards if ' '.join(c).lower() in x['name'].lower()]
    return matched

def download(cards):
    if not os.path.exists('cards'):
        os.makedirs('cards')
    for c in cards:
        filename = 'cards/%s.png' % c['name']
        if os.path.exists(filename):
            logger.info('%s already exists, skipping' % filename)
            continue
        logger.info('Getting %s...' % c['src'])
        with request.urlopen(c['src']) as resp:
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(resp, out_file)

def main():
    args = parse_args()
    fetch = need_fetch(args)
    if fetch:
        fetch_cards(args)
    if args.command == 'download':
        cards = match_cards(args)
        logger.info('Matched cards: %a' % [c['name'] for c in cards])
        download(cards)


if __name__ == '__main__':
    main()
