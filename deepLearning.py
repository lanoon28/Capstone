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

# Train / Test 분리
train_x, test_x, train_y, test_y = train_test_split(text, score, test_size=0.9, random_state=0)

tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)
tfv.fit(train_x)
tfv_train_x = tfv.transform(train_x)

load_model = joblib.load('newDeep.pkl')


tfv_test_x = tfv.transform(test_x)
# test_predict = grid_cv.best_estimator_.score(tfv_test_x,test_y)
#test_predict = load_model.best_estimator_.predict(tfv_test_x)

test_input = pd.read_excel('44.xlsx')

test_df = test_input[test_input['text'].notnull()]
test_df['text'] = test_df['text'].apply(lambda x: re.sub(r'[^ ㄱ-ㅣ 가-힣] + ', " ", x))

text_r = train_df['text']
test = tfv.transform(text_r)

print(test)

predict = load_model.best_estimator_.predict(test)

print(predict[1232])

for i in range(len(predict)):
    if (predict[i] == 0):
        print('부정')
    else:
        print('긍정')

end_time = time.time()
print(end_time - start_time)

