import re

# ================= 配置区域 =================
old_txt_path = "D:\泉\现在引用.txt"        # 旧 txt 文件路径
new_txt_path = "D:\泉\引用论文分类还需编号.txt"   # 输出的新 txt 文件路径

# 需要保留的编号
keep_ids = {
    4,5,6,7,8,9,10,11,21,22,23,34,42,44,46,49,51,52,53,54,57,60,61,63,
    76,77,78,80,88,90,96,97,99,101,102,103,104,105,106,107,109,110,111,112
}
# ==========================================


def parse_ref_line(line):
    """
    从一行中提取编号和正文，例如：
    '4.  Hashimoto ...' → (4, 'Hashimoto ...')
    """
    m = re.match(r"^\s*(\d+)\.\s*(.+)$", line.strip())
    if not m:
        return None, None
    return int(m.group(1)), m.group(2)


def main():
    results = []

    # 读取旧 txt
    with open(old_txt_path, "r", encoding="utf-8") as f:
        for line in f:
            ref_id, content = parse_ref_line(line)
            if ref_id is None:
                continue

            if ref_id in keep_ids:
                # 保留整个原始行（不修改格式）
                results.append(line.rstrip("\n"))

    # 按编号排序（保证输出顺序一致）
    def extract_id(s):
        m = re.match(r"^\s*(\d+)\.", s)
        return int(m.group(1)) if m else 999999

    results.sort(key=extract_id)

    # 写入新 txt
    with open(new_txt_path, "w", encoding="utf-8") as f_out:
        for line in results:
            f_out.write(line + "\n")

    print(f"完成！共写入 {len(results)} 条文献到 {new_txt_path}")


if __name__ == "__main__":
    main()
