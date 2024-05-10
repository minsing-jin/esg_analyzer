from abc import ABC, abstractmethod
from typing import List
import os, json
import pandas as pd
from dotenv import load_dotenv
# from openai import OpenAI
from google.oauth2 import service_account
import gspread
from khuthon.base import BASE
from gspread_dataframe import get_as_dataframe


class GoogleSheetLoadPreprocessing(BASE):
    def __init__(self):
        super().__init__()
        load_dotenv()       # Load environment variables from .env file

        __credentials = service_account.Credentials.from_service_account_file(
            os.environ.get("GOOGLE_ACCOUNT_CREDENTIAL_PATH"))
        __scoped_credentials = __credentials.with_scopes(
            [
                'https://www.googleapis.com/auth/spreadsheets',
            ])
        # Google Spread Sheet API
        self._gc = gspread.Client(auth=__scoped_credentials)

    def run_sheet_load_preprocessing(self):
        self.load_dataset()
        self.extract_most_harm_industry()
        return self.query_generation()

    def load_dataset(self):
        datasets_name_lst = ["산업별온실가스배출", "도시별시가지오염도", "world_carbon_dioxide_emission_estimates",
                             "world_land", "world_Threatned_species", "world_water_and_sanitaion_services"]
        df_dic = {}
        # 사용자에서 측정해서 올린 데이터셋을 불러옴.
        doc = self._gc.open_by_url(os.environ.get("STANDARD_GOOGLE_SPREAD_SHEET_URL"))

        # TODO: null column 제거 -> 없다고 가정해야할듯
        for name in datasets_name_lst:
            sheet = doc.worksheet(name)
            stockcode = get_as_dataframe(worksheet=sheet)
            df_dic[name] = stockcode
        self.start_dataset_dict = df_dic
        assert len(self.start_dataset_dict) == len(datasets_name_lst), "The number of datasets is not equal to the number of datasets in the list"

    # TODO: 관점별로 나눠서 gpt 결과물 추출 및 루커 스튜디오 반영 -> 대시보드에 나타낼 데이터셋 만들어서 upload dataset
    def upload_dataset(self):
        """Upload the dataset to the google sheet
        참고링크: https://velog.io/@king/python-spreadsheet
        upload 주의사항:
        1. 업로드 전에 null값 처리
        2. 업로드 전에 sheet를 clear해야함 -> 그래야 반영가능
        """
        sheet = self._gc.open_by_url(os.environ.get("STANDARD_GOOGLE_SPREAD_SHEET_URL"))

        worksheet = sheet.worksheet("first_dataset")
        worksheet.clear()  # Clear the worksheet before updating it
        worksheet.update([self.start_dataset_dict.columns.values.tolist()] + self.start_dataset_dict.values.tolist())

    def extract_most_harm_industry(self):
        industry = self.start_dataset_dict["산업별온실가스배출"]

        return industry[industry[2021] == max(industry[2021][3:])]["분야 및 연도"]

    # def query_generation(self):
    #     industry = self.extract_most_harm_industry()
    #     sys = f"""너는 구글에 검색어를 추천해주는 helpful assistant야.
    #     가장 많은 온실가스를 배출하는 산업은 {industry}이야.
    #     이 산업이 왜 온실가스를 제일 많이 배출하는지 네이버 뉴스 기사를 검색할 예정이야.
    #     다음 산업이 왜 가장 대기오염물질을 많이 배출하는 문제 원인을 잘 파악할 수 있는 네이버 검색query top-3개를 만들어줘.
    #     검색어의 조건: \n
    #     검색어의 형태는 string이며 long한 명사구이고 검색어만 출력해. 검색어에는 {industry}이라는 단어가 포함되어야해.
    #     검색어는 json format에 리스트로 들어갈거야."""
    #     user = """
    #     ------output format------
    #     ```json
    #     {"추천검색어":
    #     [
    #         "검색어1",
    #         "검색어2",
    #         ...
    #     ]}
    #     ```
    #     """
    #     try:
    #         response = self.client.chat.completions.create(
    #             model="gpt-3.5-turbo-0125",
    #             response_format={'type': "json_object"},
    #             messages=[
    #                 {"role": "system", "content": sys},
    #                 {"role": "user", "content": user}
    #             ]
    #         )
    #         result = json.loads(response.choices[0].message.content)
    #         return result
    #     except json.JSONDecodeError as e:
    #         print("Error parsing JSON: ", e)
    #         return "No category"  # or handle the error appropriately

    def query_generation(self):
        sys = f"""너는 친환경 주식관련 뉴스 검색어를 추천해주는 helpful assistant야.
        너는 검색어를 총 3개를 추천할거야. 
        첫번째는 esg, 기후변화 대응 관련 사업을 트랜드로 확장하고 있는 기업관련을 주식 검색어로 만들어줘.
        두번째는 esg 관련, 친환경 관련 주식 테마에 대한 관련 검색어로 만들어줘.
        세번째는 영향력 있는 인물에 관점으로 Esg, 기후변화 대응친환경 이슈에 관한 유명인에 대한 검색어를 만들어줘.
        """
        user = """
        ------output format------
        ```json
        {"추천검색어": 
        [
            "검색어1",
            "검색어2",
            "검색어3"
        ]}
        ```
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={'type': "json_object"},
                messages=[
                    {"role": "system", "content": sys},
                    {"role": "user", "content": user}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError as e:
            print("Error parsing JSON: ", e)
            return "No category"  # or handle the error appropriately

    def pandas_ai_eda(self, sheet_name: str, sheet_range: str):
        pass



    # # TODO: 나중에 ㄱㄱ
    # # TODO: refactoring하자..... -> 함수형 프로그래밍 데코레이터로 absa prompt keyword cloud prompt등등을 동시에 진행할 수 있게 만들기
    # # absa_prompts에 프롬프트를 넣어두기만 해도 자동으로 불러와짐. -> 상대경로 코드로 만들어주는것
    # def call_prompts(self):
    #     prompt = {}
    #     def absa_prompt():
    #         root_dir = '../Prompt_insight_extraction/prompt/absa_prompts'
    #         call_prompt = {}        # TODO: 왜 os walk가 안되는거지? -> 오타 이슈
    #
    #         for (root, dirs, files) in os.walk(root_dir):
    #             if len(files) > 1:
    #                 for file_name in files:
    #                     if 'system_prompt' in file_name:
    #                         call_prompt["system_prompt"] = open(root + '/' + file_name, 'r').read()
    #                     elif 'user_prompt' in file_name:
    #                         call_prompt["user_prompt"] = open(root + '/' + file_name, 'r').read()
    #             else:
    #                 raise FileNotFoundError(f"There is {len(files)} file that is deficient in the directory\n"
    #                                         f"The error is caused by the absence of a system prompt or user prompt\n"
    #                                         f"Here is problem root {root}{dirs}\n")
    #         return call_prompt
    #
    #     prompt['absa_prompt'] = absa_prompt()
    #     return prompt
    #
    #
    #
    #
