import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
import math

# 定义函数生成分段的数组
def generate_intervals(min_value, max_value, interval):
    num_intervals = int((max_value - min_value) / interval) + 1
    intervals = np.linspace(min_value + interval/2, max_value - interval/2, num_intervals)
    return intervals

root = tk.Tk()
root.withdraw()

# 设置初始目录
initial_dir = '/Users/jay/Desktop'
# 打开文件对话框，选择CSV文件
file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
# 更新资源管理器窗口
root.update()
# 关闭资源管理器窗口
root.destroy()

# 读取CSV文件
df = pd.read_csv(file_path)



# 提取第4列的数据
column_data = df.iloc[:, 3]

# 计算最小值和最大值
min_value = column_data.min()
max_value = column_data.max()
# 设置间隔和区间数量
interval = 1
num_intervals = int((max_value - min_value) / interval)

# num_intervals = 50
# interval = math.ceil(int((max_value - min_value) / num_intervals))

#生成分段的数组
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

# 计算每个元素占所有元素总和的比例
total_sum = np.sum(count_array)
ratio_array = [count / total_sum for count in count_array]

# 计算ratio_array和intervals数组的乘积
product = np.dot(ratio_array, intervals[:-1])

print(count_array)
print("每个元素占所有元素总和的比例:", ratio_array)
print("加权和为:", product)

# 绘制直方图
plt.hist(column_data, bins=num_intervals, range=(min_value, max_value), density=True)
plt.xlabel('Value')
plt.ylabel('Probability')
plt.title('Histogram of Data')
# 在图上画一条平行于x轴的红色线条，表示加权后的均值
plt.axhline(product, color='r')
plt.show()

# 将横纵坐标数据输出到Excel
output_data = {'Interval': intervals[:-1], 'Count': count_array}
output_df = pd.DataFrame(output_data)
output_file_path = 'histogram_data.xlsx'  # 输出文件路径
output_df.to_excel(output_file_path, index=False)
print("横纵坐标数据已输出到:", output_file_path)

