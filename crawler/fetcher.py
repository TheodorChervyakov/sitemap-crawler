"""
    Copyright 2018 Fedor Chervyakov

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import requests
from requests.exceptions import HTTPError, ReadTimeout
from lxml import etree

import itertools
import re
import sys
import logging

"""
Initializing logging here.
"""
_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=_format)

logger = logging.getLogger(__name__)

# Precompiled regex patterns
sitemap_pattern = re.compile('sitemap: ([\w.\:\-/]+\.xml/?)', re.IGNORECASE)
crawl_delay_pattern = re.compile('crawl\-delay: ([\d.]+)', re.IGNORECASE)

# Namespace used when parsing sitemaps
xml_namespaces = {'sitemap': "http://www.sitemaps.org/schemas/sitemap/0.9"}


def get_robots(url, timeout=15):
    """
    Retrieve robots.txt from the specified website
    and return its contents as a string

    Args:
        url (str): base link to the target website
        timeout (float): timeout value in seconds (default 15)

    Returns:
        str: text contents of robots.txt
    """
    # Building link to robots.txt
    if url[-1] != '/':
        url += '/'
    robots_url = url + 'robots.txt'

    logger.info('Fetching robots.txt from {0}'.format(robots_url))
    # Fetching robots.txt
    try:
        r = requests.get(robots_url, timeout=timeout)
        r.raise_for_status()
        logger.debug(r.text)
        return r.text
    except HTTPError:
        logger.warning('Request for {0} FAILED with code {1}'
                       .format(robots_url, r.status_code))
        raise
    except ReadTimeout:
        logger.warning('Request for {0} TIMEOUTed after {1} seconds.'
                       .format(robots_url, timeout))
        raise
    except Exception:
        logger.error('An unexpected error occured in get_robots',
                     exc_info=True)
        raise


def parse_robots(robots_string):
    """
    Parse robots.txt and return all sitemap entries and crawl-delay's value.

    Args:
        robots_string (str): robots.txt contents as a string

    Returns:
        dict: {sitemaps : list of sitemaps (empty list if none found),
               crawl-delay : crawl delay in seconds (None if not found)}
    """
    if robots_string is None:
        raise TypeError('The robots.txt is of None type!')
    elif len(robots_string) is 0:
        raise ValueError('The robots.txt is empty!')

    params = dict()
    # Reading sitemap entries
    matches = sitemap_pattern.findall(robots_string)
    params['sitemaps'] = set(matches)

    # Reading crawl-delay
    c = crawl_delay_pattern.search(robots_string)
    if c:
        params['crawl-delay'] = float(c.group(1))
    else:
        params['crawl-delay'] = None

    return params


def parse_sitemap(sitemap_url):
    """
    Fetch sitemap, then parse it and return list of links from it.

    If fetched sitemap is actually sitemapindex, this function calls
    itself on every link in the sitemapindex, and returns list of links
    from all urlsets in the sitemapindex. If fetched sitemap is
    urlset it returns all links from the urlset.
    
    Supported sitemap format is XML (not gzipped).

    Args:
        sitemap_url (str): link to the sitemap

    Returns:
        list: encountered links
    """
    # Checking if sitemap's extension is XML
    if sitemap_url[-4:].lower() != '.xml':
        raise AttributeError('Invalid sitemap format! {0}'.format(sitemap_url))

    # Fetching sitemap from sitemap_url
    logger.info('Requesting {0}'.format(sitemap_url))
    try:
        r = requests.get(sitemap_url)
        r.raise_for_status()
    except HTTPError as h:
        logger.error('Request for {0} FAILED with status code {1}'
                     .format(sitemap_url, r.status_code))
        raise h

    root = etree.fromstring(r.content)
    if 'sitemapindex' in root.tag:
        # Requested page is sitemapindex
        logger.info('   Looks like this is sitemapindex.')
        # Fetching urlsets from this sitemapindex
        sitemaps = [c.findtext('sitemap:loc', namespaces=xml_namespaces)
                    for c in root.getchildren()]
        logger.info('   Sitemaps in this index: {0}'.format(sitemaps))
        # Fetching links from each urlset in this sitemapindex
        links_multid = [parse_sitemap(s) for s in sitemaps]
        # Flattenning multidimensional list of links
        links = list(itertools.chain.from_iterable(links_multid))
    elif 'urlset' in root.tag:
        # Requested page is urlset
        logger.info('   This looks like urlset.')
        # Fetching links from this urlset
        links = [c.findtext('sitemap:loc', namespaces=xml_namespaces)
                 for c in root.getchildren()]
        logger.info('   Succesfully fetched {0} links from {1}'
                    .format(len(links), sitemap_url))

    return links


def main():
    """
    Used only for developement and debugging purposes
    """
    for arg in sys.argv[1:]:
        url = arg
        robots = get_robots(url)
        params = parse_robots(robots)
        logger.info(params)
        for sitemap in params['sitemaps']:
            links = parse_sitemap(sitemap)
            logger.info(len(links))


if __name__ == '__main__':
    main()
