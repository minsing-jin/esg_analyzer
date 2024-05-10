import json
from khuthon.base import BASE

class Comment(BASE):
    def __int__(self):
        pass

    def sys_prompt_article_summary(self):
        sys_prompt = (f""" 너는 주식투자 분석 helpful assistant야.
          제시된 댓글에서 주제에 대한 감정분석과 .\n
          """)
        return sys_prompt

    def user_prompt_article_summary(self, comment):
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