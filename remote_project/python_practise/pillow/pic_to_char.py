import argparse
from PIL import Image

parser = argparse.ArgumentParser()

# file -o test.txt --width 100 --height 100

parser.add_argument('file')
parser.add_argument('-o', '--output')
parser.add_argument('--width', type=int, default=80)
parser.add_argument('--height', type=int, default=80)

args = parser.parse_args()

IMAGE = args.file
OUTPUT_FILE = args.output
WIDTH = args.width
HEIGHT = args.height

# ASCII_CHAR = [chr(i) for i in range(0, 256)]
ASCII_CHAR = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    gray = 0.2126 * r + 0.7152 * g + 0.0722 * b
    unit = (256+1)/len(ASCII_CHAR)
    return ASCII_CHAR[int(gray/unit)]


def get_content(image):
    txt = ''
    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*image.getpixel((j, i)))
        txt += '\n'
    return txt


def run():
    # if not Image.isImageType(IMAGE):
    #     raise ValueError('Wrong Image File')
    image = Image.open(IMAGE)
    # image.size = WIDTH, HEIGHT
    image = image.resize((WIDTH, HEIGHT), Image.NEAREST)
    txt = get_content(image)

    if OUTPUT_FILE:
        with open(OUTPUT_FILE, 'w') as f:
            f.write(txt)
    else:
        print(txt)


if __name__ == '__main__':
    run()
