import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

GITHUB_TOKEN = "Token"

def get_bug_issues():
    url = "https://api.github.com/repos/apache/superset/issues"
    params = {'labels': 'bug', 'state': 'all', 'per_page': 100}
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    all_issues = []

    while True:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch data:", response.status_code)
            print("Response:", response.json())
            break
        issues = response.json()
        if not issues:
            print("No more issues to fetch.")
            break
        all_issues.extend(issues)
        if 'next' not in response.links:
            break
        url = response.links['next']['url']

    return all_issues

def save_data_to_file(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f)
    print(f"Data saved to {file_name}")

def load_data_from_file(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

def analyze_bug_data(bug_issues):
    if not bug_issues:
        print("No bug issues found.")
        return

    # 提取需要的字段
    extracted_data = []
    for issue in bug_issues:
        if 'created_at' in issue and 'closed_at' in issue:
            extracted_data.append({
                'created_at': issue['created_at'],
                'closed_at': issue['closed_at'],
                'labels': issue.get('labels', [])
            })

    if not extracted_data:
        print("No valid data for analysis.")
        return

    bug_df = pd.DataFrame(extracted_data)
    bug_df['created_at'] = pd.to_datetime(bug_df['created_at']).dt.to_period('M')
    bug_df['fix_time'] = (pd.to_datetime(bug_df['closed_at']) - pd.to_datetime(bug_df['created_at'])).dt.days
    bug_df = bug_df.dropna(subset=['fix_time'])  # 去掉没有修复时间的行

    # Bug 频率
    bug_counts = bug_df.groupby('created_at').size()
    bug_counts.plot(kind='line')
    plt.title('Monthly Bug Report Frequency')
    plt.xlabel('Date')
    plt.ylabel('Number of Bug Reports')
    plt.show()

    # Bug 修复时间分布
    bug_df['fix_time'].hist(bins=20)
    plt.title('Distribution of Bug Fix Times')
    plt.xlabel('Fix Time (days)')
    plt.ylabel('Number of Bugs')
    plt.show()

    # Bug 类型分布（如果有足够的标签信息）
    bug_df['bug_type'] = bug_df['labels'].apply(lambda x: [label['name'] for label in x if label['name'] != 'bug'])
    bug_type_counts = bug_df['bug_type'].explode().value_counts()
    bug_type_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Bug Type Distribution')
    plt.ylabel('')
    plt.show()

    # 计算平均修复时间
    avg_bug_fix_time = bug_df['fix_time'].mean()
    print(f"Average Bug Fix Time: {avg_bug_fix_time:.2f} days")

if __name__ == "__main__":
    # 获取数据并保存到文件
    bug_issues = get_bug_issues()
    save_data_to_file(bug_issues, 'bug_issues.json')

    # 从文件加载数据
    bug_issues = load_data_from_file('bug_issues.json')

    # 检查加载的数据
    print("Loaded bug issues:", bug_issues[:5])  # 打印前5条数据

    # 数据分析和结果展示
    analyze_bug_data(bug_issues)