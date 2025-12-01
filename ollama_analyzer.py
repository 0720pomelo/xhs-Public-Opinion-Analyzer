import json
import ollama
def openfile(path):
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
            info.append(obj)
    return info
def extract_json(text):
    import re
    pattern = r"```json(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    data=None
    if match:
        json_str = match.group(1).strip()
        data=json.loads(json_str)
    return data
def ollama_analyzer(topic):
    f=openfile('note1764233755.jsonl')
    ans=[]
    for items in f:
        prompt=f'''
            请以json格式对下列评论进行分析，话题是{topic}json格式输出中应当包括以下元素： 'stance'(用户的立场，一个-1到1的值，反应用户对议题的观点是正面还是负面的)
            'emotion'反应用户的情感强度，一个0到1的三位浮点数，1代表情感最强 'reasons'一个列表，包含用户支撑其观点的主要依据，每句话20字以内，不要超过5句子
            你要分析的评论是:{items['content']},不要在json内部添加任何注释，你输出的json内容必须合法
        '''
        response=ollama.chat(model='qwen:7b', messages=[{'role': 'user', 'content': prompt}])
        ans.append(extract_json(response['message']['content']))
        #print(ans)
ollama_analyzer('英伟达是泡沫吗')