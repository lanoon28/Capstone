import pandas as pd
import re
import warnings
warnings.filterwarnings(action = 'ignore')
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer # TF-IDF 벡터화
from sklearn.linear_model import LogisticRegression # 이진분류 알고리즘
from sklearn.model_selection import GridSearchCV # 하이퍼 파라미터 최적화?
from konlpy.tag import Okt # 형태소 분석기
import time

start_time = time.time()
okt = Okt()

# Read excel
train_df = pd.read_excel('Comments.xlsx')

# 결측값 처리
train_df = train_df[train_df['text'].notnull()]
train_df['text'] = train_df['text'].apply(lambda x: re.sub(r'[^ ㄱ-ㅣ 가-힣] + ', " ", x))

text = train_df['text']
score = train_df['score']

train_x, test_x, train_y, test_y = train_test_split(text, score, test_size=0.92, random_state=0)

tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)
tfv.fit(train_x)
tfv_train_x = tfv.transform(train_x)

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
read_df = read_df.merge(react_df, how = 'left', left_on = 'Idx', right_on = 'idx')

columns = ['ID', 'Comment', 'react']

df = read_df[columns]

print(df)
