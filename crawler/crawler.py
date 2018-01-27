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
from requests.exceptions import HTTPError

from crawler.exceptions import BadStatusCode

import threading
import logging

class Crawler(threading.Thread):

    def __init__(self, links, crawl_delay=1, max_batch_size=0,
                user_agent=None,timeout=15):
        ''' Initialize crawler.
            
        Attributes:
            links -- list of links to scan
            crawl_delay -- delay between requests (in seconds)
            max_batch_size -- maximum number of consecutive requests
            user_agent -- user agent to use when requesting pages
            timeout -- timeout value in seconds to use when requesting pages
        '''
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info('Initializing crawler.')
        
        # Performing critical checks
        if not isinstance(links, list):
            raise AttributeError

        if len(links) is 0:
            raise ValueError(
                    'Number of links in the list should be at least 1!')

        if crawl_delay < 0.1:
            raise ValueError(('Crawl delay cannot be less than 100 ms! '
                            + '{0} seconds specified.')
                            .format(crawl_delay))
        
        num_links = len(links)
        # If max_batch_size is less than 0 or exceeds length of links,
        # set max batch to the number of received links
        if 1 > max_batch_size or max_batch_size > num_links:
            max_batch_size = num_links
        
        # Initializing variables
        self.links = links
        self.crawl_delay = crawl_delay
        self.max_batch = max_batch_size
        self.user_agent = user_agent
        self.timeout = timeout
        self.done = False

        self.logger.info('Crawl delay is set to {0} seconds'
                        .format(self.crawl_delay))
        self.logger.info('Max batch size is set to {0}'.format(self.max_batch))
        self.logger.info('Crawler succesfully intialized.')


    def scan_page(self, url):
        ''' Perform GET request on specified url
        '''
        headers = dict()
        # If user agent was specified use it
        if self.user_agent is not None:
            headers['User-Agent'] = self.user_agent

        try:
            r = requests.get(url, headers=headers, timeout=self.timeout)
            r.raise_for_status()
        except HTTPError as e:
            raise BadStatusCode(url, e.response.status_code)
        except Exception:
            logger.error('An uncaught exception occured in scan_page')
            raise
        else:
            return r.elapsed.total_seconds()


    #def run(self):
        

def main():
    logging.basicConfig(level=logging.INFO)
    c = Crawler(['http://google.com'])
    logging.info(c.scan_page('http://google.com/4040'))


if __name__ == '__main__':
    main()
