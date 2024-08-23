import pandas as pd


def main():
    train_df = pd.read_csv('./data/uncased_train_origin.csv', index_col=0)
    test_df = pd.read_csv('./data/uncased_test_origin.csv', index_col=0)

    new_train_df = train_df.drop(train_df[(train_df['업종'] == '교육') | (train_df['업종'] == '기타소비') | (train_df['업종'] == '배달') | (train_df['업종'] == '보험') | (train_df['업종'] == '생활서비스')| (train_df['업종'] == '세금/공과금') | (train_df['업종'] == '여행/숙박') | (train_df['업종'] == '통신')].index, inplace=False)
    new_test_df = test_df.drop(test_df[(test_df['업종'] == '교육') | (test_df['업종'] == '기타소비') | (test_df['업종'] == '배달') | (test_df['업종'] == '보험') | (test_df['업종'] == '생활서비스')| (test_df['업종'] == '세금/공과금') | (test_df['업종'] == '여행/숙박') | (test_df['업종'] == '통신')].index, inplace=False)

    new_train_df.to_csv('./data/uncased_train.csv')
    new_test_df.to_csv('./data/uncased_test.csv')


if __name__ == '__main__':
    main()