#!/usr/bin/python
# -*- encoding: UTF-8 -*-
# test created on 14-10-28 下午12:48
# Copyright 2014 offbye@gmail.com
# http://blog.csdn.net/offbye/article/details/40538675

"""
生成带logo的二维码
"""

__author__ = ['"Xitao":<offbye@gmail.com>']

import qrcode
from PIL import Image
import os


def gen_qrcode(string, path, logo=""):
    """
    生成中间带logo的二维码
    需要安装qrcode, PIL库

    :param string: 二维码字符串
    :param path: 生成的二维码保存路径
    :param logo: logo文件路径
    :return:
    """
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=1
    )
    qr.add_data(string)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")

    if logo and os.path.exists(logo):
        icon = Image.open(logo)
        img_w, img_h = img.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        icon = icon.convert("RGBA")
        img.paste(icon, (w, h), icon)
    img.save(path)

if __name__ == "__main__":
    gen_qrcode("http://offbye.com","qr.png", "logo.png")
