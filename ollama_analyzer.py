import json
import re
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
    print(len(info))
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
        promptemotion=f'''
        分析以下评论{items['content']}针对{topic} 的主观性强度，回复为且仅为一个保留两位小数的从0到1浮点数，1代表最主观，0代表最客观
                        '''
        promptstance=f'''
        分析以下评论{items['content']}针对{items['title']} 的态度，回复为且仅为一个保留两位小数的从-1到1浮点数，1代表最正面，0代表最负面
                        '''
        promptreasons=f'''
        分析以下评论{items['content']}针对{items['title']} 的主要观点和论据，回复为且仅为一个python列表格式字符串，每一个元素代表一个论据
                        '''
        promptrelevence=f'''
        分析以下评论{items['content']}针对{topic} 的相关性，回复为且仅为一个保留两位小数的从0到1浮点数，1代表最相关，0代表完全不相关
                        '''
        Okay=False
        while(not Okay):
            try:
                processed['stance']=eval(ollama.chat(model='qwen:14b',messages=[{'role': 'user', 'content': promptstance}])['message']['content'])
                processed['emotion'] = eval(ollama.chat(model='qwen:14b', messages=[{'role': 'user', 'content': promptemotion}])['message']['content'])
                processed['reasons'] = eval(ollama.chat(model='qwen:14b', messages=[{'role': 'user', 'content': promptreasons}])['message']['content'])
                processed['relevance'] = eval(ollama.chat(model='qwen:14b', messages=[{'role': 'user', 'content': promptrelevence}])['message']['content'])
            except Exception as e:
                print(e)
            else:
                Okay=True
        #prompt=f'''
        #    请对下列评论进行分析，以json格式输出。话题是{topic}json格式输出中应当包括以下元素： 'stance'(用户的立场，一个-1到1的值，反应用户对议题的观点是正面还是负面的)
        #    'emotion'反应用户的情感强度，一个0到1的三位浮点数，1代表情感最强 'reasons'一个列表，包含用户支撑其观点的主要依据，每句话20字以内，不要超过5句子,
        #    你要分析的评论是:{items['title']},{items['content']},{items['date_and_location']},json文本要合法，不能添加任何注释，不能漏加逗号
        #'''
        #print(prompt)
        #okay=False
        #while(not okay):
        #    okay=True
        #    response=ollama.chat(model='qwen:14b', messages=[{'role': 'user', 'content': prompt}])
        #    try:
        #        processed=extract_json(response['message']['content'])
        #    except Exception as e:
        #        print(e)
        #        okay=False

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
        # 拆分时间与地点信息：中文部分作为 location，非中文部分去空格后作为 date
        raw_date_loc = items['date_and_location']
        # 提取所有中文字符作为地点字符串
        location = ''.join(re.findall(r'[\u4e00-\u9fff]', raw_date_loc))
        # 去除中文后，再去掉剩余空白字符作为日期字符串
        no_chinese = re.sub(r'[\u4e00-\u9fff]', '', raw_date_loc)
        cleaned_date = ''.join(no_chinese.split())
        processed['location'] = location[-2:]
        processed['date'] = cleaned_date
        ans.append(processed)
        print(ans)
    with open(f'./result/{pos}example.json', 'w', encoding='utf-8') as f:
        json.dump(ans, f, ensure_ascii=False, indent=4)
if __name__=='__main__':
    ollama_analyzer('英伟达是泡沫吗','note1764233755')