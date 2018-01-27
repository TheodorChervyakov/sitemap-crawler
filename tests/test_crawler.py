
from crawler import Crawler
from crawler.exceptions import BadStatusCode

import pytest

@pytest.mark.parametrize("links, max_batch_size, expected_max_batch", [
    (['http://example.com'], 2, 1),
    (['http://example.com'], 1, 1),
    (['http://example.com', 'http://google.com'], 1, 1)
])
def test_crawler_init(links, max_batch_size, expected_max_batch):
    c = Crawler(links,max_batch_size=1)

    assert c.links == links
    assert c.crawl_delay == 1
    assert c.max_batch == expected_max_batch
    assert c.user_agent == None
    assert c.timeout == 15


@pytest.mark.parametrize("crawl_delay", [-1, 0.088, 0])
def test_crawler_init_with_invalid_crawl_delay(crawl_delay):
    with pytest.raises(ValueError):
        c = Crawler(['http://exmaple.com'],crawl_delay=crawl_delay)


def test_crawler_init_if_links_is_not_list():
    with pytest.raises(AttributeError):
        c = Crawler('http://example.com')


def test_crawler_scan_page_existing():
    page = 'http://example.com'
    c = Crawler([page])
    elapsed = c.scan_page(page)
    assert elapsed > 0


def test_crawler_scan_page_bad_status_code():
    page = 'http://google.com/404'
    with pytest.raises(BadStatusCode):
        c = Crawler([page])
        elapsed = c.scan_page(page)

def test_crawler_run():
    links = ['http://google.com']
    c = Crawler(links)
    c.start()
    c.join()
    assert c.done

    
