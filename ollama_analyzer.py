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
    data={}
    if match:
        json_str = match.group(1).strip()
        rmvptn=r'\s*//.*$'
        json_str = re.sub(rmvptn, '', json_str,flags=re.MULTILINE)
        json_str = json_str.replace("'",'"')
        data=json.loads(json_str)
    else:
        raise TypeError
    return data
def ollama_analyzer(topic,pos):
    f=openfile(f'./data/{pos}.jsonl')
    ans=[]
    for items in f:
        processed={}
        processed['likes'] = items['likes']
        processed['comment_num'] = len(items['comments'])
        prompt=f'''
            请对下列评论进行分析，以json格式输出。话题是{topic}json格式输出中应当包括以下元素： 'stance'(用户的立场，一个-1到1的值，反应用户对议题的观点是正面还是负面的)
            'emotion'反应用户的情感强度，一个0到1的三位浮点数，1代表情感最强 'reasons'一个列表，包含用户支撑其观点的主要依据，每句话20字以内，不要超过5句子,'location',一个词，表示推文发出的省份或国家，港澳台为‘香港’‘澳门’‘台湾’,如果没有输出‘未知’
            你要分析的评论是:{items['title']},{items['content']},{items['date_and_location']},json文本要合法，不能添加任何注释，不能漏加逗号
        '''
        print(prompt)
        okay=False
        while(not okay):
            okay=True
            response=ollama.chat(model='qwen:7b', messages=[{'role': 'user', 'content': prompt}])
            try:
                processed=extract_json(response['message']['content'])
            except Exception as e:
                print(e)
                okay=False

        # 以下为对每条评论进行逐条情感与立场分析的代码。
        # 目前阶段只分析主帖，因此整段逻辑暂时注释掉，避免额外的模型调用和耗时。
        #
        # comments=[]
        # for comment in items['comments']:
        #     prompt=f'''
        #         请对下列评论进行分析，以json格式输出，话题是{topic},评论是{comment}内容包括'stance'(用户的立场，一个-1到1的值，反应用户对议题的观点是正面还是负面的)
        #         'emotion'反应用户的情感强度，一个0到1的三位浮点数，1代表情感最强。json文本要合法，不能添加任何注释，不能漏加逗号
        #         '''
        #     print(prompt)
        #     okay=False
        #     p={}
        #     while(not okay):
        #         okay=True
        #         response=ollama.chat(model='qwen:7b',messages=[{'role': 'user', 'content': prompt}])
        #         try:
        #             p=extract_json(response['message']['content'])
        #         except Exception as e:
        #             print(e)
        #             okay=False
        #     comments.append(p)
        #
        # processed['comments']=comments

        # 当前阶段仅保留原始评论列表，方便后续如需再次分析时使用
        processed['comments'] = items['comments']
        ans.append(processed)
        print(ans)
    with open(f'./result/{pos}.json', 'w', encoding='utf-8') as f:
        json.dump(ans, f, ensure_ascii=False, indent=4)
if __name__=='__main__':
    ollama_analyzer('英伟达是泡沫吗','note1764233755')