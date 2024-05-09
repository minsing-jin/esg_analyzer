import pandas as pd
import json
from public_opinion_analyzer.gpt_lab.process1.gpt_env import get_openai_client
from public_opinion_analyzer.gpt_lab.process1.base import BaseABSAMediaOutlet


"""
언론사별 ASBA 분석을 통해서 언론들이 어떻게 한 이슈에 대해서 다루고 있는지를 알아보기 위한 모듈
"""

class ASBAMediaOutlet(BaseABSAMediaOutlet):
    def __init__(self):
        super().__init__()

