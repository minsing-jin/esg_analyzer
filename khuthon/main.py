from khuthon.user_interface.base_user_interface import MyApp
import sys
from khuthon.preprocessing_raw.preprocessing_data import GoogleSheetLoadPreprocessing
from khuthon.public_opinion_analyzer.crawler.search_engine_news_crawler import SearchEngineNewsCrawler
from PyQt5.QtWidgets import QApplication
from khuthon.public_opinion_analyzer.gpt_lab.process.article_summary import ArticleSummary
from khuthon.public_opinion_analyzer.gpt_lab.process.insight_extraction import InsightExtraction
import pandas as pd
from khuthon.public_opinion_analyzer.gpt_lab.process.preprocessing import Preprocessing

# TODO: 산업별 온실가스 배출량으로 판별하기 근데 인사이트 제공하기에는 너무 데이터가 없음
# TODO: 산업별, 지역별, 년도별 온실가스 배출량으로 판별하기
if __name__ == '__main__':

   # TODO: 선택버튼(google sheet 만들고) 누르고 ux 디자인 -> 후순위로 배치
   # app = QApplication(sys.argv)
   # ex = MyApp()
   # sys.exit(app.exec_())
   cnt = 0

   while(cnt < 1):
       """
        gpt_df = pd.DataFrame()

        # step0. 인스턴스 선언
        google_sheet_preprocessing_process = GoogleSheetLoadPreprocessing()
        
        # 분석한 google 스프레트 sheet dataset 가져오기
        query_dic = {}
        
        # TODO: EDA -> 판다스 ai + GPT로 가장 문제 있는 산업군/ 지역/ 년도 추출
        # TODO: 가장 문제 있는 녀석 추출
        query_dic = google_sheet_preprocessing_process.query_generation()


        # TODO: 이에 따라서 GPT가 query generation + 생성한 query마다 10개씩 기사에 따른 크롤링 -> 일단 optional로 두기
        crawler = SearchEngineNewsCrawler(query_dic)
        gpt_df = crawler.run_crawling()

        # TODO: 크롤링한 기사 데이터 셋을 통해서 GPT 인사이트 추출
        summary = ArticleSummary()
        insight_extraction = InsightExtraction()

# try except로 예외처리 -> 지금 element들이 dict로 담김 항상 그럴지는 또 몰라서 ㅋㅋ
        gpt_df['article_summary'] = gpt_df.apply(summary.article_summarize, axis=1)
        gpt_df['insights'] = gpt_df.apply(insight_extraction.extract_isight_gpt, axis=1)
        gpt_df.to_csv('/Users/jinminseong/Desktop/2시연용데이터_article_summary_insights_완료.csv', index=False)
        

       preprocessing = Preprocessing()
       gpt_df = pd.read_csv('/Users/jinminseong/Desktop/2시연용데이터_article_summary_insights_완료.csv')
       preprocessing.run_preprocessing(gpt_df)
        """
       comments = pd.read_csv('/Users/jinminseong/Desktop/3시연용데이터_article_summary_insights_완료_theme.csv')


       cnt += 1


   # TODO: 텍스트 마이닝 Issue Extraction/ stakeholder extraction/ ABSA /

       # TODO: 말하는 판다스: 사용자 프롬프트 실험을 통해서 pandas ai를 활용한 데이터 preprocessing 및 분석 툴 제공
       # TODO: 사용자 프롬프트 제공은 while loop를 통해서 사용자가 원하는 만큼 계속 진행하고 실험할 수 있도록 제공, 이걸 통해서 looker studio에서
       # TODO: 각 해당하는 차트에 해당하는 구글 sheet의 이름으로 저장하면 말하는 판다스가 되네 -> 위젯은 배치까지는 아니어도 위젯 하나에 대해서는 반영가능
       # TODO: 혹은 자기가 쓰고자 하는 위젯과 그 위젯에 네이밍이 되어있는 데이터셋만 맞추고, 사용자가 배치하고자 하는 에셋들을 대시보드에 디자인하고
       # TODO: 말하는 판다스로 데이터만 만지고 분석하면 가능


       # TODO: 루커스튜디오 텍스트마이닝 시각화

       # TODO: 마지막 리포트 generation은 GPT를 통해서 리포트를 생성하고 이를 pdf로 저장 및 looker studio에 맨 마지막 페이지에 반영
       # TODO: 마지막은 경제 기업 정치 사회 기술적 관점 리포트 작정 -> article summary들로 -> 추천 기업을 바탕으로
       # google_sheet_preprocessing_process.upload_dataset()


# if __name__ == '__main__':
#     naver_base_crawler = SearchEngineNewsCrawler()
#     info_main = input("=" * 50 + "\n" + "입력 형식에 맞게 입력해주세요." + "\n" + " 시작하시려면 Enter를 눌러주세요." + "\n" + "=" * 50)
#
#     maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")
#     query = input("검색어 입력: ")
#     sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")  # 관련도순=0  최신순=1  오래된순=2
#     s_date = input("시작날짜 입력(2019.01.04):")  # 2019.01.04
#     e_date = input("끝날짜 입력(2019.01.05):")  # 2019.01.05
#
#     df = naver_base_crawler.fetch_news_content(maxpage, query, sort, s_date, e_date)
#
#     # Preprocessing Comments
#     df['Comments_tuples'] = df['naver_news_link'].apply(naver_base_crawler.get_comments)
#     df['Body'] = df['naver_news_link'].apply(naver_base_crawler.get_content)
#
#     flatten_df = df['Body'].apply(pd.Series)
#
#     df = pd.concat([flatten_df, df[['Comments_tuples']]], axis=1)
#
#     articles = deepcopy(df)
#     articles['ArticleID'] = articles.apply(naver_base_crawler.creat_uuid, axis=1)
#
#     Comments = deepcopy(articles)
#     Comments = Comments[Comments['Comments_tuples'].apply(lambda x: len(x) > 0)]
#     Comments = Comments.explode('Comments_tuples')
#     Comments[['CommentID','Comment_person','CommentDate', 'CommentText']] = Comments['Comments_tuples'].apply(pd.Series)
#     Comments = Comments.reset_index(drop=True).drop('Comments_tuples', axis=1)
#
#     articles = articles[['ArticleID', 'PublicationDate', 'title', 'media_outlet', 'link', 'Body', 'Comments_tuples']]
#     Comments = Comments[['CommentID', 'ArticleID', 'Comment_person', 'CommentDate', 'CommentText', 'PublicationDate', 'title', 'media_outlet', 'link', 'Body']]
#     comments_col = Comments.columns.tolist()
#     articles_col = articles.columns.tolist()
#     articles['PublicationDate'] = articles['PublicationDate'].apply(convert_string_time_to_iso8601)
#
#     articles.to_csv('/Users/jinminseong/Desktop/naver_articles.csv', index=False)
#     Comments.to_csv('/Users/jinminseong/Desktop/naver_comments.csv', index=False)





