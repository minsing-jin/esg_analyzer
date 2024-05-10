from khuthon.public_opinion_analyzer.gpt_lab.process.base import BaseInsightExtraction
import pandas as pd
import json
from typing import List

# TDOO: 인사이트 도출, 수치관련 인용구 추출
class InsightExtraction(BaseInsightExtraction):
    def __init__(self):
        super().__init__()

    def extract_isight_gpt(self, row):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={'type': "json_object"},
                messages=[
                    {"role": "system", "content": self.extract_insight_system_prompt()},
                    {"role": "user", "content": self.extract_insight_user_prompt(row['Body'], row['title'], row['media_outlet'])}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError as e:
            print("Error parsing JSON: ", e)
            return "No category"  # or handle the error appropriately


# issue categorization
if __name__ == '__main__':
    # articles = pd.read_csv('/Users/jinminseong/Desktop/#2_issue_extraction_and_summary.csv')
    # tt= json.loads(articles['0'][0])
    #
    #
    issue_reproduction = ReproductionIssue()

    # issue etraction한게 리스트로 담긴게 아니라 string으로 담겨서 다시 수정해야함.
    # articles['issue'] = articles['issue'].apply(ast.literal_eval)
    #
    # # issue categorization
    # issue_lst = list(itertools.chain.from_iterable(articles['issue'].tolist()))
    # issues = issue_reproduction.categorize_gpt(issue_lst)
    # issue_reproduction.issues_str = ", ".join(issues)

    articles = pd.read_csv('/Users/jinminseong/Desktop/naver_articles.csv')
    articles["issue"] = articles.apply(issue_reproduction.matching_issue, axis=1).apply(pd.Series)
    tset = 0
    articles.to_csv('/Users/jinminseong/Desktop/#3_gpt_4_issue_reproduction.csv', index=False)



if __name__ == '__main__':
    articles = pd.read_csv('/Users/jinminseong/Desktop/naver_articles.csv')

    articles = articles
    issue_extraction = CooperateExtraction()
    tmp = articles.apply(issue_extraction.extract_issue_gpt, axis=1)

    articles = pd.concat([articles, tmp], axis=1)
    articles.to_csv('/Users/jinminseong/Desktop/#2_issue_extraction_and_summary.csv', index=False)
