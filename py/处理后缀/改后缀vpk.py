import os
import argparse
from pathlib import Path

"""
禁用模组
python  "D:\小功能程序\py\处理后缀\改后缀vpk.py" "D:/steam/steamapps/common/Left 4 Dead 2/left4dead2/addons" disable

恢复
python  "D:\小功能程序\py\处理后缀\改后缀vpk.py" "D:/steam/steamapps/common/Left 4 Dead 2/left4dead2/addons" enable

只改后缀（不动文件夹）	--only-files
只改文件夹（不动后缀）	--only-folders
启用白名单功能 --strict 
"""

TARGET_NAMES = {
    "1971235345_smoker",
    "3106824828_charger",
    "3252023518_hunter",
    "3334801928_charger_voice",
    "3337137543_hunter_voice",
    "3343311779_charger",
    "3345795744_witch",
    "3346058229_witch_voice",
    "3348394498_tank_voice",
    "3350745519_tankrock",
    "3352525304_tank",
    "3353002262_jockey",
    "3358730605_jockey_voice",
    "3486705129_spitter",
}

def change_extension(folder_path, from_ext, to_ext, strict=True):
    """仅在指定文件夹内修改文件后缀（不递归子文件夹）"""
    folder = Path(folder_path)
    if not folder.exists():
        print(f"错误：文件夹 '{folder_path}' 不存在")
        return

    # ====== 过滤逻辑就在这里 ======
    files = [f for f in folder.glob(f"*{from_ext}") if f.is_file()]
    if strict:                       # 加了 --strict 才启用白名单
        files = [f for f in files if f.stem in TARGET_NAMES]
    # ==============================

    if not files:
        print("在当前目录中没有找到需要重名的文件")
        return

    print(f"找到 {len(files)} 个文件需要重命名...")
    renamed = 0
    for f in files:
        new = f.with_suffix(to_ext)
        if new.exists():
            print(f"警告：跳过 '{f.name}'，因为 '{new.name}' 已存在")
            continue
        try:
            f.rename(new)
            print(f"✓ {f.name} -> {new.name}")
            renamed += 1
        except Exception as e:
            print(f"✗ 重命名 '{f.name}' 失败：{e}")
    print(f"完成！成功重命名 {renamed}/{len(files)} 个文件")

def rename_addon_folders(base_path, action):
    """重命名sourcemod和metamod文件夹"""
    base_path = Path(base_path)
    
    if action == 'disable':
        for folder_name in ['sourcemod', 'metamod']:
            folder_path = base_path / folder_name
            if folder_path.exists() and folder_path.is_dir():
                new_path = base_path / f"{folder_name}_"
                try:
                    if not new_path.exists():
                        folder_path.rename(new_path)
                        print(f"✓ 重命名文件夹: {folder_name} -> {folder_name}_")
                    else:
                        print(f"警告：文件夹 '{folder_name}_' 已存在，跳过")
                except Exception as e:
                    print(f"✗ 重命名文件夹 '{folder_name}' 失败: {str(e)}")
    
    else:  # enable
        for folder_name in ['sourcemod_', 'metamod_']:
            folder_path = base_path / folder_name
            if folder_path.exists() and folder_path.is_dir():
                original_name = folder_name.rstrip('_')
                original_path = base_path / original_name
                try:
                    if not original_path.exists():
                        folder_path.rename(original_path)
                        print(f"✓ 恢复文件夹: {folder_name} -> {original_name}")
                    else:
                        print(f"警告：文件夹 '{original_name}' 已存在，跳过")
                except Exception as e:
                    print(f"✗ 恢复文件夹 '{folder_name}' 失败: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="游戏插件禁用/启用工具")
    group = parser.add_mutually_exclusive_group()   # 互斥
    group.add_argument("--only-files",   action="store_true", help="只改后缀，不动文件夹")
    group.add_argument("--only-folders", action="store_true", help="只改文件夹，不动后缀")
    parser.add_argument("folder", help="目标文件夹路径")
    parser.add_argument("action", choices=["disable", "enable"], 
                       help="disable-禁用插件, enable-启用插件")
    parser.add_argument("--strict", action="store_true",
                   help="只处理白名单内的文件")
    args = parser.parse_args()
    
    do_files  = not args.only_folders   # 默认 True
    do_folders = not args.only_files    # 默认 True

    if args.action == "disable":
        print("正在禁用插件...")
        if do_files:
            change_extension(args.folder, ".vpk", ".vp", strict=args.strict)
        if do_folders:
            rename_addon_folders(args.folder, 'disable')
        print("✅ 禁用完成！")

    else:  # enable
        print("正在启用插件...")
        if do_files:
            change_extension(args.folder, ".vp", ".vpk", strict=args.strict)
        if do_folders:
            rename_addon_folders(args.folder, 'enable')
        print("✅ 启用完成！")

if __name__ == "__main__":
    main()