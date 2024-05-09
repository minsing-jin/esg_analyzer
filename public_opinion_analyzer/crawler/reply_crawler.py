# 네이버 뉴스 기사 검색 후 네이버 뉴스 버전으로 클릭
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

"""
컴퓨터처럼 생각하는것
기능 분화:
1. 검색후 링크 리스트 긁기
2. 네이버 뉴스 링크로 들어가서 본문과 댓글 긁기
"""


def crawler():

    info_main = input("=" * 50 + "\n" + "입력 형식에 맞게 입력해주세요." + "\n" + " 시작하시려면 Enter를 눌러주세요." + "\n" + "=" * 50)

    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")
    query = input("검색어 입력: ")
    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")  # 관련도순=0  최신순=1  오래된순=2
    s_date = input("시작날짜 입력(2019.01.04):")  # 2019.01.04
    e_date = input("끝날짜 입력(2019.01.05):")  # 2019.01.05

    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1
    maxpage_t = (int(maxpage) - 1) * 10 + 1  # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지

    link_lst_to_crawling = []

    while page <= maxpage_t:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=" + sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
            page)

        response = requests.get(url)
        html = response.text

        # 뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')

        # <a>태그에서 제목과 링크주소 추출
        atags = soup.select('.news_tit')
        for atag in atags:
            link_lst_to_crawling.append(atag.text)  # 제목
            link_lst_to_crawling.append(atag['href'])  # 링크주소

# 특정 뉴스 사이트 들어가면 news comments 긁어오기
def get_naver_news_contents_comments(url, wait_time=5, delay_time=0.1):


    # 크롬 드라이버로 해당 url에 접속
    driver = webdriver.Chrome()

    # (크롬)드라이버가 요소를 찾는데에 최대 wait_time 초까지 기다림 (함수 사용 시 설정 가능하며 기본값은 5초)
    driver.implicitly_wait(wait_time)

    # 인자로 입력받은 url 주소를 가져와서 접속
    driver.get(url)

    # 더보기가 안뜰 때 까지 계속 클릭 (모든 댓글의 html을 얻기 위함)
    while True:

        # 예외처리 구문 - 더보기 광클하다가 없어서 에러 뜨면 while문을 나감(break)
        try:
            more  =  driver.find_element(By.CLASS_NAME,  'u_cbox_btn_more')
            more.click()
            time.sleep(delay_time)

        except:
            break

    # 본격적인 크롤링 타임

    # selenium으로 페이지 전체의 html 문서 받기
    html = driver.page_source

    # 위에서 받은 html 문서를 bs4 패키지로 parsing
    soup = BeautifulSoup(html, 'lxml')

    # 1)작성자
    nicknames = soup.select('span.u_cbox_nick')
    list_nicknames = [nickname.text for nickname in nicknames]

    # 2)댓글 시간
    datetimes = soup.select('span.u_cbox_date')
    list_datetimes = [datetime.text for datetime in datetimes]

    # 3)댓글 내용
    contents = soup.select('span.u_cbox_contents')
    list_contents = [content.text for content in contents]


    # 4)작성자, 댓글 시간, 내용을 셋트로 취합
    list_sum = list(zip(list_nicknames,list_datetimes,list_contents))

    # 드라이버 종료
    driver.quit()

    # 함수를 종료하며 list_sum을 결과물로 제출
    return list_sum

# step3. 실제 함수 실행 및 엑셀로 저장
if __name__ == '__main__': # 설명하자면 매우 길어져서 그냥 이렇게 사용하는 것을 권장

    # 원하는 기사 url 입력
    url = 'https://n.news.naver.com/mnews/article/015/0004963867?sid=100'

    # 함수 실행
    comments = get_naver_news_contents_comments(url)

    # 엑셀의 첫줄에 들어갈 컬럼명
    col = ['작성자','시간','내용']

    # pandas 데이터 프레임 형태로 가공
    df = pd.DataFrame(comments, columns=col)
    print(df)
    # 데이터 프레임을 엑셀로 저장 (파일명은 'news.xlsx', 시트명은 '뉴스 기사 제목')
    df.to_excel('news.xlsx', sheet_name='뉴스 기사 제목')
