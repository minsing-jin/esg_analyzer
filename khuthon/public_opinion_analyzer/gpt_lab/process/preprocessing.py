import pandas as pd

class Preprocessing:
    def __init__(self, gpt_df):
        self.gpt_df = None

    def preprocessiing_pipeline(self):
        gpt_df = self.gpt_df
        def splited(row):
            sperate_dic1 = {}
            sperate_dic2 = {}

            for key, value in row.items():
                if key == '2 기업 추출':
                    sperate_dic1[key] = value
                else:
                    sperate_dic2[key] = value

            return sperate_dic1, sperate_dic2

        def distrbuted(row):
            corporation = []
            score = []
            if row == {}:
                return corporation, score
            elem = row['2 기업 추출']

            for key, value in elem.items():
                corporation.append(key)
                score.append(value)
            return corporation, score

        gpt_df['insights'] = gpt_df['insights'].apply(ast.literal_eval)
        temp = gpt_df['insights'].apply(splited)
        gpt_df['기업추출'], gpt_df['insights1'] = zip(*temp)

        temp_insight = pd.json_normalize(gpt_df['insights1'])
        temp_insight2 = gpt_df['기업추출'].apply(distrbuted)
        gpt_df['기업'], gpt_df['score'] = zip(*temp_insight2)

        gpt_df = pd.concat([gpt_df, temp_insight], axis=1)

        comment = gpt_df.drop(
            ['insights', 'Body', '기업추출', 'insights1', '기업', 'score', '1 esg관련주식 유망요소, 위협요소추출', '3 주식 트랜드 분석',
             '4 esg 관련 주식 이해관계자 인물, 기관 기업 추출', '5 esg 관련 테마 추출'], axis=1)

        corp = gpt_df.drop(['insights', 'Body', '기업추출', 'insights1', 'score', '1 esg관련주식 유망요소, 위협요소추출', '3 주식 트랜드 분석',
                            '4 esg 관련 주식 이해관계자 인물, 기관 기업 추출', '5 esg 관련 테마 추출'], axis=1)

        score = gpt_df.drop(['insights', 'Body', '기업추출', 'insights1', '기업', '1 esg관련주식 유망요소, 위협요소추출', '3 주식 트랜드 분석',
                             '4 esg 관련 주식 이해관계자 인물, 기관 기업 추출', '5 esg 관련 테마 추출'], axis=1)

        esg_threaten = gpt_df.drop(
            ['insights', 'Body', '기업추출', 'insights1', 'score', '3 주식 트랜드 분석', '4 esg 관련 주식 이해관계자 인물, 기관 기업 추출',
             '5 esg 관련 테마 추출'], axis=1)

        trend = gpt_df.drop(['insights', 'Body', '기업추출', 'insights1', 'score', '1 esg관련주식 유망요소, 위협요소추출',
                             '4 esg 관련 주식 이해관계자 인물, 기관 기업 추출', '5 esg 관련 테마 추출'], axis=1)

        stakeholder = gpt_df.drop(
            ['insights', 'Body', '기업추출', 'insights1', 'score', '1 esg관련주식 유망요소, 위협요소추출', '3 주식 트랜드 분석',
             '5 esg 관련 테마 추출'], axis=1)

        theme = gpt_df.drop(['insights', 'Body', '기업추출', 'insights1', 'score', '1 esg관련주식 유망요소, 위협요소추출', '3 주식 트랜드 분석',
                             '4 esg 관련 주식 이해관계자 인물, 기관 기업 추출'], axis=1)

        corp = corp.explode('기업')
        score = score.explode('score')
        assert len(corp) == len(score)
        corp = pd.concat([corp, score['score']], axis=1)

        from ast import literal_eval
        def safe_literal_eval(s):
            try:
                # Only evaluate if string looks like a Python literal
                if s.startswith(('[', '{')) and s.endswith((']', '}')):
                    return literal_eval(s)
                else:
                    return []
            except ValueError:
                return []

        comment['comments'] = comment['comments'].apply(safe_literal_eval)
        esg_threaten = esg_threaten['1 esg관련주식 유망요소, 위협요소추출'].apply(safe_literal_eval)
        stakeholder['4 esg 관련 주식 이해관계자 인물, 기관 기업 추출'] = stakeholder.apply(safe_literal_eval)
        theme['5 esg 관련 테마 추출'] = theme.apply(safe_literal_eval)

        comment = comment[comment['comments'].apply(lambda x: len(x) > 0)]
        esg_threaten = esg_threaten[esg_threaten.apply(lambda x: len(x) > 0)]
        trend = trend[trend['3 주식 트랜드 분석'].apply(lambda x: len(x) > 0)]
        stakeholder = stakeholder[stakeholder['4 esg 관련 주식 이해관계자 인물, 기관 기업 추출'].apply(lambda x: len(x) > 0)]
        theme = theme[theme['5 esg 관련 테마 추출'].apply(lambda x: len(x) > 0)]

        stakeholder = stakeholder.explode('4 esg 관련 주식 이해관계자 인물, 기관 기업 추출')

        comment = comment.explode('comments')
        esg_threaten = esg_threaten.explode('1 esg관련주식 유망요소, 위협요소추출')
        trend = trend.explode('3 주식 트랜드 분석').dropna()
        theme = theme.explode('5 esg 관련 테마 추출')

        return comment, corp, esg_threaten, trend, stakeholder, theme
