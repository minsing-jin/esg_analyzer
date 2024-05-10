from bs4 import BeautifulSoup
import re
from abc import ABC, abstractmethod
import uuid
from khuthon.base import BASE


class BaseCrawler(ABC, BASE):
    def __init__(self):
        super().__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        # EDA후 데이터셋
        # TODO: query_geration_lst -> 나중으로
        self.query_generation_lst = None    # 데이터 기반 쿼리 만들어주는 데이터 lst

        self.crawled_dataset = None  # 뉴스 기사 데이터셋

        # GPT finally generation
        self.issue_dataset = None   # 이슈 데이터셋
        self.absa_dataset = None    # absa 데이터셋
        self.stakeholder_dataset = None     # 이해관계자 데이터셋

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
