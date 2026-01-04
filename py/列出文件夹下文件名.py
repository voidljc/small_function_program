import os

# 获取当前目录下的所有文件和文件夹名
entries = os.listdir('D:\l4d2_MODpack\weaponmdf_0\scripts')

# 遍历列表并逐行打印
for entry in entries:
    print(entry)