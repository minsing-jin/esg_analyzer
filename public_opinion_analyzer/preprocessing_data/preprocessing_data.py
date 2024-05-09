import pandas as pd

if __name__ == '__main__':
    sliced_comments_df = pd.read_csv('/Users/jinminseong/Desktop/naver_comments.csv')
    sliced_comments_df = sliced_comments_df.groupby('ArticleID').head(100)
    sliced_comments_df.to_csv('/Users/jinminseong/Desktop/#1_sliced_naver_comments.csv', index=False)
