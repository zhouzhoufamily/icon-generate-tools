'''
Author: levi
Date: 2021-11-01 13:27:57
Description: icon generate tools
'''
# -*- coding:utf-8 -*-

import os

import sys

from pathlib import Path

from PIL import Image, ImageDraw

# circle_corner 切圆角算法原文链接：https://blog.csdn.net/bo_mask/article/details/106665380

def circle_corner(img, radii):
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 黑色方形内切白色圆形

    img = img.convert("RGBA")
    w, h = img.size

    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)),
                (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)),
                (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)),
                (0, h - radii))  # 左下角

    img.putalpha(alpha)		# 白色区域透明可见，黑色区域不可见

    return img


# ======= Android =======
AS_ICON_CFG_LIST = [
    ["ldpi", 36],
    ["mdpi", 48],
    ["hdpi", 72],
    ["xhdpi", 96],
    ["xxhdpi", 144],
    ["xxxhdpi", 192]
]

asOutDir = "./out_android"
asRadii = 180


def android_mask_icon(srcFile):
    if not os.path.isfile(srcFile) and not os.path.exists(srcFile):
        print("icon file name is err")
        return

    if not os.path.exists(asOutDir):
        os.mkdir(asOutDir)
        pass

    filePrefix = "drawable-"

    for cfg in AS_ICON_CFG_LIST:

        # 1. get icon cfg
        w = cfg[1]
        h = w
        dstPath = asOutDir+"/"+filePrefix+cfg[0]
        dstFile = dstPath+"/"+"icon.png"

        # 2. open image
        im = Image.open(srcFile)

        # 3. circle corner
        im = circle_corner(im, asRadii)

        # 4. scale image, ANTIALIAS and save icon
        if not os.path.exists(dstPath):
            os.mkdir(dstPath)
            pass

        im.resize((w, h), Image.ANTIALIAS).save(dstFile, "PNG", quality=100)


# ======= IOS =======
IOS_ICON_CFG_LIST = [
    ["Icon-16", 16],
    ["Icon-16@2x", 32],
    ["Icon-32", 32],
    ["Icon-32@2x", 64],
    ["Icon-128", 128],
    ["Icon-128@2x", 256],
    ["Icon-256", 256],
    ["Icon-256@2x", 512],
    ["Icon-512", 512],
    ["Icon-512@2x", 1024],
    ["Icon-20", 20],
    ["Icon-20@2x", 40],
    ["Icon-20@3x", 60],
    ["Icon-29", 29],
    ["Icon-29@2x", 58],
    ["Icon-29@3x", 87],
    ["Icon-40", 40],
    ["Icon-40@2x", 80],
    ["Icon-40@3x", 120],
    ["Icon-60@2x", 120],
    ["Icon-60@3x", 180],
    ["Icon-76", 76],
    ["Icon-76@2x", 152],
    ["Icon-83.5@2x", 167],
    ["Icon-1024", 1024],
    ["Icon-24@2x", 48],
    ["Icon-27.5@2x", 55],
    ["Icon-86@2x", 172],
    ["Icon-98@2x", 196],
    ["Icon-108@2x", 216],
    ["Icon-44@2x", 88],
    ["Icon-50@2x", 100]
]

iosOutDir = "./out_ios"


def ios_mask_icon(srcFile):
    if not os.path.isfile(srcFile) and not os.path.exists(srcFile):
        print("icon file name is err")
        return

    if not os.path.exists(iosOutDir):
        os.mkdir(iosOutDir)
        pass

    for cfg in IOS_ICON_CFG_LIST:

        # 1. get icon cfg
        w = cfg[1]
        h = w
        dstFile = iosOutDir+"/"+cfg[0]+".png"

        # 2. open image
        im = Image.open(srcFile)
        im.resize((w, h)).save(dstFile, "PNG", quality=100)


def mask_all_platform():

    if len(sys.argv) < 3:
        print("args err !, sample: python3 icon_generate_tools.py 1024x1024.png ANDROID")
        input("exit")
        return

    filePath = sys.argv[1]
    if not os.path.exists(filePath):
        print("args 1 src file path err!", filePath)
        input("exit")
        return

    plat = sys.argv[2]
    if plat == "ANDROID":
        android_mask_icon(filePath)
    elif plat == "IOS":
        ios_mask_icon(filePath)
    else:
        print("args 2 platform err!")


if __name__ == "__main__":

    print("## generate begin ...")

    mask_all_platform()

    print("## generate end .")
