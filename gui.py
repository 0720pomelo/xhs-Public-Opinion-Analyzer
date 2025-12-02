import tkinter as tk
from tkinter import ttk, messagebox


def start_analysis():
    """Callback for the Start button – will later trigger search & analysis."""
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showwarning("提示", "请输入你想研究的话题。")
        return

    # TODO: 在这里调用你的舆情分析模块，例如：
    # from ollama_analyzer import analyze_topic
    # result = analyze_topic(topic)
    # 现在先用一个简单弹窗占位
    messagebox.showinfo(
        "分析开始",
        f"正在为话题「{topic}」抓取数据并进行分析...\n（此处为占位逻辑）"
    )


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

    # 输入框 + 开始按钮 区域
    entry_frame = ttk.Frame(window)
    entry_frame.pack(pady=10, fill="x", padx=40)

    global topic_entry
    topic_entry = ttk.Entry(entry_frame, font=("Arial", 14))
    topic_entry.pack(side="left", fill="x", expand=True)

    start_button = ttk.Button(
        entry_frame,
        text="开始分析",
        command=start_analysis
    )
    start_button.pack(side="left", padx=(10, 0))

    # 功能按钮区域（目前只是占位，无实际功能）
    buttons_frame = ttk.LabelFrame(window, text="功能面板（占位）")
    buttons_frame.pack(pady=40, padx=40, fill="both", expand=False)

    btn1 = ttk.Button(buttons_frame, text="功能一")
    btn2 = ttk.Button(buttons_frame, text="功能二")
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


