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

warnings.filterwarnings(action = 'ignore')
start_time = time.time()
okt = Okt()

load_model = joblib.load('newDeep.pkl')

train_df = pd.read_excel('44.xlsx')

train_df = train_df[train_df['Comment'].notnull()]

train_df['Comment'] = train_df['Comment'].apply(lambda x : re.sub(r'[^ ㄱ-ㅣ가-힣]+', " ", x))

text = train_df['Comment']

train_x = text

print(train_x[0])
print(type(train_x))
tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)
tfv.fit(train_x)
tfv_train_x = tfv.transform(train_x)

print(tfv_train_x.toarray())


print(tfv_train_x)

end_time = time.time()
print(end_time-start_time)
#test_predict = load_model.best_estimator_.predict(tfv_train_x)

#print(test_predict)

