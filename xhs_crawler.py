from DrissionPage.errors import ElementNotFoundError
from DrissionPage import ChromiumPage, ChromiumOptions
import json
import time

def append_to_json_file(data,filename):
    with open(filename, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write('\n')



def crawl_xhs(keyword,num,filename=f'note{int(time.time())}'):
    pos=f'./data/{filename}.jsonl'
    with open(pos, 'w', encoding='utf-8') as f:
        pass
    options = ChromiumOptions()
    options.headless(True)
    options.set_argument('--no-sandbox')
    options.set_argument("--disable-gpu")
    options.set_argument('--start-maximized')
    options.set_argument('--window-size', '1200,1000')
    dp = ChromiumPage(options)
    try:
        dp.get(f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=unknown&type=51")
        time.sleep(1)
        lst=[]
        t=time.time()
        while len(lst)<int(num) and time.time()-t<900:
            dp.wait.ele_displayed('.cover mask ld')
            elements = dp.eles('.cover mask ld')
            for element in elements:
                try:
                    lst.append(element.attrs.get('href'))
                except:
                    continue
            lst=list(set(lst))
            dp.scroll()
            time.sleep(0.1)
        #print(lst)
        #res=[]
        for urls in lst:
            dp.get(f'https://www.xiaohongshu.com{urls}')
            time.sleep(1)
            #print(urls)
            dp.wait.ele_displayed('.comment-item')
            comment_list=dp.eles('.comment-item',timeout=0.2)
            comments=[]
            dp.wait.ele_displayed('.slider-container')
            try:
                img=dp.ele('.slider-container',timeout=0.2).eles('tag:img')
            except ElementNotFoundError:
                img=[]
            images=[]
            for comment in comment_list:
                comments.append({'username':comment.ele('.author').text,'comment':comment.ele('.note-text').text})
            for image in img:
                images.append(image.attrs.get('src'))
            info={'username': dp.ele('.username').text,
                  'title': dp.ele('.title').text,
                  'content': dp.ele('.note-text').text,
                  'image': images,
                  'date_and_location':dp.ele('.bottom-container').text,
                  'likes': int(dp.ele('.interact-container',timeout=0.2).ele('.count').text),
                  'comments': comments
                  }
            #res.append(info)
            append_to_json_file(info,pos)
        #with open (pos,'w',encoding='utf-8') as f:
        #    json.dump(res,f,ensure_ascii=False,indent=2)
    finally:
        try:
            dp.quit()
        except:
            pass

if __name__=='__main__':
    crawl_xhs('英伟达是泡沫吗',10)