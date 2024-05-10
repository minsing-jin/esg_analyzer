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

