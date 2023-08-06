#!/usr/bin/env python
from acme_news.browser.acme_browser import ACMEBrowser
from typing import List, Dict

class CNNEngine(ACMEBrowser):
    """
    DESCRIPTION
        This class inherit the web browser functionalities from the ACMEBrowser.

    FUNCTIONS
        __build_bulk_query__
        __build_url_query__
        __set_category__
        __set_page_size__
        get_query
        get_all_queries
        get_article_title
        get_links
        get_all_links
        get_page_content

    USAGE
        Please run the tests using pytest tests
    """
    def __init__(self, url: str = "",
                 news_article: str = "",
                 page_depth: int = 0,
                 category: str = "politics",
                 size: int = 10):

        self.url: str = url
        self.query: str = ""
        self.page_depth = page_depth
        self.news_article: str = news_article
        self.size: int = size
        self.category: str = category
        self.cnn_links: List = []
        self.batch_queries: List = []
        self.cnn_driver = None
        self.categories: List[str] = ['us', 'world', 'politics', 'business', 'opinions', 'health', 'entertainment', 'style', 'travel']

        if self.url:
            self.cnn_driver = self.browser(url=self.url)

        elif self.news_article and page_depth > 0:
            self.batch_queries = self.__build_bulk_query__()

        elif self.news_article:
            self.cnn_driver = self.browser(url=self.__build_url_query__(size=self.size,
                                                                        category=self.category)
                                           )

        super(CNNEngine, self).__init__()

    def __build_bulk_query__(self) -> List[str]:
        if not self.news_article:
            raise ValueError(f"Please provide the right news articles")

        if self.page_depth % 10 != 0:
            raise ValueError("Page depth must be a multply of 10")

        self.batch_queries = [self.__build_url_query__(page=article_page) for article_page in range(0, self.page_depth, 10)]
        return self.batch_queries

    def __build_url_query__(self, size: int = 10, category: str = "politics", page: int = 0) -> str:

        self.__set_category__(category=category)
        self.__set_page_size__(page_size=size)

        if not self.news_article:
            raise ValueError(f"Please provide the right news articles")

        if self.category == 'all':
            self.query = f"https://www.cnn.com/search?size={self.size}&q={self.news_article}"
            return self.query

        if self.category.lower() not in self.categories:
            raise ValueError(f"The following category {self.category} is not the right category.")

        if self.page_depth == 0:
            self.query = f"https://www.cnn.com/search?size={self.size}&q={self.news_article}&category={self.category}"
            return self.query

        self.query = f"https://www.cnn.com/search?size={self.size}&q={self.news_article}&category={self.category}&from={page}&page={round(page/10) +1}"
        return self.query

    def __set_category__(self, category):
        if not category:
            raise ValueError("Please provide the right category.")

        self.category = category

    def __set_page_size__(self, page_size):
        if not page_size or page_size < 1 or not isinstance(page_size, int):
            raise ValueError("Please provide the right page size")

        self.size = page_size

    def get_query(self) -> str:
        return self.query

    def get_all_queries(self) -> List[str]:
        return self.batch_queries

    def get_article_title(self) -> str:
        return self.cnn_driver.title

    def get_links(self) -> List[str]:
        return [tag.find_element_by_tag_name('a').get_attribute('href') for tag in self.cnn_driver.find_elements_by_css_selector("h3.cnn-search__result-headline")]

    def get_all_links(self) -> List[str]:
        for url_query in self.batch_queries:
            self.cnn_driver = self.browser(url=url_query)
            self.cnn_links.extend(self.get_links())

        return self.cnn_links

    def get_page_content(self) -> Dict:
        pass


