from bs4 import BeautifulSoup
import re
from abc import ABC, abstractmethod
import uuid

class BaseCrawler(ABC):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

    # Function to clean HTML content
    def clean_html(self, html_content):
        pattern = '<[^>]*>'
        cleaned_text = re.sub(pattern, '', html_content)
        cleaned_text = cleaned_text.replace("\n", " ").strip()
        return cleaned_text

    def creat_uuid(self, row):
        return uuid.uuid4()

    @abstractmethod
    def extract_news_link(self, maxpage, query, sort, s_date, e_date):
        pass

    @abstractmethod
    def fetch_news_content(self, url):
        pass

    @abstractmethod
    def get_content(self, url):
        pass

    @abstractmethod
    def get_comments(self, url, wait_time=5, delay_time=0.1):
        pass
