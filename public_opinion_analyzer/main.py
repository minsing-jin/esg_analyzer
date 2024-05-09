from public_opinion_analyzer.crawler.base_crawler import SearchEngineNewsCrawler
import pandas as pd
from copy import deepcopy
from public_opinion_analyzer.tools.convert_time_to_iso8601 import convert_string_time_to_iso8601


if __name__ == '__main__':
    naver_base_crawler = SearchEngineNewsCrawler()
    info_main = input("=" * 50 + "\n" + "입력 형식에 맞게 입력해주세요." + "\n" + " 시작하시려면 Enter를 눌러주세요." + "\n" + "=" * 50)

    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")
    query = input("검색어 입력: ")
    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")  # 관련도순=0  최신순=1  오래된순=2
    s_date = input("시작날짜 입력(2019.01.04):")  # 2019.01.04
    e_date = input("끝날짜 입력(2019.01.05):")  # 2019.01.05

    df = naver_base_crawler.fetch_news_content(maxpage, query, sort, s_date, e_date)

    # Preprocessing Comments
    df['Comments_tuples'] = df['naver_news_link'].apply(naver_base_crawler.get_comments)
    df['Body'] = df['naver_news_link'].apply(naver_base_crawler.get_content)

    flatten_df = df['Body'].apply(pd.Series)

    df = pd.concat([flatten_df, df[['Comments_tuples']]], axis=1)

    articles = deepcopy(df)
    articles['ArticleID'] = articles.apply(naver_base_crawler.creat_uuid, axis=1)

    Comments = deepcopy(articles)
    Comments = Comments[Comments['Comments_tuples'].apply(lambda x: len(x) > 0)]
    Comments = Comments.explode('Comments_tuples')
    Comments[['CommentID','Comment_person','CommentDate', 'CommentText']] = Comments['Comments_tuples'].apply(pd.Series)
    Comments = Comments.reset_index(drop=True).drop('Comments_tuples', axis=1)

    articles = articles[['ArticleID', 'PublicationDate', 'title', 'media_outlet', 'link', 'Body', 'Comments_tuples']]
    Comments = Comments[['CommentID', 'ArticleID', 'Comment_person', 'CommentDate', 'CommentText', 'PublicationDate', 'title', 'media_outlet', 'link', 'Body']]
    comments_col = Comments.columns.tolist()
    articles_col = articles.columns.tolist()
    articles['PublicationDate'] = articles['PublicationDate'].apply(convert_string_time_to_iso8601)

    articles.to_csv('/Users/jinminseong/Desktop/naver_articles.csv', index=False)
    Comments.to_csv('/Users/jinminseong/Desktop/naver_comments.csv', index=False)
