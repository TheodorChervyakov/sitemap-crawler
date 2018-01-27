from crawler import fetcher

class TestFetcher(object):
        
    sitemap_url1 = 'http://example.com/sitemap.xml'
    sitemap_url2 = 'http://example.com/sitemap2.xml/'
    sitemap_word = 'Sitemap: '
    
    def test_parse_robots(self):

        robots = self.sitemap_word + self.sitemap_url1

        returned_params = fetcher.parse_robots(robots)
        assert 'sitemaps' in returned_params.keys()
        assert self.sitemap_url1 in returned_params['sitemaps']
        assert 1 == len(returned_params['sitemaps'])

        robots += '\n' + self.sitemap_word + self.sitemap_url2

        returned_params_2 = fetcher.parse_robots(robots) 
        assert 'sitemaps' in returned_params_2.keys()
        assert (self.sitemap_url1 in returned_params_2['sitemaps']
                and self.sitemap_url2 in returned_params_2['sitemaps'])
        assert 2 == len(returned_params_2['sitemaps'])

    def test_parse_robots_with_crawl_delay(self):

        crawl_delay = 0.5

        robots = self.sitemap_word + self.sitemap_url1
        robots += '\n' + self.sitemap_word + self.sitemap_url2
        robots += '\n' + 'Crawl-delay: ' + str(crawl_delay)

        params = fetcher.parse_robots(robots,crawl_delay=True)

        assert 'crawl-delay' in params.keys()
        assert crawl_delay == params['crawl-delay']

        params_2 = fetcher.parse_robots(robots,crawl_delay=False)

        assert 'crawl-delay' not in params_2.keys()
        
