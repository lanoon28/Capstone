from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
import pandas as pd

class wordcreate:
    global okt
    okt = Okt()

    def __init__(self):
        return 0

    def create(loadfile):
        openex = pd.read_excel(loadfile)
        allword = openex['Comment']

        word = []

        for i in range(len(allword)):
            nouns = okt.nouns(allword[i])  # 명사만 추출
            word = nouns + word

        words = [n for n in word if len(n) > 1]  # 단어의 길이가 1개인 것은 제외

        comment = Counter(words)  # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
        co30 = comment.most_common(50)

        wc = WordCloud(font_path='/Library/Fonts/AppleGothic',width=400, height=400, scale=2.0, max_font_size=250)
        gen = wc.generate_from_frequencies(dict(co30))
        plt.figure()
        plt.imshow(gen)

        wc.to_file('word.png')

# 사용법
# 생성
st = wordcreate
st.create('total.xlsx')
# create안에 엑셀위치 + 긍부정만 넣으면됨 긍정이면 '긍정' 부정이면 '부정'
# 혹시 이거 워드클라우드 크기나 이런거 설정필요하면 말하셈