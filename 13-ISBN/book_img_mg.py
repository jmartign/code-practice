# coding:utf-8
from __future__ import print_function
from StringIO import StringIO
import os
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests


# I took picture of my books, then want to paste ISBN# in those pictures
# ** notice: im.rotate() does not change image size, but im.transpose()


def get_isbn_img(isbn):
    url = 'http://b.wwei.cn/html/image.php'
    payload = {
        'filetype':'PNG',
        'dpi': 72,
        'scale': 1,
        'rotation': 0,
        'font_family': 'Arial.ttf',
        'font_size': 8,
        'text': isbn,
        'thickness': 30,
        'code': 'BCGisbn',
    }
    r = requests.get(url, params=payload)
    return Image.open(StringIO(r.content))


MARGIN = 10

def get_isbn_from_filepath(filepath):
    name = os.path.basename(filepath)
    if name.startswith('9'):
        return os.path.splitext(name)[0]
    return None


def get_output_filepath(filepath):
    dir = os.path.join(os.path.dirname(filepath), 'out')
    if not os.path.exists(dir):
        os.mkdir(dir)
    return os.path.join(dir, os.path.basename(filepath))


def process_book_picture(pic_filepath):
    isbn = get_isbn_from_filepath(pic_filepath)
    if not isbn:
        return
    im = Image.open(pic_filepath)
    # print(im.format, im.size, im.mode)
    
    new_size = (lambda x: (x[0] * 400 / x[1], 400))(im.size)
    out_img = im.resize(new_size).transpose(Image.ROTATE_90)
    # enhance image
    out_img = out_img.point(lambda i: i * 1.2).filter(ImageFilter.SHARPEN)
    
    isbn_box = paste_isbn_img(out_img, isbn)
    draw_copyright_words(out_img, (isbn_box[2] + MARGIN, isbn_box[3] - 20))
    out_img.save(get_output_filepath(pic_filepath))


def paste_isbn_img(out_img, isbn):
    isbn_img = get_isbn_img(isbn)
    y_0 = out_img.size[1] - isbn_img.size[1] - MARGIN
    isbn_box = (MARGIN, y_0, MARGIN + isbn_img.size[0], y_0 + isbn_img.size[1])

    out_img.paste(isbn_img, isbn_box)
    return isbn_box


def draw_copyright_words(out_img, xy):
    fnt = ImageFont.truetype('cour.ttf', 16)
    draw = ImageDraw.Draw(out_img)
    draw.text(xy, '@lizbew ^.^', font=fnt, fill=(0, 0, 0))
    del draw 


if __name__ == '__main__':
    for f in glob.glob(r'mybook\*.JPG'):
        process_book_picture(f)
