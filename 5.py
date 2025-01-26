# 分析GitHub上的Apache Superset社区数据来了解其活跃度，包括成员的参与度和贡献情况

import requests
import pandas as pd
import matplotlib.pyplot as plt

# 1. 获取GitHub数据
def get_github_data(endpoint, token, state="all"):
    url = f"https://api.github.com/repos/apache/superset/{endpoint}?state={state}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

GITHUB_TOKEN = ("Token")

# 获取已关闭的 Issues 和 Pull Requests
issues = get_github_data('issues', GITHUB_TOKEN, state="closed")
pull_requests = get_github_data('pulls', GITHUB_TOKEN, state="closed")

# 2. 数据处理
# 提取活跃用户
issue_authors = [issue['user']['login'] for issue in issues if 'user' in issue and issue['user'] is not None]
pr_authors = [pr['user']['login'] for pr in pull_requests if 'user' in pr and pr['user'] is not None]
all_authors = issue_authors + pr_authors
author_counts = pd.Series(all_authors).value_counts().head(10)

# 计算平均处理时间
def calculate_average_time(data):
    times = []
    for item in data:
        if 'created_at' in item and 'closed_at' in item and item['closed_at'] is not None:
            created_at = pd.to_datetime(item['created_at'])
            closed_at = pd.to_datetime(item['closed_at'])
            times.append((closed_at - created_at).days)
    if times:
        return sum(times) / len(times)
    else:
        return None

avg_issue_time = calculate_average_time(issues)
avg_pr_time = calculate_average_time(pull_requests)

# 3. 保存到CSV文件
# 保存活跃用户数据
author_counts.to_csv("active_users.csv", header=["Contributions"], index_label="User")

# 保存处理时间数据
data = {
    "Type": ["Issues", "Pull Requests"],
    "Average Handling Time (days)": [avg_issue_time, avg_pr_time]
}
pd.DataFrame(data).to_csv("handling_times.csv", index=False)

# 4. 绘制图表
# 绘制活跃用户分布图
plt.figure(figsize=(10, 6))
author_counts.plot(kind='bar')
plt.title('Top 10 Active Community Members')
plt.xlabel('User')
plt.ylabel('Number of Contributions')
plt.show()

# 绘制处理时间分布图
plt.figure(figsize=(10, 6))
issue_times = [pd.to_datetime(issue['closed_at']) - pd.to_datetime(issue['created_at']) for issue in issues if issue['closed_at'] is not None]
pr_times = [pd.to_datetime(pr['closed_at']) - pd.to_datetime(pr['created_at']) for pr in pull_requests if pr['closed_at'] is not None]

# 检查是否有数据可绘制
if issue_times:
    plt.hist([t.days for t in issue_times], bins=20, alpha=0.5, label='Issues')
if pr_times:
    plt.hist([t.days for t in pr_times], bins=20, alpha=0.5, label='Pull Requests')

# 检查是否有标签可用
handles, labels = plt.gca().get_legend_handles_labels()
if handles and labels:
    plt.legend()
else:
    print("No data to plot for handling times.")

plt.title('Distribution of Handling Times')
plt.xlabel('Days')
plt.ylabel('Frequency')
plt.show()

# 打印处理时间数据
print("Issue Times:", issue_times)
print("PR Times:", pr_times)