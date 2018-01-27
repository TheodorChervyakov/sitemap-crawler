
from crawler.crawler import Crawler

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


@pytest.mark.parametrize("links", [
    ['http://example.com'],
    ['http://example.com', 'http://google.com']
])
def test_crawler_init_with_invalid_max_batch_size(links):
    c = Crawler(links, max_batch_size=2)

    assert c.max_batch == len(links)


@pytest.mark.parametrize("crawl_delay", [-1, 0.088, 0])
def test_crawler_init_with_invalid_crawl_delay(crawl_delay):
    with pytest.raises(ValueError):
        c = Crawler(['http://exmaple.com'],crawl_delay=crawl_delay)


def test_crawler_init_if_links_is_not_list():
    with pytest.raises(AttributeError):
        c = Crawler('http://example.com')
