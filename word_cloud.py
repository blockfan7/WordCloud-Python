# 워드 클라우드에 필요한 라이브러리 불러들인다.
from wordcloud import WordCloud
# 조선어 자욘얼어처리 라이브러리 불러온다.
from konlpy.tag import Twitter
# 명사의 출현빈도를 세는 라이브러리 불러온다.
from collections import Counter
# 그래프생성에 필요한 라이브러리 불러온다.
import matplotlib.pyplot as plt
# Flask 웹 서버구축에 필요한 라이브러리 불러온다.
from flask import Flask, request, jsonify

font_path = 'NanumGothic.ttf'

#플라스크 웹 서버객체 생성
app = Flask(__name__)

def get_tags(text, max_count, min_length):
    t = Twitter()
    nouns = t.nouns(text)
    processed = [n for n in nouns if len(n) >= min_length]
    count = Counter(processed)
    result = {}
    for n, c in count.most_common(max_count):
        result[n] = c
    if len(result) == 0:
        result["내용 없음"] = 1
    return result

def make_cloud_image(tags, file_name):
    #만들려는 word cloud의 기본설정을 진행한다.
    word_cloud = WordCloud(
        font_path=font_path,
        width=800,
        height=800,
        background_color="white"
    )
    word_cloud = word_cloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(word_cloud)
    plt.axis("off")
    #만들어진 이미지 객체를 파일형태로 저장한다.

    fig.savefig("outputs/{0}.png".format(file_name))


def process_from_text(text, max_count, min_length, words):
    tags = get_tags(text, max_count, min_length)
    # 단어 가중치 적용
    for n, c in words.items():
        if n in tags:
            tags[n] = tags[n] * int(words[n])

    make_cloud_image(tags, "output")

@app.route("/process", methods = ['GET', 'POST'])
def process():
    content = request.json
    words = {}
    if content['words'] is not None:
        for data in content['words'].values():
            words[data['word']] = data['weight']

    process_from_text(content['text'], content['maxCount'], content['minLength'], words)
    result = {'result':True}
    return jsonify(result)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)

