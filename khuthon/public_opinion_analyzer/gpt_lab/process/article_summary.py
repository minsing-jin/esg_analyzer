import json
from khuthon.base import BASE

class ArticleSummary(BASE):
    def __int__(self):
        pass

    def sys_prompt_article_summary(self):
        sys_prompt = (f""" 너는 주식투자 분석 helpful assistant야.
          제시된 뉴스 기사를 요약할거야. 요약은 주식 투자의 관점에서 어떻게 투자를 하면 좋을지애 대한 관점으로
           핵심을 요약해줘. 단 character가 50000 이내로 요약해야해.\n
          """)
        return sys_prompt

    def user_prompt_article_summary(self, title, media_outlet, body):
        user_prompt = f"""
          아래는 뉴스 기사를 요약해 \n

          News title: {title}\n
          News media outlet{media_outlet}\n\n

          News body: {body}
          """
        return user_prompt

    def article_summarize(self, row):
        response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": self.sys_prompt_article_summary()},
                    {"role": "user",
                     "content": self.user_prompt_article_summary(row['title'], row['media_outlet'], row['Body'])}
                ]
            )
        return response.choices[0].message.content