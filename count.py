import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# 创建GUI窗口
window = tk.Tk()
window.title("分段数组生成器")
window.geometry("400x350")

# 选择CSV文件
def choose_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    csv_entry.delete(0, tk.END)
    csv_entry.insert(tk.END, file_path)

# 生成分段数组
def generate_intervals():
    # 读取CSV文件
    file_path = csv_entry.get()
    df = pd.read_csv(file_path)

    # 提取指定列的数据
    column_index = int(column_entry.get())
    column_data = df.iloc[:, column_index]

    # 计算最小值和最大值
    min_value = column_data.min()
    max_value = column_data.max()

    # 获取输入的间隔
    interval = float(interval_entry.get())

    # 设置区间数量
    num_intervals = int((max_value - min_value) / interval)

    # 生成分段的数组
    intervals = generate_intervals(min_value, max_value, interval)

    # 统计每个间隔中数据的个数并生成一个数组
    count_array = []
    for i in range(num_intervals):
        lower_bound = min_value + i * interval
        upper_bound = min_value + (i + 1) * interval
        count = ((column_data >= lower_bound) & (column_data < upper_bound)).sum()
        count_array.append(count)

    # 统计数据分布
    hist, bin_edges = np.histogram(column_data, bins=num_intervals, range=(min_value, max_value), density=True)

    # 绘制直方图
    plt.hist(column_data, bins=num_intervals, range=(min_value, max_value), density=True)
    plt.xlabel('Value')
    plt.ylabel('Probability')
    plt.title('Histogram of Data')
    plt.show()

    # 计算每个元素占所有元素总和的比例
    total_sum = np.sum(count_array)
    ratio_array = [count / total_sum for count in count_array]

    # 计算ratio_array和intervals数组的乘积
    product = np.dot(ratio_array, intervals[:-1])

    # 输出结果
    result_text.insert(tk.END, "各区间数据个数: {}\n".format(count_array))
    result_text.insert(tk.END, "每个元素占所有元素总和的比例: {}\n".format(ratio_array))
    result_text.insert(tk.END, "加权和为: {}\n".format(product))

# 标签和输入框
csv_label = tk.Label(window, text="选择CSV文件:")
csv_label.pack()
csv_entry = tk.Entry(window, width=40)
csv_entry.pack()
choose_button = tk.Button(window, text="选择", command=choose_csv_file)
choose_button.pack()

column_label = tk.Label(window, text="输入要提取的列索引:")
column_label.pack()
column_entry = tk.Entry(window, width=10)
column_entry.pack()

interval_label = tk.Label(window, text="设置间隔:")
interval_label.pack()
interval_entry = tk.Entry(window, width=10)
interval_entry.pack()

generate_button = tk.Button(window, text="生成分段数组", command=generate_intervals)
generate_button.pack()

result_text = tk.Text(window, height=10, width=40)
result_text.pack()

window.mainloop()
