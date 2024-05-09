import pandas as pd
import json
from public_opinion_analyzer.gpt_lab.process1.gpt_env import get_openai_client
from public_opinion_analyzer.gpt_lab.process1.base import BaseExtraction


"""
1번 프롬프트로 기사를 주제(의료 정원 확대)랑 넣었을 때 기사에서 여론이 될 만한 이슈들을 뽑는 것도 챌린지고 
2번 프롬프트에서 1번에서 뽑힌 결과값들을 뭉터기(포맷이나 양은 너가 실험을 통해 판단해서 전략을 세우도록)로
전달해서 괜찮은 수준만큼 줄이는 것도 챌린지일 거야.
"""


class IssueExtraction(BaseExtraction):
    def __init__(self):
        super().__init__()

    def extract_issue_gpt(self, row):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={'type': "json_object"},
                messages=[
                    {"role": "system", "content": self.create_issue_extration_system_prompt()},
                    {"role": "user", "content": self.create_issue_extration_user_prompt(row['Body'], row['title'], row['media_outlet'])}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError as e:
            print("Error parsing JSON: ", e)
            return "No category"  # or handle the error appropriately


if __name__ == '__main__':
    articles = pd.read_csv('/Users/jinminseong/Desktop/naver_articles.csv')

    articles = articles
    issue_extraction = IssueExtraction()
    tmp = articles.apply(issue_extraction.extract_issue_gpt, axis=1)

    articles = pd.concat([articles, tmp], axis=1)
    articles.to_csv('/Users/jinminseong/Desktop/#2_issue_extraction_and_summary.csv', index=False)
