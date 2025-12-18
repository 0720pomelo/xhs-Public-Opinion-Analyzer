import json
from chinese_summarizer import summarize_sentences
def key_sentence_extraction(path):
    with open(path, 'r', encoding='utf-8') as f:
        data=json.load(f)
    key_sentences=[]
    for items in data:
        try:
            key_sentences+=items['reasons']
        except Exception as e:
            print(e)
    return summarize_sentences(key_sentences, max_sentences=10)

if __name__ == '__main__':
    a=(key_sentence_extraction('./result/note1764233755.json'))
    for i in a :
        print(i)