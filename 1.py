# 利用GitHub API获取Apache Superset的提交历史数据
import requests
import json
import pandas as pd

url = "https://api.github.com/repos/apache/superset/commits"
headers = {
    "Authorization": "token Token"
}

all_commits = []
page = 1
per_page = 100  # 每页显示的记录数

while True:
    params = {
        "page": page,
        "per_page": per_page
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    commits = response.json()
    if not commits:
        break  # 如果没有更多数据，退出循环
    all_commits.extend(commits)
    page += 1

print(f"Total commits fetched: {len(all_commits)}")

# 保存为JSON文件
with open("commits.json", "w") as f:
    json.dump(all_commits, f, indent=4)

# 保存为CSV文件
df = pd.json_normalize(all_commits)
df.to_csv("commits.csv", index=False)