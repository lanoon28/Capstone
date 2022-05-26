import pandas as pd
import warnings
import re
from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import joblib
import time
from sklearn.feature_selection import RFE

warnings.filterwarnings(action='ignore')


class deepLearning:
    def __init__(self):
        pass

    def learning(self):
        okt = Okt()

        train_df = pd.read_excel('Comments.xlsx')

        train_df = train_df[train_df['text'].notnull()]

        train_df['text'] = train_df['text'].apply(lambda x: re.sub(r'[^ ㄱ-ㅣ가-힣]+', " ", x))

        text = train_df['text']
        score = train_df['score']

        train_x, test_x, train_y, test_y = train_test_split(text, score, test_size=0.92, random_state=0)

        tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1, 2), min_df=3, max_df=0.9)
        tfv.fit(train_x)

        load_model = joblib.load('newDeep.pkl')

        test_input = pd.read_excel('craw.xlsx')

        test_df = test_input[test_input['Comment'].notnull()]
        test_df['Comment'] = test_df['Comment'].apply(lambda x: re.sub(r'[^ ㄱ-ㅣ 가-힣] + ', " ", x))

        text_r = test_df['Comment']
        test = tfv.transform(text_r)

        ts_predict = load_model.best_estimator_.predict(test)

        react_df = pd.DataFrame(columns=['idx', 'react'])

        for i in range(len(ts_predict)):
            if (ts_predict[i] == 0):
                react = '부정'
            else:
                react = '긍정'

            react_df = react_df.append(pd.DataFrame([[i, react]], columns=['idx', 'react']), ignore_index=True)

        read_df = pd.read_excel('craw.xlsx')
        # print(read_df,react_df)
        read_df = read_df.merge(react_df, how='left', left_on='no', right_on='idx')

        columns = ['ID', 'Comment', 'react']
        df = read_df[columns]

        df.to_excel('total.xlsx')

    def positive(self):
        self.read = pd.read_excel('total.xlsx')
        self.positive = self.read[self.read['react'] == '긍정']
        self.positive.to_excel('positive.xlsx')

    def negative(self):
        read = pd.read_excel('total.xlsx')
        negative = read[read['react'] == '부정']
        negative.to_excel('negative.xlsx')


