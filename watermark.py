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
    parser = argparse.ArgumentParser(description="图片批量水印工具")
    parser.add_argument("dir", help="图片文件夹路径")
    parser.add_argument("--font_size", type=int, default=32, help="字体大小")
    parser.add_argument("--color", type=str, default="white", help="字体颜色")
    parser.add_argument("--position", type=str, choices=["left_top", "center", "right_bottom"], default="right_bottom", help="水印位置")
    args = parser.parse_args()

    src_dir = args.dir
    out_dir = os.path.join(src_dir, os.path.basename(src_dir) + "_watermark")
    os.makedirs(out_dir, exist_ok=True)

    for fname in os.listdir(src_dir):
        fpath = os.path.join(src_dir, fname)
        if os.path.isfile(fpath) and fname.lower().endswith((".jpg", ".jpeg", ".png")):
            date = get_exif_date(fpath)
            if date:
                out_path = os.path.join(out_dir, fname)
                add_watermark(fpath, out_path, date, args.font_size, args.color, args.position)
                print(f"已处理: {fname}")

if __name__ == "__main__":
    main()
