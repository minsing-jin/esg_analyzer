import requests, json
import pandas as pd
import time
from public_opinion_analyzer.gpt_lab.process1.base import BaseCityExtraction

class GetLocation(BaseCityExtraction):
    def __init__(self):
        super().__init__()
        self.url = 'https://dapi.kakao.com/v2/local/search/address.json?query='
        self.headers

    def get_location(self, address):
        pass

    def sys_prompt_city_extraction(self):
        pass

    def user_prompt_city_extraction(self):
        pass


    def get_location(self, address):
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
        # 'KaKaoAK '는 그대로 두시고 개인키만 지우고 입력해 주세요.
        # ex) KakaoAK 6af8d4826f0e56c54bc794fa8a294
        headers = {"Authorization": "KakaoAK 18fa7c3977bc313b0659499b554180de"}
        api_json = json.loads(str(requests.get(url, headers=headers).text))
        #   address = api_json['documents'][0]['address']
        return api_json


