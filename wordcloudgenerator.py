import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
import json

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def preprocess_text(text):
    """文本预处理"""
    # 去除URL
    text = re.sub(r'http\S+', '', text)
    # 去除@提及
    text = re.sub(r'@\S+', '', text)
    # 去除特殊字符，保留中文、英文、数字
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9#]', ' ', text)
    return text.strip()


def extract_hashtags(text):
    """提取hashtag"""
    hashtags = re.findall(r'#([^\s#]+)', text)
    return [tag for tag in hashtags if len(tag) > 0]


def extract_keywords(texts, top_k=50):
    """提取关键词"""
    all_text = ' '.join(texts)

    # 使用TF-IDF提取关键词
    keywords_tfidf = jieba.analyse.extract_tags(
        all_text,
        topK=top_k,
        withWeight=True
    )

    # 使用TextRank提取关键词
    keywords_textrank = jieba.analyse.textrank(
        all_text,
        topK=top_k,
        withWeight=True
    )

    # 合并结果
    keyword_weights = {}
    for word, weight in keywords_tfidf + keywords_textrank:
        if word in keyword_weights:
            keyword_weights[word] += weight
        else:
            keyword_weights[word] = weight

    return keyword_weights


def process_social_media_data(tweets_comments):
    """处理社交媒体数据"""
    hashtags = []
    cleaned_texts = []

    for text in tweets_comments:
        # 提取hashtag
        tags = extract_hashtags(text)
        hashtags.extend(tags)

        # 清洗文本
        cleaned = preprocess_text(text)
        if cleaned:
            cleaned_texts.append(cleaned)

    # 提取关键词
    keywords = extract_keywords(cleaned_texts)

    return hashtags, keywords


def create_wordcloud(keyword_weights):
    """创建词云图"""
    wordcloud = WordCloud(
        font_path='simhei.ttf',
        width=800,
        height=600,
        background_color='white',
        max_words=100,
        colormap='viridis'
    )

    # 生成词云
    wordcloud.generate_from_frequencies(keyword_weights)
    return wordcloud


def plot_results(wordcloud, hashtags, keywords):
    """可视化结果"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))

    # 词云图
    ax1.imshow(wordcloud, interpolation='bilinear')
    ax1.set_title('关键词词云')
    ax1.axis('off')

    # 热门hashtag
    hashtag_counts = Counter(hashtags).most_common(10)
    if hashtag_counts:
        tags, counts = zip(*hashtag_counts)
        ax2.barh(range(len(tags)), counts)
        ax2.set_yticks(range(len(tags)))
        ax2.set_yticklabels(tags)
    ax2.set_title('热门Hashtag')
    ax2.invert_yaxis()

    # 热门关键词
    top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]
    if top_keywords:
        words, weights = zip(*top_keywords)
        ax3.barh(range(len(words)), weights)
        ax3.set_yticks(range(len(words)))
        ax3.set_yticklabels(words)
    ax3.set_title('热门关键词')
    ax3.invert_yaxis()

    plt.tight_layout()
    plt.show()
def generate_wordcloud(path):
    text = []
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    decoder=json.JSONDecoder()
    pos=0
    content_length=len(content)
    info=[]
    while pos < content_length:
        if pos>content_length:
            break
        obj,pos=decoder.raw_decode(content,idx=pos)
        pos+=1
        print(obj)
        info.append(obj)
        info.append(obj)
    for items in info:
        text.append(items['content'])
        text.append(items['title'])
        for comment in items['comments']:
            text.append(comment['comment'])
    hashtags, keywords = process_social_media_data(text)
    wordcloud = create_wordcloud(keywords)
    plot_results(wordcloud, hashtags, keywords)

# 使用示例
if __name__ == "__main__":
    path = 'note1764233755.jsonl'
    generate_wordcloud(path)