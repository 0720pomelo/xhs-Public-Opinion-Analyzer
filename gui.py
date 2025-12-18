import tkinter as tk
from tkinter import ttk, messagebox
import time
import os

from xhs_crawler import crawl_xhs
from ollama_analyzer import ollama_analyzer
from illuminator import key_sentence_extraction
from wordcloudgenerator import generate_wordcloud


def start_analysis():
    """开始按钮回调：根据输入话题爬取小红书数据。"""
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showwarning("提示", "请输入你想研究的话题。")
        return

    # 生成一个简单且基本唯一的文件名，例如：note_时间戳
    filename = f"note_{int(time.time())}"

    saved_name = f"{filename}.jsonl"

    # 调用爬虫，固定抓取 100 条
    try:
        crawl_xhs(keyword=topic, num=100, filename=filename)
    except Exception as e:
        # 爬取失败时，也把已经保存的（部分）数据文件路径告诉用户，方便后续分析
        messagebox.showerror(
            "爬取失败",
            f"爬取过程中出现异常：\n{e}\n\n"
            f"已保存的数据（可能是不完整的）文件路径为：\n"
            f"data/{saved_name}\n\n"
            f"你仍然可以使用该文件继续后续解析和分析。"
        )
        return

    # 爬取完成后给出提示，并告知保存的文件名
    messagebox.showinfo(
        "爬取完成",
        f"已完成对话题「{topic}」的爬取，可以开始后续分析。\n\n"
        f"数据文件保存在 data 目录下，文件名为：\n{saved_name}\n\n"
        f"请将上面的文件名复制到下方的“解析目标文件”文本框中。"
    )


def start_parsing():
    """解析按钮回调：调用 ollama 分析器对指定文件进行解析。"""
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showwarning("提示", "请输入你想研究的话题。")
        return

    target_name = target_entry.get().strip()
    if not target_name:
        messagebox.showwarning("提示", "请输入要解析的数据文件名（例如 note_xxx.jsonl）。")
        return

    # 用户可能会直接粘贴带后缀的文件名，这里自动去掉 .jsonl
    if target_name.endswith(".jsonl"):
        pos = target_name[:-6]
    else:
        pos = target_name

    result_path = os.path.join("result", f"{pos}.json")

    # 如果已经有同名结果文件，则提示用户可以直接开始分析
    if os.path.exists(result_path):
        messagebox.showinfo(
            "提示",
            f"检测到结果文件已存在：\n{result_path}\n\n"
            "该文件已经解析完成，请直接开始分析（例如点击“关键句提取”等功能按钮）。"
        )
        return

    try:
        ollama_analyzer(topic, pos)
    except Exception as e:
        messagebox.showerror("错误", f"解析过程中出现异常：\n{e}")
        return

    messagebox.showinfo("解析完成", "解析完成，现在可以点击功能按钮了。")


def start_key_sentence_extraction():
    """功能一：关键句提取。"""
    target_name = target_entry.get().strip()
    if not target_name:
        messagebox.showwarning("提示", "请输入要解析的数据文件名（例如 note_xxx.json 或 note_xxx）。")
        return

    # 支持用户输入 note_xxx 或 note_xxx.json，两种情况都转成 ./result/note_xxx.json
    if target_name.endswith(".json"):
        base_name = target_name[:-5]
    else:
        base_name = target_name

    path = f"./result/{base_name}.json"

    try:
        sentences = key_sentence_extraction(path)
    except FileNotFoundError:
        messagebox.showerror("错误", f"找不到结果文件：\n{path}")
        return
    except Exception as e:
        messagebox.showerror("错误", f"关键句提取过程中出现异常：\n{e}")
        return

    if not sentences:
        messagebox.showinfo("关键句提取结果", "未能提取到关键句。")
        return

    result_text = "\n".join(f"{idx+1}. {s}" for idx, s in enumerate(sentences))
    messagebox.showinfo("关键句提取结果", result_text)


def start_wordcloud_generation():
    """功能二：词云生成。"""
    target_name = target_entry.get().strip()
    if not target_name:
        messagebox.showwarning("提示", "请输入要解析的数据文件名（例如 note_xxx 或 note_xxx.jsonl）。")
        return

    # 支持用户输入 note_xxx 或 note_xxx.jsonl，两种情况都转成 ./data/note_xxx.jsonl
    if target_name.endswith(".jsonl"):
        base_name = target_name[:-6]
    else:
        base_name = target_name

    path = f"./data/{base_name}.jsonl"

    try:
        generate_wordcloud(path)
    except FileNotFoundError:
        messagebox.showerror("错误", f"找不到数据文件：\n{path}")
        return
    except Exception as e:
        messagebox.showerror("错误", f"生成词云过程中出现异常：\n{e}")
        return

    messagebox.showinfo("词云生成", f"已根据数据文件生成词云及相关可视化：\n{path}")


def create_main_window():
    window = tk.Tk()
    window.title("小红书舆情综合分析系统")
    window.geometry("800x600")

    # 使用 ttk 主题，让界面更美观（“面子工程”）
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        # 如果系统没有该主题，就忽略
        pass

    # 顶部说明文字
    title_label = ttk.Label(
        window,
        text="请输入你想研究的话题",
        font=("Arial", 18)
    )
    title_label.pack(pady=20)

    # 话题输入框 + “开始分析（爬取）”按钮
    entry_frame = ttk.Frame(window)
    entry_frame.pack(pady=10, fill="x", padx=40)

    global topic_entry
    topic_entry = ttk.Entry(entry_frame, font=("Arial", 14))
    topic_entry.pack(side="left", fill="x", expand=True)

    start_button = ttk.Button(
        entry_frame,
        text="开始分析（爬取）",
        command=start_analysis
    )
    start_button.pack(side="left", padx=(10, 0))

    # 解析目标文件输入框标签
    target_label = ttk.Label(
        window,
        text="解析目标文件（例如：note_xxx.jsonl）：",
        font=("Arial", 12)
    )
    target_label.pack(pady=(20, 5))

    # 解析目标文件输入框 + “开始解析”按钮
    parse_frame = ttk.Frame(window)
    parse_frame.pack(pady=5, fill="x", padx=40)

    global target_entry
    target_entry = ttk.Entry(parse_frame, font=("Arial", 12))
    target_entry.pack(side="left", fill="x", expand=True)

    parse_button = ttk.Button(
        parse_frame,
        text="开始解析",
        command=start_parsing
    )
    parse_button.pack(side="left", padx=(10, 0))

    # 功能按钮区域
    buttons_frame = ttk.LabelFrame(window, text="功能面板")
    buttons_frame.pack(pady=40, padx=40, fill="both", expand=False)

    btn1 = ttk.Button(buttons_frame, text="关键句提取", command=start_key_sentence_extraction)
    btn2 = ttk.Button(buttons_frame, text="词云生成", command=start_wordcloud_generation)
    btn3 = ttk.Button(buttons_frame, text="功能三")
    btn4 = ttk.Button(buttons_frame, text="功能四")

    # 使用 grid 让四个按钮排成 2x2 的简单布局
    btn1.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
    btn2.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
    btn3.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
    btn4.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

    # 让每列同比例扩展
    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)

    return window


if __name__ == "__main__":
    main_window = create_main_window()
    main_window.mainloop()


