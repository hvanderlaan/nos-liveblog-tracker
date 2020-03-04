#!/usr/bin/env python3

""" Simple liveblog tracker of nos.nl """

import sys
import re
import argparse

import requests
import bs4


def get_args():
    """ function for getting commandline arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="URL of liveblog")

    return parser.parse_args()


def get_liveblogs():
    """ Dunction for getting liveblogs """
    links = []
    html = requests.get('https://nos.nl')
    soup = bs4.BeautifulSoup(html.text, 'html.parser')

    for link in soup.findAll('a', attrs={'href': re.compile("^/liveblog/")}):
        links.append('https://nos.nl' + link.get('href'))

    return links


def get_live_data(url):
    """ Function for getting liveblog data """
    html = requests.get(url)

    data = bs4.BeautifulSoup(html.text, 'html.parser')
    headlines = data.findAll('h2', {'class': ['js-liveblog-update-title']})
    headlines = re.sub('<[^>]+>', '', str(headlines))
    headlines = re.sub('\[', ' ', str(headlines))
    headlines = re.sub('\]', '', str(headlines))
    headlines = headlines.split(',')

    return headlines


def main():
    args = get_args()

    print('*'*60)
    print('NOS liveblog tracker v2.0 - by: Harald van der Laan')
    print('*'*60)
    print()

    links = get_liveblogs()

    if args.url:
        headlines = get_live_data(args.url)
    else:
        if links:
            if len(links) == 1:
                headlines = get_live_data(links[0])
            else:
                counter = 0
                for link in links:
                    print(f'{counter}. {link}')
                    counter = counter + 1

                entry = input('geeft een liveblog numer op: ')
                headlines = get_live_data(links[int(entry)-1])
        else:
            print('Er is op dit moment geen active liveblog op nos.nl.')
            sys.exit(127)

    for line in headlines:
        print(line)


if __name__ == "__main__":
    main()
    sys.exit(0)
