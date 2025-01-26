# 使用libcst库进行更深入的代码结构分析

import libcst as cst
import os

class CodeAnalyzer(cst.CSTVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.functions.append(node.name.value)

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        self.classes.append(node.name.value)

def analyze_code_structure_libcst(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        tree = cst.parse_module(f.read())
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")
                        continue

                    analyzer = CodeAnalyzer()
                    tree.visit(analyzer)

                    for func in analyzer.functions:
                        print(f"Function: {func} in {file_path}")
                    for cls in analyzer.classes:
                        print(f"Class: {cls} in {file_path}")

# 调用函数，分析superset目录下的代码结构
analyze_code_structure_libcst('superset')