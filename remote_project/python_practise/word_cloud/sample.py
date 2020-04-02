#! /usr/bin/env python
# encoding: utf-8
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

from os import path
import random
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

d = path.dirname(__file__)
font_path = path.join(d, 'DroidSansFallbackFull.ttf')

mask = np.array(Image.open(path.join(d, 'stormtrooper_mask.png')))


def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


# Read the whole text.
text = open(path.join(d, 'santi.txt'), encoding='gbk').read()

stopwords = set(STOPWORDS)
stopwords.add('int')
stopwords.add('ext')

# Generate a word cloud image
wordcloud = WordCloud(font_path=font_path, max_font_size=2000, mask=mask, stopwords=stopwords).generate(text)
wordcloud.to_file('a_old_hope.png')
# Display the generated image:
# the matplotlib way:
default_colors = wordcloud.to_array()

plt.title('Custom Colors')
plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3))
wordcloud.to_file('a_new_hope.png')
plt.axis("off")

# lower max_font_size
# wordcloud = WordCloud(font_path=font_path, max_font_size=40, mask=mask).generate(text)
plt.figure()
plt.title('词云')
plt.imshow(default_colors)
plt.axis("off")
plt.show()
