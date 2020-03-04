#!/usr/bin/env python3

""" Simple liveblog tracker of nos.nl """

# =========================================================================== #
# File   : nos-liveblog-tracker.py                                            #
# Purpose: Displaying the headlines from the nos liveblog                     #
#                                                                             #
# Author : Harald van der Laan                                                #
# Date   : 2020-03-04                                                         #
# Version: v2.1.0                                                             #
# =========================================================================== #
# Changelog:                                                                  #
# - v2.1.0: Version number bump for better versioning   (Harald van der Laan) #
# - v2.0.2: Changed code for getting liveblog url       (Harald van der Laan) #
# - v2.0.1: Update with daemon functionality            (Harald van der Laan) #
# - v2.0.0: Rewritten code to python3 script            (Harald van der Laan) #
# - v1.x.x: Legacy shell script not supported any more  (Harald van der laan) #
# =========================================================================== #
# Copyright © 2020 Harald van der Laan                                        #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining       #
# a copy of this software and associated documentation files (the "Software") #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included     #
# in all copies or substantial portions of the Software.                      #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,             #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES             #
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.   #
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, #
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,               #
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE  #
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                               #
# =========================================================================== #

import sys
import re
import time
import subprocess
import argparse

import requests
import bs4


def get_args():
    """ function for getting commandline arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--daemon', action='store_true',
                        help="Draai script als daemon")
    parser.add_argument('-u', '--url', help="URL van liveblog")

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


def main(args):
    print('*'*60)
    print('NOS liveblog tracker v2.1.0 - by: Harald van der Laan')
    print('*'*60)
    print()

    links = get_liveblogs()

    if args.url:
        headlines = get_live_data(args.url)
    else:
        if links:
            headlines = get_live_data(links[0])
        else:
            print('Er is op dit moment geen active liveblog op nos.nl.')
            sys.exit(127)

    for line in headlines:
        print(line)


if __name__ == "__main__":
    ARGS = get_args()

    if ARGS.daemon:
        while True:
            try:
                subprocess.Popen('clear', shell=True)
                time.sleep(.5)
                main(ARGS)
                time.sleep(60)
            except KeyboardInterrupt:
                sys.exit(0)
    else:
        main(ARGS)
        sys.exit(0)
