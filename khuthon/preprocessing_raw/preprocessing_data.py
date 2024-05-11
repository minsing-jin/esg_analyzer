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
    def upload_dataset(self, df: pd.DataFrame, sheet_name: str):
        """Upload the dataset to the google sheet
        참고링크: https://velog.io/@king/python-spreadsheet
        upload 주의사항:
        1. 업로드 전에 null값 처리
        2. 업로드 전에 sheet를 clear해야함 -> 그래야 반영가능
        """
        path = "/Users/jinminseong/Desktop/khuthon-422909-b0604f438115.json"
        load_dotenv()  # Load environment variables from .env file

        # Use the environment variable to get the path
        credentials_path = os.environ.get(path)
        if credentials_path is None:
            raise ValueError("Google application credentials path not found in environment variables.")

        __credentials = service_account.Credentials.from_service_account_file(credentials_path)

        __scoped_credentials = __credentials.with_scopes(
            [
                'https://www.googleapis.com/auth/spreadsheets',
            ])
        # Google Spread Sheet API
        self._gc = gspread.Client(auth=__scoped_credentials)

        sheet = self._gc.open_by_url(os.environ.get("STANDARD_GOOGLE_SPREAD_SHEET_URL"))

        worksheet = sheet.worksheet("first_dataset")
        worksheet.clear()  # Clear the worksheet before updating it
        worksheet.update([self.start_dataset_dict.columns.values.tolist()] + self.start_dataset_dict.values.tolist())

    def extract_most_harm_industry(self):
        industry = self.start_dataset_dict["산업별온실가스배출"]

        return industry[industry[2021] == max(industry[2021][3:])]["분야 및 연도"]

    def query_optimization(self, query: str):
        sys = f"""너는 친환경 주식관련 뉴스 검색어를 추천해주는 helpful assistant야.
        너는 검색어를 총 3개를 추천할거야. {query}에 대한 관련 검색어를 만들어줘.
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
