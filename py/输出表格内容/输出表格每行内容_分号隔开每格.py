import pandas as pd
import os

def process_spreadsheet(file_path):
    """
    读取表格文件并按指定格式输出每一行内容。
    
    参数:
    file_path (str): 表格文件的路径 (支持 .xlsx, .xls, .csv)
    """
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在。")
        return

    try:
        # 根据文件扩展名选择读取方式
        # header=None: 不将第一行作为列名，而是作为第一行数据
        # dtype=str: 强制读取为字符串，避免数字精度问题
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, header=None, dtype=str)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path, header=None, dtype=str)
        else:
            print("不支持的文件格式。请使用 .csv 或 .xlsx/.xls 文件。")
            return

        # 将 NaN (空值) 替换为空字符串
        df = df.fillna('')

        # 遍历每一行进行输出
        for index, row in df.iterrows():
            # 将行内所有元素用分号连接
            # row.tolist() 将 pandas Series 转换为列表
            line_content = ';'.join(row.tolist())
            print(f"第{index + 1}行：{line_content}")

    except Exception as e:
        print(f"处理文件时发生错误: {e}")

if __name__ == "__main__":
    # 在此处修改为您实际的文件路径
    target_file = "D:/小功能程序/py/输出表格内容/检索记录.csv" 
    
    # 示例调用
    process_spreadsheet(target_file)