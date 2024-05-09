import pandas as pd
import json
from public_opinion_analyzer.gpt_lab.process1.base import BaseReproduction
from typing import List
import ast
import itertools


class ReproductionIssue(BaseReproduction):
    def __init__(self):
        super().__init__()
        self.issues_str = "전공의 면허정지 처분 무기한 연기, 의대 정원 확대에 대한 정부와 의사단체의 갈등, 의료계의 집단 사직서 제출 예고와 그 후폭풍, 한동훈 비상대책위원장의 중재 역할, 비수도권 의대 지역인재전형 확대, 수시모집 최저학력기준 완화 가능성, 비수도권 대학의 정시모집 어려움, 수도권 학생들의 비수도권 의대 지원 기회 변화, 의료 서비스 접근성, 의료 공백 장기화 우려, 고3 재학생의 대비, 진학 지도 및 지원 강화, 의대 교수 사직서 예고, 정부와 의료계의 대화 노력, 비수도권 의대 정원 증원과 지방유학 시대의 도래, 지역인재전형 확대와 지역 균형 발전, 의대 열풍과 사교육 시장의 반응, 지방유학과 입시 경쟁 심화, 비수도권 의대 증원의 사회적 비용 우려, 의사 파업과 전공의 복귀, 정치적 성향과 의사 파업에 대한 인식, 의료대란에 대한 고령층의 우려, 의대 교수들의 집단 사직 및 서비스 축소, 무수능 전형 도입, 의대 정원 확대와 교육 질 문제, 의료 인프라 확충을 위한 정부의 재정 투입, 의대 증원을 통한 의사 수 확대의 필요성, 전공의에 대한 의존도 낮추기, 학습권 침해와 개인의 권리 존중, 의사 집단의 사회적 지위와 국민 생명"

    # TODO:category가 15개 안나올수도 있어서 exception 처리 해야함.
    def categorize_gpt(self, issue_lst: List):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={'type': "json_object"},
                messages=[
                    {"role": "system", "content": self.sys_prompt_categorize_issue()},
                    {"role": "user",
                     "content": self.user_prompt_categorize_issue(", ".join(issue_lst))}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            return result['reproduction_issue']
        except json.JSONDecodeError as e:
            print("Error parsing JSON: ", e)
            return "No category"  # or handle the error appropriately

    def matching_issue(self, row):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={'type': "json_object"},
                messages=[
                    {"role": "system", "content": self.sys_prompt_matching_issue(self.issues_str)},
                    {"role": "user", "content": self.user_prompt_matching_issue(row['title'], row['media_outlet'], row['Body'])}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError as e:
            print("Error parsing JSON: ", e)
            return "No category"

# TODO: 추후 모듈로 쓸거면 내가 실수로 만든것들 다시 refactoring 해야함.

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

    # gpt-4로 issue matching

    articles = pd.read_csv('/Users/jinminseong/Desktop/naver_articles.csv')
    articles["issue"] = articles.apply(issue_reproduction.matching_issue, axis=1).apply(pd.Series)
    tset = 0
    articles.to_csv('/Users/jinminseong/Desktop/#3_gpt_4_issue_reproduction.csv', index=False)
