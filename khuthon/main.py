from khuthon.user_interface.base_user_interface import MyApp
import sys
from khuthon.preprocessing_raw.preprocessing_data import GoogleSheetLoadPreprocessing
from khuthon.public_opinion_analyzer.crawler.search_engine_news_crawler import SearchEngineNewsCrawler
from PyQt5.QtWidgets import QApplication
from khuthon.public_opinion_analyzer.gpt_lab.process.article_summary import ArticleSummary
from khuthon.public_opinion_analyzer.gpt_lab.process.insight_extraction import InsightExtraction
import pandas as pd
from khuthon.public_opinion_analyzer.gpt_lab.process.preprocessing import Preprocessing

if __name__ == '__main__':
    button = ""
    query = ""

    while(True):
        if (button == "0"):
            break
        button = str(input("텍스트 마이닝 보고서를 생성하시겠습니까? (0: 종료, 1: 생성) : "))
        query = str(input("검색어를 입력해주세요: "))

        gpt_df = pd.DataFrame()

        # step0. 인스턴스 선언
        google_sheet_preprocessing_process = GoogleSheetLoadPreprocessing()

        query_dic = {}

        query_dic = google_sheet_preprocessing_process.query_optimization(query)

        crawler = SearchEngineNewsCrawler(query_dic)
        gpt_df = crawler.run_crawling()

        summary = ArticleSummary()
        insight_extraction = InsightExtraction()

        gpt_df['article_summary'] = gpt_df.apply(summary.article_summarize, axis=1)
        gpt_df['insights'] = gpt_df.apply(insight_extraction.extract_isight_gpt, axis=1)

        preprocessing = Preprocessing()
        comment, corp, esg_threaten, trend, stakeholder, theme = preprocessing.run_preprocessing(gpt_df)
        df_lst = [corp, esg_threaten, trend, stakeholder, theme]
        df_name_lst = ['corp', 'threaten', 'trend', 'stakeholder', 'theme']

        for idx in range(len(df_lst)):

            google_sheet_preprocessing_process.upload_dataset(df_lst[idx], df_name_lst[idx])

        print("텍스트 마이닝 보고서 생성이 완료되었습니다!")
