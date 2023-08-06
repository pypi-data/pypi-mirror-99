# -*- coding: utf-8 -*-
"""cliquery utility functions.

   Functions include:
   Web requests and requests caching
   Text processing
   URL processing
   User input and sanitation
   Miscellaneous
"""

from __future__ import absolute_import
import glob
import random
import os
import sys

import lxml.html as lh
import requests
from six import PY2, iteritems
from six.moves.urllib.parse import quote_plus
from six.moves.urllib.request import getproxies


USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) '
               'Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) '
               'Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) '
               'Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) '
               'AppleWebKit/536.5 (KHTML, like Gecko) '
               'Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) '
               'AppleWebKit/536.5 (KHTML, like Gecko) '
               'Chrome/19.0.1084.46 Safari/536.5')


XDG_CACHE_DIR = os.environ.get('XDG_CACHE_HOME',
                               os.path.join(os.path.expanduser('~'), '.cache'))
CACHE_DIR = os.path.join(XDG_CACHE_DIR, 'cliquery')
CACHE_FILE = os.path.join(CACHE_DIR, 'cache{0}'.format('' if PY2 else '3'))

# Web requests and requests caching functions
#


def get_proxies():
    """Get available proxies to use with requests library."""
    proxies = getproxies()
    filtered_proxies = {}
    for key, value in iteritems(proxies):
        if key.startswith('http://'):
            if not value.startswith('http://'):
                filtered_proxies[key] = 'http://{0}'.format(value)
            else:
                filtered_proxies[key] = value
    return filtered_proxies


def get_resp(url):
    """Get webpage response as an lxml.html.HtmlElement object."""
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        request = requests.get(url, headers=headers, proxies=get_proxies())
        return lh.fromstring(request.content)
    except Exception:
        sys.stderr.write('Failed to retrieve {0}.\n'.format(url))
        raise


def get_raw_resp(url):
    """Get webpage response as a str object."""
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        request = requests.get(url, headers=headers, proxies=get_proxies())
        return request.text.encode('utf-8') if PY2 else request.text
    except Exception:
        sys.stderr.write('Failed to retrieve {0} as str.\n'.format(url))
        raise


def enable_cache():
    """Enable requests library cache."""
    try:
        import requests_cache
    except ImportError as err:
        sys.stderr.write('Failed to enable cache: {0}\n'.format(str(err)))
        return
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    requests_cache.install_cache(CACHE_FILE)


def clear_cache():
    """Clear requests library cache."""
    for cache in glob.glob('{0}*'.format(CACHE_FILE)):
        os.remove(cache)

# Text processing functions
#


def remove_whitespace(text):
    """Remove unnecessary whitespace while keeping logical structure

       Keyword arguments:
       text -- text to remove whitespace from (list)

        Retain paragraph structure but remove other whitespace,
        such as between words on a line and at the start and end of the text.
    """
    clean_text = []
    curr_line = ''
    # Remove any newlines that follow two lines of whitespace consecutively
    # Also remove whitespace at start and end of text
    while text:
        if not curr_line:
            # Find the first line that is not whitespace and add it
            curr_line = text.pop(0)
            while not curr_line.strip() and text:
                curr_line = text.pop(0)
            if curr_line.strip():
                clean_text.append(curr_line)
        else:
            # Filter the rest of the lines
            curr_line = text.pop(0)
            if text:
                if curr_line.strip():
                    clean_text.append(curr_line)
                else:
                    # If the current line is whitespace then make sure there is
                    # no more than one consecutive line of whitespace following
                    if not text[0].strip():
                        if len(text) > 1 and text[1].strip():
                            clean_text.append(curr_line)
                    else:
                        clean_text.append(curr_line)
            else:
                # Add the final line if it is not whitespace
                if curr_line.strip():
                    clean_text.append(curr_line)

    # Now filter each individual line for extraneous whitespace
    cleaner_text = []
    clean_line = ''
    for line in clean_text:
        clean_line = ' '.join(line.split())
        if not clean_line.strip():
            clean_line += '\n'
        cleaner_text.append(clean_line)
    return cleaner_text


def split_title(title, delim):
    """Return largest title piece."""
    largest_len = 0
    largest_piece = None
    piece_len = 0

    for piece in title.split(delim):
        piece_len = len(piece)
        if piece_len > largest_len:
            largest_len = piece_len
            largest_piece = piece
    return largest_piece or title


def get_title(resp):
    """Extract title from webpage response."""
    title = resp.xpath('//title/text()')
    if not title:
        return ''
    else:
        title = title[0]

    # Split title by common delimeters
    common_delim = ['|', '-', '–', '»', ':']
    for delim in common_delim:
        if delim in title:
            title = split_title(title, delim)
            break
    return title


def get_text(resp):
    """Return text that is not within a script or style tag."""
    return resp.xpath('//*[not(self::script) and not(self::style)]/text()')

# URL processing functions
#


def add_scheme(url):
    """Add scheme to URL."""
    if not check_scheme(url):
        return 'http://{0}'.format(url)
    return url


def check_scheme(url):
    """Check URL for a scheme."""
    if url and (url.startswith('http://') or url.startswith('https://')):
        return True
    return False


def add_schemes(urls):
    """Append scheme to URLs if not present."""
    if isinstance(urls, list):
        return [x if check_scheme(x) else add_scheme(x) for x in urls]
    if check_scheme(urls):
        return urls
    return add_scheme(urls)

# User input and sanitation functions
#


def clean_query(args, query):
    """Split the query or replace it's special characters if necessary"""
    if args['bookmark']:
        return query
    elif args['open'] and not (args['search'] or args['wolfram'] or
                               args['first']):
        # The query consists of links to open directly
        return query.split()
    else:
        # Replace special characters with hex encoded escapes
        return quote_plus(query)


def check_input(user_input, num=False, empty=False):
    """Check user input for empty, a number, or for an exit signal"""
    if isinstance(user_input, list):
        user_input = ''.join(user_input)

    try:
        u_inp = user_input.lower().strip()
    except AttributeError:
        u_inp = user_input

    # Check for exit signal
    if u_inp in ('q', 'quit', 'exit'):
        sys.exit()

    if num:
        return is_num(user_input)
    elif empty:
        return not user_input
    return True


def confirm_input(user_input):
    """Check user input for yes, no, or an exit signal"""
    if isinstance(user_input, list):
        user_input = ''.join(user_input)

    try:
        u_inp = user_input.lower().strip()
    except AttributeError:
        u_inp = user_input

    # Check for exit signal
    if u_inp in ('q', 'quit', 'exit'):
        sys.exit()
    if u_inp in ('y', 'yes'):
        return True
    return False

# Miscellaneous functions
#


def is_num(num):
    """Return whether num can be an int"""
    try:
        num = int(num)
        return True
    except ValueError:
        return False


def in_range(length, start=None, end=None):
    """Return if start and end are between [0, length)"""
    if start is None and end is None:
        return False
    elif start is not None and end is None:
        end = start
    elif end is not None and start is None:
        start = end

    if not isinstance(start, int) and is_num(start):
        start = int(start)
    if not isinstance(end, int) and is_num(end):
        end = int(end)
    return start >= 0 and end < length


def reset_flags(args):
    """Return a dictionary with all bool flags set to False"""
    return {k: False if isinstance(v, bool) else v for k, v in iteritems(args)}


def get_lookup_flags(args):
    """Return a dictionary with keys equal to first letter of their values"""
    return {k[0]: k for k, v in iteritems(args) if isinstance(v, bool)}
