# 统计每月或每年的提交次数并绘制时间序列图
import matplotlib.pyplot as plt
import pandas as pd

# 设置 Matplotlib 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 加载数据
df = pd.read_csv('commits.csv', low_memory=False)

# 转换日期列
df['commit.author.date'] = pd.to_datetime(df['commit.author.date'], errors='coerce')

# 按年份和月份分组统计提交次数
df['year'] = df['commit.author.date'].dt.year
df['month'] = df['commit.author.date'].dt.month
monthly_commits = df.groupby(['year', 'month']).size().reset_index(name='count')

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(monthly_commits['year'].astype(str) + '-' + monthly_commits['month'].astype(str), monthly_commits['count'], marker='o')
plt.title('每月提交次数')
plt.xlabel('年份-月份')
plt.ylabel('提交次数')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 统计每个作者的提交次数
author_commits = df['commit.author.name'].value_counts().reset_index()
author_commits.columns = ['作者', '提交次数']

# 绘制柱状图
plt.figure(figsize=(12, 6))
plt.bar(author_commits['作者'], author_commits['提交次数'], color='skyblue')
plt.title('作者提交次数')
plt.xlabel('作者')
plt.ylabel('提交次数')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()