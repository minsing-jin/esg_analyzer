import pandas as pd
import json
from public_opinion_analyzer.gpt_lab.process1.gpt_env import get_openai_client
from abc import ABC, abstractmethod
from typing import List

class BaseLocalGovernmentAnalysis(ABC):
    def __init__(self):
        self.client = get_openai_client()


class ExtractLocalGovernmentAnalysis(BaseLocalGovernmentAnalysis):
    def __init__(self):
        super().__init__()

    # TODO: 함수형프로그래밍으로 프롬프트를 넣을 수는 없을까?
    def issue_extract_gpt(self, row):
        pass

    def important_event_extract_gpt(self, row):
        pass

    # TODO: 이슈를 프롬프트에 제시해야할까 person과 quote를 뽑으려면 -> 굳이?
    def sys_prompt_person_quote_extract(self):
        system_prompt = """
        지자체 관련 뉴스 기사에서 핵심이 되는 인물과 조직 그리고 그들이 말하는 중요한 top 3개의 quote들을 뽑을거야. 3개가 안되면 3개 이하로 뽑아도 돼.
        또한 뉴스 기사에서 대립적인 관계에 있는 이해관계자가 있다면 이해관계자도 뽑아줄거야.
        결과물들은 모두 한글로 뽑아줘.

        ----example1----
        "article": "In a recent development, the Mayor of Seoul has announced a new initiative to improve public transportation. 
        The initiative, spearheaded by the Seoul Metropolitan Government, aims to reduce traffic congestion and pollution. 
        Mayor Park, Handonggun stated, 'This initiative will transform our city's landscape,' emphasizing the importance of sustainable development.",

        ```json
        {
            "person": ["Mayor Park","Handonggun" .......],
            "organization": ["Seoul Metropolitan Government", "City Council" .......],
            "stakesholder": ["stakeholder1", "stakeholder2" .......],
            "top_quotes": [
                "This initiative will transform our city's landscape",
                "aims to reduce traffic congestion and pollution",
                "emphasizing the importance of sustainable development"]
        }
        ```

        ----example2----
        "article": 이 밖에 의대 증원에 반발해 사직한 전공의들에게 보건복지부가 내린 업무개시명령을 취소해달라는 소송,의협 관계자가 전공의들의 집단행동을 
        조장했다는 이유로 면허정지 처분을 받은 것을 집행정지해달라는 소송도 진행 중이다. 정부가 의대 증원 규모를 2000명으로 결정한 회의체의 회의록을 작성하지 
        않아 직무를 유기했다며 복지부·교육부 장·차관 등을 고위공직자범죄수사처에 고발한 사건도 있다.협 의 관계자가 전공의들의 집단행동을 조장했다는 이유로 
        면허정지 처분을 받은 것을 집행정지해달라는 소송도 진행 중이다. 정부가 의대 증원 규모를 2000명으로 결정한 회의체의 회의록을 작성하지 않아 직무를 
        유기했다며 복지부·교육부 장·차관 등을 고위공직자범죄수사처에 고발한 사건도 있다.
        ``json
        {
            "person": ["전공의 ","복지부·교육부 장·차관", "협 의 관계자" .......],
            "organization": ["보건복지부", "정부", "고위공직자범죄수사처" .......],
            "stakesholder": ["전공의", "정부, "보건복지부" .......],
            "top_quotes": ["의대 증원 규모를 2000명으로 결정한 회의체의 회의록을 작성하지 
        않아 직무를 유기했다며 복지부·교육부 장·차관 등을 고위공직자범죄수사처에 고발",
        "의대 증원에 반발해 사직한 전공의들에게 보건복지부가 내린 업무개시명령을 취소해달라",
        ]
        }
        ```

    
        -----output_format-----
         ```json
        {
            "person": ["person1","person2" .......],
            "organization": ["organization1", "organization2" .......],
            "top_quotes": [
                "quote1",
                "quote2",
                "quote3"]
        }
        ```
        """
        return system_prompt

    def user_prompt_person_quote_extract(self, body, title, media_outlet):
        user_prompt = f"""
        News title: {title}\n
        News media outlet{media_outlet}\n\n

        News body: {body}
        """
        return user_prompt

    def extract_person_quote_gpt(self, row):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={'type': "json_object"},
                messages=[
                    {"role": "system", "content": self.sys_prompt_person_quote_extract()},
                    {"role": "user",
                     "content": self.user_prompt_person_quote_extract(row['title'], row['media_outlet'], row['Body'])}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError as e:
            print("Error parsing JSON: ", e)
            return "No category"