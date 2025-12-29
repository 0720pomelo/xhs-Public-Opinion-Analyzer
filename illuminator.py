import json
from chinese_summarizer import summarize_sentences
import matplotlib.pyplot as plt
#from matplotlib import font_manager
#import numpy as np
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

def locationcounterwithweights(path):
    with open(path, 'r', encoding='utf-8') as f:
        data=json.load(f)
    locations={}
    for items in data:
        if(len(items['location'])<1 or items['location']=='辑于'):
            continue
        try:
            locations[items['location']]+=(items['likes']+items['comment_num']*5)*items['relevance']
        except KeyError:
            locations[items['location']]=(items['likes']+items['comment_num']*5)*items['relevance']
    return locations


def create_weight_pie_chart(data_dict, title="地址权重占比图", figsize=(12, 8)):
    """
    创建地址权重占比饼图

    参数:
        data_dict: 字典，键为地址，值为权重
        title: 图表标题
        figsize: 图表尺寸
    """
    # 准备数据
    addresses = list(data_dict.keys())
    weights = list(data_dict.values())
    weights=[round(i,2) for i in weights]
    # 计算总权重和占比
    total_weight = sum(weights)
    percentages = [(weight / total_weight) * 100 for weight in weights]

    # 创建标签：地址:权重占比%
    labels = [f"{addr}: {percent:.1f}%"
              for addr, percent in zip(addresses, percentages)]

    # 设置中文字体（如果需要显示中文）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建图表
    fig, ax = plt.subplots(figsize=figsize)

    # 创建饼图
    wedges, texts, autotexts = ax.pie(
        weights,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1},
        textprops={'fontsize': 10}
    )

    # 设置标题
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

    # 确保饼图是圆形
    ax.axis('equal')

    # 添加图例（可选）
    ax.legend(
        wedges,
        [f"{addr}: {weight}" for addr, weight in zip(addresses, weights)],
        title="地址: 权重",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # 调整布局
    plt.tight_layout()
    plt.show()

    # 打印统计信息
    print("=" * 50)
    print("地址权重统计信息:")
    print("=" * 50)
    for i, (address, weight) in enumerate(data_dict.items(), 1):
        print(f"{i:2d}. {address:20s} 权重: {weight}  占比: {percentages[i - 1]:6.2f}%")
    print("-" * 50)
    print(f"总权重: {total_weight}")
    print(f"地址数量: {len(addresses)}")
    print("=" * 50)
if __name__ == '__main__':
    a=(locationcounterwithweights('./result/note1764233755example.json'))
    print(a)
    create_weight_pie_chart(a, title="各地区地址权重分布")