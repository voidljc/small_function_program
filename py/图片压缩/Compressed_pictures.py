from PIL import Image

def compress_jpg(input_path, output_path, quality=80):
    """
    压缩 JPG 图片
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    :param quality: 压缩质量 (1-95)，数字越小文件越小，画质越差
    """
    img = Image.open(input_path)
    # 转成 RGB 避免有些 JPG 带 alpha 通道报错
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(output_path, "JPEG", quality=quality, optimize=True)

# 示例用法：
compress_jpg("D:\小功能程序\py\图片压缩\Gemini_Generated_Image_7ov81e7ov81e7ov8.png", "D:\小功能程序\py\图片压缩\Gemini_Generated_Image_7ov81e7ov81e7ov8.png", quality=70)
