from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def summarize_sentences(sentences: List[str], max_sentences: int = 10) -> List[str]:
    """
    使用 TF‑IDF + 余弦相似度的抽取式摘要（基于 scikit-learn）。

    思路：
    - 用 TF‑IDF 将每个句子表示成向量；
    - 求所有句子向量的“中心”（平均向量）；
    - 计算每个句子与中心的余弦相似度，相似度越高说明越“代表整体内容”；
    - 选取得分最高的 max_sentences 句，并按原始顺序返回。
    """
    # 预处理：去除两端空白，过滤空句
    cleaned: List[str] = []
    seen = set()
    for s in sentences:
        s_clean = (s or "").strip()
        if not s_clean:
            continue
        if s_clean in seen:
            continue
        seen.add(s_clean)
        cleaned.append(s_clean)

    if len(cleaned) <= max_sentences:
        return cleaned

    # 使用 TF‑IDF 将每个句子向量化
    vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
    tfidf_matrix = vectorizer.fit_transform(cleaned)  # shape: (n_sentences, n_features)

    # 计算“文档中心”向量（所有句子向量的平均）
    centroid = tfidf_matrix.mean(axis=0)  # scipy matrix / sparse
    centroid = np.asarray(centroid)       # 转为标准 ndarray 以兼容新版 NumPy / sklearn

    # 每个句子与中心的余弦相似度
    sims = cosine_similarity(tfidf_matrix, centroid).ravel()  # shape: (n_sentences,)

    # 取相似度最高的 max_sentences 个句子下标
    ranked_indices = sims.argsort()[::-1][:max_sentences]
    ranked_indices = sorted(ranked_indices)  # 按原始顺序返回

    return [cleaned[i] for i in ranked_indices]


if __name__ == "__main__":
    sample_sentences = [
    "最近股市波动很大，很多人都在讨论是不是该减仓避险。",
    "我觉得英伟达的估值确实有点高，但短期内还不一定会崩盘。",
    "人工智能相关概念被炒得太热了，普通投资者很难分辨哪些公司是真的有技术。",
    "从长期来看，半导体行业还是有很强的增长潜力的。",
    "A股市场散户占比太高，情绪化交易非常严重。",
    "今年的消费恢复不如预期，很多人都在缩减开支。",
    "我身边的朋友都说不敢随便跳槽了，觉得经济环境不稳定。",
    "互联网大厂的校招名额在缩减，竞争比以前更加激烈。",
    "有些公司大规模裁员，却还在对外宣称业务高速发展。",
    "短视频平台上的理财博主很多，但真正懂金融的人其实不多。",
    "大家都在谈论副业，但现实中能稳定赚钱的副业并不多。",
    "年轻人更愿意把钱花在体验和兴趣上，而不是传统意义上的大件消费。",
    "不少人开始重新关注存款利率和货币基金的收益。",
    "过去几年跑去炒币的人，现在很多都不怎么发声了。",
    "新能源车品牌之间的价格战已经影响到传统车企的利润空间。",
    "电动车的充电基础设施在一线城市还算方便，小城市就比较麻烦。",
    "很多老一辈还是更信任燃油车，觉得更稳定更可靠。",
    "手机更新换代的速度在放缓，大家不再每年都换新机。",
    "有的品牌通过软件更新故意拖慢老手机的速度，被用户疯狂吐槽。",
    "现在的年轻人越来越重视隐私问题，对应用权限更加敏感。",
    "很多 App 要求不必要的权限，让人感觉很不安全。",
    "在线办公工具的普及，让远程工作变得更加可行。",
    "但长时间远程办公也让一些人感觉边界感变弱，很疲惫。",
    "有的公司表面上支持弹性工作制，实际上还是用考勤来衡量员工。",
    "不少人反映加班文化依然严重，只是换了一种说法。",
    "在社交媒体上，大家对于“躺平”和“摆烂”的讨论依然很多。",
    "也有年轻人强调要保持一定的上进心，只是不盲目内卷。",
    "房价问题依旧是大家最关心的话题之一。",
    "一些城市的新盘打折促销，说明市场确实在降温。",
    "租房市场的压力也不小，优质房源价格依然不低。",
    "不少毕业生选择合租，把生活成本压到最低。",
    "疫情之后，大家对健康和保险的关注度明显提高了。",
    "越来越多人开始主动学习理财知识，希望实现财务自由。",
    "但真正做到理性投资的，其实只是少数人。",
    "有些人仍然抱有“一夜暴富”的幻想，喜欢追逐热点。",
    "社交平台上的情绪容易被放大，导致信息环境很嘈杂。",
    "很多人开始刻意减少信息输入，避免被负面新闻影响心情。",
    "对于人工智能替代工作的担忧，也在不断上升。",
    "有的岗位确实在被自动化取代，但也会出现新的岗位需求。",
    "终身学习的观念被越来越多人接受，但真正行动起来不容易。",
    "不少人报了很多网课，却很难坚持学完。",
    "有些平台的课程质量参差不齐，用户体验并不好。",
    "知识付费的热度有所下降，大家变得更加理性。",
    "短视频内容越来越碎片化，导致注意力更容易分散。",
    "有的用户开始尝试“数字断舍离”，刻意减少使用手机的时间。",
    "关于环境保护和可持续发展的讨论在年轻人中越来越多。",
    "虽然大家都说要低碳生活，但真正改变消费习惯的并不多。",
    "有些品牌借环保之名做营销，被认为是“漂绿”行为。",
    "总体来看，社会情绪比较复杂，既有焦虑也有谨慎的乐观。",
    "很多人一边吐槽现实，一边还是努力在自己的领域找到机会。",
]
    summary = summarize_sentences(sample_sentences, max_sentences=10)
    for i, s in enumerate(summary, 1):
        print(f"{i}. {s}")


