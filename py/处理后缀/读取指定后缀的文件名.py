# =======================
# 参数区
# =======================
TARGET_DIR = r"D:/steam/steamapps/common/Left 4 Dead 2/left4dead2/addons/"   # 指定要扫描的文件夹路径
EXTENSION = ".vp"                      # 指定文件扩展名（区分大小写）
# =======================


import os

def list_vp_filenames(directory: str, ext: str):
    """
    在给定目录下查找指定扩展名文件并返回文件名（不含后缀）。
    """
    result = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path) and entry.endswith(ext):
            name_without_ext = os.path.splitext(entry)[0]
            result.append(name_without_ext)
    return result


if __name__ == "__main__":
    filenames = list_vp_filenames(TARGET_DIR, EXTENSION)
    for name in filenames:
        print(name+",")
