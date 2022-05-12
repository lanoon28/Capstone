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
warnings.filterwarnings(action = 'ignore')

okt = Okt()

m = joblib.load('deep.pkl')

tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)
tfv.fit(train_x)
tfv_train_x = tfv.transform(train_x)


input_text = pd.read_excel('tt')

input_text = re.compile(r'[ㄱ-ㅣ가-힣]+').findall(input_text)
input_text = [" ".join(input_text)]

st_tfidf = tfv.transform(input_text)

st_predict = m.best_estimator_.predict(st_tfidf)


if(st_predict == 0):
    print('예측 결과: ->> 부정 감성')
else :
    print('예측 결과: ->> 긍정 감성')