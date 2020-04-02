# coding:utf-8
import random
import time
import os
import numexpr
import numpy
from PIL import Image, ImageFont, ImageDraw

STA = time.time()

root = os.getcwd() + "/resoures/"  # root: 脚本的根目录

W_num = 3  # W_num: 一行放多少张照片 将 W_num 设置为更大的值可以取得更好的效果，例如 7，15

H_num = 3  # H_num: 一列放多少张照片

W_size = 640  # W_size: 照片宽为多少

H_size = 360  # H_size: 照片高为多少

alpha = 0.5  # 透明度
aval = []  # aval: 存放所有照片的路径


def getAllPhotos():
    """
    得到待处理的图片路径
    :return:
    """
    STA = time.time()
    src = root + "photos/"
    for i in os.listdir(src):
        """如果文件是.jpg or .png 就添加到处理列表中"""
        if os.path.splitext(src + i)[-1] == ".jpg" or os.path.splitext(src + i)[-1] == ".png":
            aval.append(src + i)
    return aval


def scale(img_path, dst_width, dst_height):
    """
    指定图片大小
    :param img_path:
    :param dst_width:
    :param dst_height:
    :return:
    """
    STA = time.time()
    im = Image.open(img_path)
    if im.mode != "RGBA":
        im = im.convert("RGBA")  # 强制图片为RGBA格式

    s_w, s_h = im.size
    if s_w < s_h:
        im = im.rotate(90)  # 当宽度小于高度时，旋转90度

    resized_img = im.resize((dst_width, dst_height), Image.ANTIALIAS)
    resized_img = resized_img.crop((0, 0, dst_width, dst_height))  # 生成矩阵
    print("scale Func Time %s" % (time.time() - STA))

    return resized_img


def jointAndBlend():
    """
    实现图片拼接混合
    :return:
    """
    iW_size = W_num * W_size
    iH_size = H_num * H_size
    resized_img = scale(root + "lyf.jpg", iW_size, iH_size)  # resize 后的图片
    I = numpy.array(resized_img)
    I = numexpr.evaluate("""I*(1-alpha)""")  # 调节透明度

    """从上到下, 从左到右, 进行操作"""
    for i in range(W_num):
        for j in range(H_num):
            SH = I[(j * H_size):((j + 1) * H_size), (i * W_size):((i + 1) * W_size)]
            STA = time.time()
            DA = scale(random.choice(aval), W_size, H_size)
            print("Cal Func Time %s" % (time.time() - STA))
            res = numexpr.evaluate("""SH+DA*alpha""")
            I[(j * H_size):((j + 1) * H_size), (i * W_size):((i + 1) * W_size)] = res

    Image.fromarray(I.astype(numpy.uint8)).save("blend.png")


def rotate():
    imName = "blend.png"
    print("正在将图片旋转中...")
    STA = time.time()
    im = Image.open(imName)
    im2 = Image.new("RGBA", (W_size * int(W_num + 1), H_size * (H_num + 4)))
    im2.paste(im, (int(0.5 * W_size), int(0.8 * H_size)))
    im2 = im2.rotate(359)
    im2.save("rotate.png")
    print("rotate Func Time %s" % (time.time() - STA))


def addText():
    print("正在向图片中添加祝福语...")
    img = Image.open("blend.png")
    fontWeight = W_num * W_size // 12
    font = ImageFont.truetype('xindexingcao57.ttf', fontWeight)
    draw = ImageDraw.Draw(img)
    draw.ink = 21 + 118 * 256 + 65 * 256 * 256

    #    draw.text((0,H_size * 6),unicode("happy every day",'utf-8'),(0,0,0),font=font)

    draw.text((W_size * 0.5, fontWeight), "happy life written by python", font=font)
    img.save("addText.png")


if __name__ == '__main__':
    getAllPhotos()  # 得到待处理图片
    # jointAndBlend()  # 进行拼接混合
    # rotate()  # 旋转
    addText()  # 添加文本
    print("Total Time %s" % (time.time() - STA))
