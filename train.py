import re

from typing import List


def train(init_dir, model):
    text = input() if init_dir is None or init_dir == '' \
        else get_text_from_dir(init_dir)
    corpus = generate_corpus(text)


def generate_corpus(text):
    corp = dict()
    words = [clear_text(word) for word in text.split()]

    for i in range(len(words) - 1):

        if words[i] in corp.keys():
            corp[words[i]].append(words[i + 1])
        else:
            corp[words[i]] = [words[i + 1]]

    return corp


def get_text_from_dir(dir):
    with open(dir, 'r') as file:
        text = file.read()

    return text


def clear_text(text):
    regex = re.compile('[^a-zA-Zа-яА-Я]')
    res_text = regex.sub('', text)

    return res_text.lower()
