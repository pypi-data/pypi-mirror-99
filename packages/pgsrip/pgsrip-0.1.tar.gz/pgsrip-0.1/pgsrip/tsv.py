# -*- coding: utf-8 -*-
import re
from typing import Tuple


class TsvDataItem:

    def __init__(self, level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf, text):
        self.level = int(level)
        self.page_num = int(page_num)
        self.block_num = int(block_num)
        self.par_num = int(par_num)
        self.line_num = int(line_num)
        self.word_num = int(word_num)
        self.left = int(left)
        self.top = int(top)
        self.width = int(width)
        self.height = int(height)
        self.conf = int(conf)
        self.text = text

    def __repr__(self):
        return f'<{self.__class__.__name__} [{str(self)}]>'

    def __str__(self):
        return f'{(self.top, self.left)}{self.text}'

    @property
    def h_center(self):
        return self.top + self.height // 2

    @property
    def w_center(self):
        return self.left + self.width // 2

    def matches(self, shape: Tuple[int, int, int, int]):
        h_start, w_start, h_end, w_end = shape
        return h_start <= self.h_center <= h_end and w_start <= self.w_center <= w_end


class TsvData:

    NON_WORD_RE = re.compile(r'\W')

    def __init__(self, data: dict):
        keys = data.keys()
        items = [TsvDataItem(**{k: values[i] for (i, k) in enumerate(keys)}) for values in (
            zip(*[data[key] for key in keys]))]
        items.sort(key=lambda x: x.word_num)
        items.sort(key=lambda x: x.line_num)
        items.sort(key=lambda x: x.par_num)
        items.sort(key=lambda x: x.block_num)
        items.sort(key=lambda x: x.page_num)
        self.items = items
        self.words = {text for text in [self.NON_WORD_RE.sub('', item.text) for item in items] if text}

    def select(self, shape: Tuple[int, int, int, int]):
        return [item for item in self.items if item.level == 5 and item.matches(shape)]

    def has_word(self, word: str):
        return self.NON_WORD_RE.sub('', word) in self.words
