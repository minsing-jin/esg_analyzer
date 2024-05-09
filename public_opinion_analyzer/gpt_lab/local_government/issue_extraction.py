import pandas as pd
import json
from public_opinion_analyzer.gpt_lab.process1.gpt_env import get_openai_client
from abc import ABC, abstractmethod
from public_opinion_analyzer.gpt_lab.local_government.base import ExtractLocalGovernmentAnalysis
from typing import List


class LocalGovernmentArticles(ExtractLocalGovernmentAnalysis):
    def __init__(self):
        super().__init__()


if __name__  == "__main__":
    news_articles = pd.read_csv('/Users/jinminseong/Desktop/local_government_news.csv')
    loacl_articles_analysis = LocalGovernmentArticles()
    news_articles['quote_person'] = news_articles.apply(loacl_articles_analysis.extract_person_quote_gpt, axis=1)
    test = news_articles['quote_person']

    news_articles.to_csv('/Users/jinminseong/Desktop/person_organization_top_quote.csv', index=False)
