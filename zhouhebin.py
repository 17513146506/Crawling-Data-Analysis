
#作者：周何彬  2023.0520
import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
# 定义爬取函数

def crawl_data():
    url = 'https://www.maigoo.com/news/662215.html'
    headers = {
        'User-Agent': 'Mozi  lla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.find('table', class_='table1')
    rows = table.findAll('tr')

    # 新建csv文件并写入表头
    with open('high_school_ranking.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['排名', '学校名称', '省份', '类型', '得分'])

    # 逐行解析数据并写入csv文件
    with open('high_school_ranking.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        for row in rows[1:]:  #第一行是表头，不需要处理
            tds = row.find_all('td')
            rank = tds[0].text.strip()
            school_name = tds[1].text.strip()
            province = tds[2].text.strip()
            school_type = tds[3].text.strip()
            score = tds[4].text.strip()
            writer.writerow([rank, school_name, province, school_type, score])
            print(rank, school_name, province, school_type, score)
    import tkinter as tk
    import pandas as pd
    # 读取CSV文件
    df = pd.read_csv('high_school_ranking.csv')
    # 创建TK对象
    root = tk.Tk()
    root.title('CSV数据展示')
    # 创建表格控件
    table = tk.Text(root, height=20, font=('Courier', 20))
    # 显示表头
    header = ' , '.join(df.columns.values) + '\n'
    table.insert('end', header)
    # 显示数据
    for i, row in df.iterrows():
        row = ' , '.join([str(val) for val in row.values]) + '\n'
        table.insert('end', row)
    # 将表格控件添加到窗口
    table.pack()
    # 启动窗口消息循环
    root.mainloop()
# 对爬取的数据进行处理：清洗和补全
def process_data():
    import pandas as pd
    # df = pd.read_csv('high_school_ranking.csv')
    df=pd.read_csv('high_school_ranking.csv', na_values=['/', 'NA', 'NaN', 'NULL'])
    # 清洗省份和类型字段
    df['省份'] = df['省份'].str.replace('省|市|自治区|回族|壮族|维吾尔|特别行政区', '', regex=True)
    df['类型'] = df['类型'].str.replace('非独立学院', '民办本专科', regex=True)
    df['类型'] = df['类型'].str.replace('本科及以上', '民办本专科', regex=True)
    df['类型'] = df['类型'].str.replace('专科（高职）', '民办本专科', regex=True)
    df['类型'] = df['类型'].str.replace('专科（高职）', '民办本专科', regex=True)
    df['类型'] = df['类型'].str.replace('专科及以上', '民办本专科', regex=True)
    # 补全缺失值
    df['得分'].fillna(df['得分'].median(), inplace=True)
    df.to_csv('processed_data.csv', index=False)
# 对前100名高校的数据进行统计和分析
def select_file():
    # 创建一个Tk对象
    root = tk.Tk()
    # 隐藏主窗口，否则会在任务栏中显示一个空窗口
    root.withdraw()
    # 选择文件
    file_path = filedialog.askopenfilename(title="选择文件", filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
    # 返回文件路径
    a=(str(file_path))
    return a
def analyze_data1():
    import pandas as pd
    # 解决matplotlib绘图中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['font.sans-serif'] = ['KaiTi']   # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    df = pd.read_csv('processed_data.csv')
    top100 = df[:100]
    # 统计每个省份的高校数量
    prov_counts = top100['省份'].value_counts()
    # 统计各个类型的高校数量
    type_counts = top100['类型'].value_counts()
    # 创建一个2行1列的图布，大小为12x12英寸
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    # 绘制柱状图1：各省高校数量
    axes[0].bar(x=prov_counts.index, height=prov_counts.values, width=0.6)
    axes[0].set_xticklabels(labels=prov_counts.index, rotation=90)
    axes[0].set_title('各省高校数量')
    # 绘制柱状图2：各类型高校数量
    axes[1].bar(x=type_counts.index, height=type_counts.values, width=0.6)
    axes[1].set_xticklabels(labels=type_counts.index, rotation=90)
    axes[1].set_title('各类型高校数量')
    # 调整图表之间的距离
    plt.subplots_adjust(wspace=0.3, hspace=0.6)
    # 展示图表
    plt.show()
def analyze_data2():
    import pandas as pd
    # 解决matplotlib绘图中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['font.sans-serif'] = ['KaiTi']   # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    df = pd.read_csv('processed_data.csv')
    top100 = df[:100]
    # 各类型数量的比例
    type_counts = top100['类型'].value_counts().to_dict()
    # 各省数量的比例
    prov_counts = top100['省份'].value_counts().to_dict()
    # 创建一个1行2列的图布，大小为12x6英寸
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    # 绘制饼状图1：各类型数量的比例
    axes[0].pie(x=list(type_counts.values()), labels=list(type_counts.keys()), autopct='%1.1f%%')
    axes[0].set_title('各类型数量的比例')
    # 绘制饼状图2：各省数量的比例
    axes[1].pie(x=list(prov_counts.values()), labels=list(prov_counts.keys()), autopct='%1.1f%%')
    axes[1].set_title('各省数量的比例')
    # 展示图表
    plt.show()
# 可视化界面
root = tk.Tk()
root.title("民办高校排名分析系统")
root.geometry("600x600")
root.resizable(width=False, height=False)
# 定义功能函数
def crawl():
    crawl_data()
def process_file():
    process_data()
    tk.messagebox.showinfo(title='消息', message ='数据处理完成')
def exit_file():
    exit(0)
def view_file():
    import tkinter as tk
    import pandas as pd
    # 读取CSV文件
    df = pd.read_csv('processed_data.csv')
    # 创建TK对象
    root = tk.Tk()
    root.title('CSV数据展示')
    # 创建表格控件
    table = tk.Text(root, height=20, font=('Courier', 20))
    # 显示表头
    header = ' , '.join(df.columns.values) + '\n'
    table.insert('end', header)
    # 显示数据
    for i, row in df.iterrows():
        row = ' , '.join([str(val) for val in row.values]) + '\n'
        table.insert('end', row)
    # 将表格控件添加到窗口
    table.pack()
    # 启动窗口消息循环
    root.mainloop()
crawl_button=tk.Button(root, text='爬取数据', command=crawl, width=15, height=3)
process_button = tk.Button(root, text='数据处理', command=process_file, width=15, height=3)
view_button = tk.Button(root, text='数据显示', command=view_file, width=15, height=3)
analyze1_button = tk.Button(root, text='数据分析-柱状图', command=analyze_data1, width=15, height=3)
analyze2_button = tk.Button(root, text='数据分析-饼状图', command=analyze_data2, width=15, height=3)
exit_button= tk.Button(root, text='退出系统', command=exit_file, width=15, height=3)
crawl_button.pack(pady=15)
process_button.pack(pady=15)
view_button.pack(pady=15)
analyze1_button.pack(pady=15)
analyze2_button.pack(pady=15)
exit_button.pack(pady=15)
root.mainloop()
