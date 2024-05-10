import pandas as pd
import json
from khuthon.public_opinion_analyzer.gpt_lab.process.gpt_env import get_openai_client
from abc import ABC, abstractmethod
from typing import List
from khuthon.base import BASE


class BaseInsightExtraction(BASE):
    def __init__(self):
        super().__init__()
        self.issue_gen = None

    @abstractmethod
    def extract_insight_gpt(self, row):
        pass

    def extract_insight_system_prompt(self):
        system_prompt = """너는 esg주식의 인사이트를 위한 helpful assistant야. 너는 다음의 5가지 임무를 수행할거야.
        1 esg관련주식 유망요소, 위협요소추출: 너는 주식 추천을 위해서 위협요소 혹은 유망요소들을 추출할거야. esg관련 주식에 영향을 미치는 긍정적, 부정적 factor들을 뉴스 기사에서 추출해.
        2 기업 추출 및 감정추출: 너는 뉴스기사에 있는 주식의 기업을 추출할거야. 기사에 존재하는 이슈들을 전부 뽑아. 그리고 뉴스기사에서 그 기업에 대해서 긍정적으로 평가하는지 
        부정적으로 평가하는지 감정을 추출해. 평가의 지표는 1~5점 사이이고, 숫자가 클수록 긍정적인 평가, 작을수록 부정적인 평가야.
        3 주식 트랜드 분석: 너는 뉴스기사를 분석해서 트랜드가 어떻게 흘러가는지 결론으로써 인사이트를 제공하는 한줄의 평가를 할거야. 주식의 종목을 추천할지, 주식투자에 부정적인, 혹은 긍정적인 
        영향은 어떠한것인지 인사이트를 정리해.
        4 esg 관련 주식 이해관계자 인물, 기관 기업 추출: 뉴스 기사에서 나오는 esg 관련 주식에 영향을 미치는 인물 이해관계자 인물들과 기관, 기업들을 추출해. 
        5 esg 관련 테마 추출: esg 관련 주식 투자에 도움이 될만한 테마가 있다면 추출해. 기업이 ESG 경영관련하여 어떤 산업분야인지 추출해
        
        위의 5가지 임무를 user prompt에 주어진 기사를 기반으로 수행해.
        
        예시는 다음과 같아.
        —--------------example-------------------
        결과 예시:
        ```json
         {
          “1 esg관련주식 유망요소, 위협요소추출”: ["esg 마이크로소프트 GPU 효율화 개발", "오마트 테크놀로지 esg 지열 발전 투자 증가", "현대 불법 폐기물 증가로 주식 하락" ......]
         },
         {
         "2 기업 추출": {"삼성": "4", 마이크로소프트: "2", 플루언스 에너지: "1" .....}
         },
         {
         "3 주식 트랜드 분석": "위 자료를 통해서 ESG 경영이 우수하고, 앞으로의 투자를 계속 받으며 수소산업이 유망하는것으로 보입니다. 마이크로 소프트 esg 경영 주식 투자 종목으로 추천합니다.
         },
        {
        "4 esg 관련 주식 이해관계자 인물, 기관 기업 추출": ["일론 머스크", "마이크로 소프트", "번지 에너지"]
        } 
        "5 esg 관련 테마 추출" : ["지열발전", "농업"......]
        ```
        """
        return system_prompt

    def extract_insight_user_prompt(self, body, title, media_outlet):
        user_prompt = f"""
        아래는 뉴스의 제목과 언론사 그리고 본문이 들어가 있어. \n
        News title: {title}\n
        News media outlet{media_outlet}\n\n

        News body: {body}
        """
        return user_prompt



class BaseABSAMediaOutlet(BASE):
    def __int__(self):
        super().__init__()

    @abstractmethod
    def asba_media_outlet_gpt(self, row):
        pass

    def sys_prompt_asba_media_outlet(self):
        pass

    def user_prompt_asba_media_outlet(self):
        pass
