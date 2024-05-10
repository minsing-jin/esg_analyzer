import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI


def get_openai_client():
    # Access the API key using the variable name defined in the .env file
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("API key is not set")

    client = OpenAI(api_key=api_key)
    return client


class BASE:
    def __init__(self):
        # 데이터셋 정의
        self.first_dataset = None     # 측정한 온실가스 데이터셋
        self.start_dataset_dict = None   # 구글 sheet에서 가져온 데이터셋

        self.crawled_dataset = None  # 뉴스 기사 데이터셋

        # GPT finally generation
        self.issue_dataset = None   # 이슈 데이터셋
        self.absa_dataset = None    # absa 데이터셋
        self.stakeholder_dataset = None     # 이해관계자 데이터셋

        self.client = get_openai_client()