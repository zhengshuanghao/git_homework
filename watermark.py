import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import piexif

def get_exif_date(img_path):
    try:
        exif_dict = piexif.load(img_path)
        date_str = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()
        date = date_str.split(' ')[0].replace(':', '-')
        return date
    except Exception:
        return None

def get_watermark_position(img_size, text_size, position):
    w, h = img_size
    tw, th = text_size
    if position == 'left_top':
        return (10, 10)
    elif position == 'center':
        return ((w-tw)//2, (h-th)//2)
    elif position == 'right_bottom':
        return (w-tw-10, h-th-10)
    else:
        return (10, 10)

def add_watermark(img_path, out_path, text, font_size, color, position):
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    text_size = draw.textsize(text, font=font)
    pos = get_watermark_position(img.size, text_size, position)
    draw.text(pos, text, font=font, fill=color)
    img.save(out_path)

def main():
    print("欢迎使用图片批量水印工具！")
    src_dir = input("请输入图片文件夹路径: ").strip()
    font_size = input("请输入字体大小（默认32）: ").strip()
    font_size = int(font_size) if font_size else 32
    color = input("请输入字体颜色（如 white、yellow，默认white）: ").strip()
    color = color if color else "white"
    position = input("请输入水印位置（left_top, center, right_bottom，默认right_bottom）: ").strip()
    position = position if position in ["left_top", "center", "right_bottom"] else "right_bottom"

    out_dir = os.path.join(src_dir, os.path.basename(src_dir) + "_watermark")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for fname in os.listdir(src_dir):
        fpath = os.path.join(src_dir, fname)
        if os.path.isfile(fpath) and fname.lower().endswith((".jpg", ".jpeg", ".png")):
            date = get_exif_date(fpath)
            if date:
                out_path = os.path.join(out_dir, fname)
                add_watermark(fpath, out_path, date, font_size, color, position)
                print(f"已处理: {fname} -> {out_path}")
    print(f"所有图片已处理完毕，水印图片保存在: {out_dir}")

if __name__ == "__main__":
    main()
