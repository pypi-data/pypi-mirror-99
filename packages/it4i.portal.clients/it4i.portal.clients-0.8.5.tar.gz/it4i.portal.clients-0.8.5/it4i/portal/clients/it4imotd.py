#!/usr/bin/env python
"""
Shows IT4I messages of the day into formatted text or HTML page
"""

from textwrap import TextWrapper

import argparse
import random
import os
import re
import sys
import time
import dateutil.parser

from bs4 import BeautifulSoup
from chameleon.zpt.loader import TemplateLoader
from .logger import LOGGER
from .config import API_URL
from .jsonlib import jsondata

def render_text(jsonout, width):
    """
    print text-only MOTD
    """
    wrapper = TextWrapper(width=width,
                          replace_whitespace=False,
                          break_long_words=False,
                          break_on_hyphens=False)
    for item in jsonout:
        updated = True
        print >> sys.stdout
        mysearch = re.search(r'^(.*)\s(\([\d-]*\sto\s[\d-]*\)$)', item['title'])
        if mysearch:
            for title_line in wrapper.wrap(mysearch.group(1)):
                print >> sys.stdout, title_line.center(width).encode('utf-8')
            print >> sys.stdout, mysearch.group(2).center(width).encode('utf-8')
            updated = False
        else:
            print >> sys.stdout, item['title'].center(width).encode('utf-8')

        if updated:
            print >> sys.stdout, ('(%s)' % dateutil.parser.parse(item['updated_at']).strftime("%Y-%m-%d %H:%M:%S")).center(width)
        print >> sys.stdout
        item['content'] = re.sub(r'(<br ?/?>){1,}',
                                 '\n',
                                 item['messageBody'])
        soup = BeautifulSoup(item['content'], 'html.parser')
        for paragraph in soup.get_text().strip().split('\n'):
            print >> sys.stdout, wrapper.fill(paragraph.strip()).encode('utf-8')
        print >> sys.stdout

def render_html(jsonout, page_template):
    """
    print HTML-templated MOTD
    """
    pt_loader = TemplateLoader([os.path.dirname(page_template)],
                               auto_reload=True)
    template = pt_loader.load(page_template)
    print >> sys.stdout, template(items=jsonout).encode('utf-8')

def main():
    """
    main function
    """

    parser = argparse.ArgumentParser(description="""
The command shows IT4I messages of the day into formatted text or HTML page.""")
    parser.add_argument('-t', '--template',
                        action='store',
                        help="""
path to TAL / Zope Page Template, output will be formatted into HTML page""")
    parser.add_argument('-w', '--width',
                        default=78,
                        type=int,
                        action='store',
                        help="""
maximum line width (intended for text rendering, default of 78 columns)""")
    parser.add_argument('-c', '--cron',
                        action='store_true',
                        help="sleep from 10 up to 60 seconds prior to any actions")
    parser.add_argument('-m', '--message',
                        default='all',
                        action='store',
                        choices=['all', 'important', 'notice'],
                        help="select type of messages")
    arguments = parser.parse_args()

    if arguments.template is not None:
        if not os.path.isfile(arguments.template):
            LOGGER.error("Page template '%s' not found", arguments.template)
            sys.exit(1)

    remote = ('%s/motd/%s' % (API_URL, arguments.message))
    jsonout = jsondata(remote)

    if arguments.cron:
        time.sleep(random.randint(10, 60))
    if arguments.template is not None:
        render_html(jsonout, arguments.template)
    else:
        render_text(jsonout, arguments.width)

if __name__ == "__main__":
    main()
