import requests
from bs4 import BeautifulSoup


class MainPageNewsCrawler:
    """
    네이버 뉴스 메인 페이지에서 뉴스를 크롤링하는 클래스
    랭킹에 따라 뉴스들을 가져옴.
    """
    def __init__(self):
        self.url = "https://news.naver.com/main/ranking/popularMemo.naver"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
        self.res = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(self.res.text, 'lxml')


    def get_news(self):
        newslist = self.soup.select(".rankingnews_list")
        newsData = []
        for news in newslist[:12]:
            # 5개의 상위랭킹 뉴스를 가져옴
            lis = news.findAll("li")
            # 5개 뉴스 데이터 수집
            for li in lis:
                # 뉴스랭킹
                news_ranking = li.select_one(".list_ranking_num").text

                # 뉴스링크와 제목
                list_title = li.select_one(".list_title")
                news_title = list_title.text
                news_link = list_title.get("href")

                # 뉴스 썸네일
                try:
                    news_img = li.select_one("img").get("src")
                except:
                    news_img = None
                print("랭킹: ", news_ranking)
                print("제목: ", news_title)
                print("링크: ", news_link)
                print("썸네일: ", news_img)

                newsData.append({
                    "rank": news_ranking,
                    "title": news_title,
                    "link": news_link,
                    "img": news_img
                })
        return newsData

    # 뉴스 안쪽으로 들어가기
    def get_news_content(self, newsData):
        # 뉴스 작성 시간
        for news in newsData:
            news_url = news['link']
            res = requests.get(news_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'lxml')
            news_time = soup.select_one(".media_end_head_info_datestamp").select_one(".media_end_head_info_datestamp_time").get("data-date-time")
            news_content = soup.select_one("#newsct_article").text.replace("\n","").replace("\t","")
            news['time'] = news_time
            news['contents'] = news_content

        return newsData
