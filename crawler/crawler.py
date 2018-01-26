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
import threading

import logging

class Crawler(threading.Thread):

    def __init__(self, links, crawl_delay=1, max_batch_size=0):
        ''' Initialize crawler.
            
            @links is the list of links to scan
            @crawl_delay is the delay between requests (in seconds)
            @max_batch_size is the maximum number of consecutive requests
        '''
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing crawler.')
        num_links = len(links)
        if num_links is 0:
            raise ValueError(
                    'Number of links in the list should be at least 1!')

        if crawl_delay < 0.1:
            raise ValueError(
                    'Crawl delay cannot be less than 100 ms! Received {0}'
                    .format(crawl_delay))
        
        self.links = links
        self.crawl_delay = crawl_delay
        self.logger.info('Crawl delay is set to {0} seconds'
                        .format(self.crawl_delay))
        # If max_batch_size is less than 0 or exceeds length of links,
        # set max batch to the number of received links
        if 1 > max_batch_size or max_batch_size > num_links:
            max_batch_size = num_links
        self.max_batch = max_batch_size
        self.logger.info('Max batch size is set to {0}'.format(self.max_batch))
        self.logger.info('Crawler succesfully intialized.')

def main():
    logging.basicConfig(level=logging.INFO)
    c = Crawler(['http:google.com'])

if __name__ == '__main__':
    main()
