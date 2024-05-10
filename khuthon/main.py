from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLineEdit, QLabel
import sys
import pandas as pd
from khuthon.preprocessing_raw.preprocessing_data import GoogleSheetLoadPreprocessing
from khuthon.public_opinion_analyzer.crawler.search_engine_news_crawler import SearchEngineNewsCrawler
from khuthon.public_opinion_analyzer.gpt_lab.process.article_summary import ArticleSummary
from khuthon.public_opinion_analyzer.gpt_lab.process.insight_extraction import InsightExtraction
from khuthon.public_opinion_analyzer.gpt_lab.process.preprocessing import Preprocessing

class MyApp(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text Mining Report Generator')
        layout = QVBoxLayout()

        self.label = QLabel("검색어를 입력해주세요:", self)
        layout.addWidget(self.label)

        self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit)

        self.btn1 = QPushButton("1: 생성", self)
        self.btn1.clicked.connect(self.process_input)
        layout.addWidget(self.btn1)

        self.btn0 = QPushButton("0: 종료", self)
        self.btn0.clicked.connect(self.close)
        layout.addWidget(self.btn0)

        self.setLayout(layout)

    def process_input(self):
        query = self.lineEdit.text()
        self.generate_report(query)

    def generate_report(self, query):
        gpt_df = pd.DataFrame()
        google_sheet_preprocessing_process = GoogleSheetLoadPreprocessing()
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

        for idx, df in enumerate(df_lst):
            google_sheet_preprocessing_process.upload_dataset(df, df_name_lst[idx])

        print("텍스트 마이닝 보고서 생성이 완료되었습니다!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
