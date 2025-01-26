# 使用ast库解析代码结构，提取类和函数的定义

import ast
import os

def analyze_code_structure(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read())
                    except SyntaxError as e:
                        print(f"Syntax error in {file_path}: {e}")
                        continue

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            print(f"Function: {node.name} in {file_path}")
                        elif isinstance(node, ast.ClassDef):
                            print(f"Class: {node.name} in {file_path}")

# 调用函数，分析superset目录下的代码结构
analyze_code_structure('superset')