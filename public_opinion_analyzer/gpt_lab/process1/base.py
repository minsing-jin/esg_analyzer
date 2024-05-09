import pandas as pd
import json
from public_opinion_analyzer.gpt_lab.process1.gpt_env import get_openai_client
from abc import ABC, abstractmethod
from typing import List

class BaseProcess(ABC):
    def __init__(self):
        self.client = get_openai_client()


class BaseExtraction(BaseProcess):

    @abstractmethod
    def extract_issue_gpt(self, row):
        pass

    def create_issue_extration_system_prompt(self):
        system_prompt = """
        Prompt on article issue extraction for sentiment analysis
        You are a helpful assistant designed to output JSON in Korean.
        Analyze the content of an article to identify the primary issues discussed, focusing on aspects that might lead to varied opinions (pro, con, neutral) in the comments section. For each issue:
        1. Summarize its core aspect in a single sentence, ensuring the summary is neutral yet captures potential perspectives.
        2. Structure your findings in JSON, with each entry containing:
          - A ‘issue’ field for the issue.
          - A 'description' field providing a neutral summary that encapsulates possible public opinions.
        Ensure the description:
        - Avoids a general overview without clear positions.
        - Directly relates to a stance that could be labeled as pro, con, or neutral.
        - Emphasizes specific aspects of the issue that are likely to evoke diverse opinions, facilitating discussion and aligning with potential positions from commenters or reporters.
        Here's the article content: {{article content}}
        
        —--------------example-------------------
        결과 예시:
        [
         {
          “Issue”: "전공의 면허정지 연기",
          "description": "정부가 전공의 면허정지 처분을 무기한 연기하여 의료개혁에 관한 협의를 모색하는 것으로, 일부는 정부의 유연한 접근을 지지하지만 다른 이들은 이로 인한 의료 현장의 불안을 우려할 수 있음.",
         },
         {
          “Issue”: "의대 정원 확대 논란",
          "description": "정부는 의대 정원을 확대하지 않겠다는 입장을 고수하고 있으며, 이에 대해 일각은 의료 공백과 감정 소모를 우려하여 합리적인 접근을 지지하고 있으나, 다른 이들은 의대 정원 확대의 필요성을 강조하고 있을 수 있음.",
         },
         {
          “Issue”: "정부와 의료계 협의",
          "description": "정부와 의료계가 협의체를 구성하여 대화를 모색하는 것으로, 이에 대해 일부는 문제 해결을 위한 건설적인 노력으로 평가할 수 있지만, 다른 이들은 정부의 결정이 실질적인 결과를 도출할 수 있는지에 대한 의문을 제기할 수 있음.",
         },
         .........
        ]
        """
        return system_prompt

    def create_issue_extration_user_prompt(self, body, title, media_outlet):
        user_prompt = f"""
        아래는 뉴스의 제목과 언론사 그리고 본문이 들어가 있어. 이 내용을 바탕으로 여론이 될 만한 이슈들을 추출해줘. \n
        News title: {title}\n
        News media outlet{media_outlet}\n\n

        News body: {body}
        """
        return user_prompt


class BaseReproduction(BaseProcess):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def categorize_gpt(self, row):
        pass

    @abstractmethod
    def matching_issue(self, row):
        pass

    def sys_prompt_categorize_issue(self):
        sys_prompt = """
        The user prompt will contain the issue extracted from the news article. \n
        Based on this, summarize the issue and reproduce the issue in Korean.

        --------output format---------------
        ```json
        {
        "reproduction_issue": ["reproduction_issue1", "reproduction_issue2", "reproduction_issue3"......]
        }
        ```
        """
        return sys_prompt

    def user_prompt_categorize_issue(self, issues: str):
        user_prompt = f"""
        아래는 뉴스 기사에서 추출된 이슈가 들어가 있어. 
        이 내용들을 바탕으로 비슷한 의미를 가지고 있는 이슈들은 묶거나 비슷한 이슈들의 개념을 모두 포함하는 
        이슈로 포함해. 혹은 여러 개념을 포함할 수 있는 더큰 상위 개념의 이슈가 있다면 상위개념의 이슈로 제시해. 
        제시된 이슈들을 가장 잘 나타내는 이슈들을 생성 혹은 카테고라이즈해서 system prompt에 제시된 json format처럼 리스트에 20개의 
        reproduction된 이슈들을 담아줘. \n
        f{issues}
        \n
        -------------------예시-------------------
        예시1. 예를들면 "의사 정원 확대", "의사 인구수 늘림"은 둘의 의미가 같으므로 공통된 의미인 "의사 정원 확대"로 볼 수 있어.
        예시2. 예를들면 의사전형확대로 인한 기사에 "지역인재 전형", "지역 인재 특별전형 비율 확대", "의대 진학 경쟁"가 이슈라면 더큰 상위 개념인 "의대 입시 문제"로 묶을 수 있어.
        """
        return user_prompt

    def sys_prompt_matching_issue(self, issues: str):
        sys_prompt = (f"""
        제시된 뉴스기사에 본문과 가장 가까운 이슈들을 매칭시켜서 json형식으로 내보내. \n
        제시된 뉴스에서 나올 이슈들은 다음과 같아. {issues} \n
        """ + """
        --------output format---------------
        ```json
        {
        "matching_issue": ["most_corrected_issue1" , "most_corrected_issue2", "most_corrected_issue3" .....]
        }
        ```
        """)
        return sys_prompt

    def user_prompt_matching_issue(self, title, media_outlet, body):
        user_prompt = f"""
        아래는 뉴스 기사에서 추출된 이슈가 들어가 있어. 이 내용들을 바탕으로 가장 가까운 의미를 가지고 있는 이슈를 선택해줘. \n
        
        News title: {title}\n
        News media outlet{media_outlet}\n\n

        News body: {body}
        """
        return user_prompt


class BaseABSAMediaOutlet(BaseProcess):
    def __int__(self):
        super().__init__()

    @abstractmethod
    def asba_media_outlet_gpt(self, row):
        pass

    def sys_prompt_asba_media_outlet(self):
        pass

    def user_prompt_asba_media_outlet(self):
        pass


class BaseCityExtraction(BaseProcess):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_location(self, address):
        pass

    def sys_prompt_city_extraction(self):
        pass

    def user_prompt_city_extraction(self):
        pass