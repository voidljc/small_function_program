#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
一个用于循环计算 F1-Score 的 Python 脚本。
会持续提示用户输入精确率 (precision) 和召回率 (recall)，
直到用户输入 'exit' 退出。
"""

import sys

def calculate_f1(precision: float, recall: float) -> float:
    """
    根据精确率和召回率计算 F1-Score。

    F1-Score 的计算公式为:
    F1 = 2 * (precision * recall) / (precision + recall)

    Args:
        precision (float): 精确率 (0.0 到 1.0 之间)。
        recall (float): 召回率 (0.0 到 1.0 之间)。

    Returns:
        float: 计算得到的 F1-Score。
               如果输入无效 (不在 0-1 范围)，返回 -1.0。
    """
    # 检查输入的有效性
    if not (0.0 <= precision <= 1.0):
        print(f"  [错误]: 精确率 (precision) 必须在 0.0 和 1.0 之间。输入值: {precision}")
        return -1.0
    if not (0.0 <= recall <= 1.0):
        print(f"  [错误]: 召回率 (recall) 必须在 0.0 和 1.0 之间。输入值: {recall}")
        return -1.0

    # 处理分母为零的边缘情况
    # 如果 precision 和 recall 均为 0，则 F1-Score 定义为 0
    if precision + recall == 0.0:
        return 0.0

    # 计算 F1-Score
    f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score

def main_loop():
    """
    主循环函数，用于持续接收用户输入并计算。
    """
    print("=== F1-Score 循环计算器 ===")
    print("使用方法:")
    print("  1. 输入 精确率 和 召回率 (用空格隔开), 例如: 0.8 0.9")
    print("  2. 输入 'exit' (或 'q') 退出程序。")
    print("-" * 35)

    while True:
        # 获取用户输入
        try:
            user_input = input("请输入 (precision recall) 或 'exit': ").strip().lower()
        except EOFError:
            # 处理 Ctrl+D (EOF) 退出
            print("\n正在退出程序...")
            break

        # 检查退出条件
        if user_input == 'exit' or user_input == 'q':
            print("正在退出程序...")
            break

        # 解析输入
        parts = user_input.split()

        # 验证输入格式
        if len(parts) != 2:
            print(f"  [错误]: 输入格式不正确。请输入两个数字 (例如: 0.8 0.9)")
            print("-" * 35)
            continue

        # 尝试转换
        try:
            precision = float(parts[0])
            recall = float(parts[1])
        except ValueError:
            print(f"  [错误]: 输入无效 '{parts[0]}', '{parts[1]}'。请输入数字。")
            print("-" * 35)
            continue

        # 执行计算
        f1 = calculate_f1(precision, recall)

        # 打印结果 (calculate_f1 内部已处理了 <0 的错误打印)
        if f1 >= 0.0:
            print(f"  > 精确率: {precision:.4f}, 召回率: {recall:.4f}")
            print(f"  > 计算结果 F1-Score: {f1:.6f}")
        
        print("-" * 35)

if __name__ == "__main__":
    main_loop()