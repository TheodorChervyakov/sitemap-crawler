'''
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
'''
import requests
from lxml import etree

import re
import sys
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

sitemap_pattern = re.compile('sitemap: ([\w.\:\-/]+\.xml/?)', re.IGNORECASE)
crawl_delay_pattern = re.compile('crawl\-delay: ([\d.]+)', re.IGNORECASE)

def get_robots(url):
    ''' 
    Retrieves robots.txt from
    url + /robots.txt
    '''
    # Building link to robots.txt
    if url[-1] != '/': url += '/'
    robots_url = url + 'robots.txt'

    logger.info('Fetching robots.txt from {0}'.format(robots_url))
    # Fetching robots.txt
    try:
        r = requests.get(robots_url)
        r.raise_for_status()
        logger.debug(r.text)
        return r.text
    except requests.exceptions.HTTPError as e:
        logger.error('Request for {0} failed with code {1}'
                    .format(robots_url,r.status_code))
        raise e
    except Exception as ex:
        logger.exception(ex)
        raise ex

def parse_robots(robots_string,crawl_delay=True):
    params = {'sitemaps' : list()}
    
    matches = sitemap_pattern.findall(robots_string)
    params['sitemaps'] = set(matches)
    
    if crawl_delay:
        c = crawl_delay_pattern.search(robots_string)
        if c: params['crawl-delay'] = c.group(1)
        else: params['crawl-delay'] = None

    return params


def main():
    for arg in sys.argv[1:]:
        url = arg
        robots = get_robots(url)
        params = parse_robots(robots)
        logger.info(params)

if __name__ == '__main__':
    main()
