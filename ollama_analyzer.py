#from xhs_crawler import crawl_xhs
import json
import ollama
#key=input()
#num=int(input())
#path=crawl_xhs(key,num)
'''
def analysis(path):
    with open(path,'r',encoding='utf-8') as f:
        info=json.loads(f.read())
    print(info)
    response=ollama.generate(model='qwen:7b',prompt=f'对下面的内容进行分析{info}')
    print(response['response'])
if __name__ == '__main__':
    analysis('notes1764155199.6800692.json')
'''
from wordcloudgenerator import *
