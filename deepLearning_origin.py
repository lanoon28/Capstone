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

start = time.time()

warnings.filterwarnings(action = 'ignore')

okt = Okt()

train_df = pd.read_excel('Comments.xlsx')

train_df = train_df[train_df['text'].notnull()]

train_df['text'] = train_df['text'].apply(lambda x : re.sub(r'[^ ㄱ-ㅣ가-힣]+', " ", x))

text = train_df['text']
score = train_df['score']

train_x, test_x, train_y, test_y = train_test_split(text, score , test_size=0.92, random_state=0)

tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)
tfv.fit(train_x)
tfv_train_x = tfv.transform(train_x)
clf = LogisticRegression(random_state=0)
# params = {'C': [15, 18, 19, 20, 22]}
# grid_cv = GridSearchCV(clf, param_grid=params, cv=3, scoring='accuracy', verbose=1)
# grid_cv.fit(tfv_train_x, train_y)
# print(grid_cv.best_params_, grid_cv.best_score_)
#
# joblib.dump(grid_cv,'./newDeep.pkl')

load_model = joblib.load('newDeep.pkl')

tfv_test_x = tfv.transform(test_x)
test_predict = load_model.best_estimator_.predict(tfv_test_x)


# input_text = 'ㅅㅂ 이걸 왜 만드냐'
#
# input_text = re.compile(r'[ㄱ-ㅣ가-힣]+').findall(input_text)
# input_text = [" ".join(input_text)]
#
# st_tfidf = tfv.transform(input_text)

#st_predict = load_model.best_estimator_.predict(st_tfidf)

# print('감성 분류 모델의 정확도 : ',round(accuracy_score(test_y, test_predict), 3))
#
# if(st_predict == 0):
#     print('예측 결과: ->> 부정 감성')
# else :
#     print('예측 결과: ->> 긍정 감성')

test_input = pd.read_excel('44.xlsx')

test_df = test_input[test_input['Comment'].notnull()]
test_df['Comment'] = test_df['Comment'].apply(lambda x: re.sub(r'[^ ㄱ-ㅣ 가-힣] + ', " ", x))

text_r = test_df['Comment']
test = tfv.transform(text_r)

ts_predict = load_model.best_estimator_.predict(test)



for i in range(len(ts_predict)):
    if (ts_predict[i] == 0):
        print('부정')
    else:
        print('긍정')

stop = time.time()
print(stop - start)
print(len(ts_predict))

