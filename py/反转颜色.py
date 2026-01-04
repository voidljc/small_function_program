from PIL import Image, ImageOps

# 输入与输出路径
input_path = "D:\小功能程序\py\屏幕截图 2025-12-17 202021.png"
output_path = "D:\小功能程序\py\屏幕截图 2025-12-17 202021.png"

# 打开图片
image = Image.open(input_path)

# 反转颜色
inverted_image = ImageOps.invert(image.convert("RGB"))

# 保存反转后的图片
inverted_image.save(output_path)

print(f"已生成反转图像：{output_path}")
