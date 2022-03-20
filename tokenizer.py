#!/usr/bin/env python3
# coding: utf-8
# 提供幾種斷詞方法

# 一些語言學上的例外:
# itini, tini, aitinisa, anohatini => ini

import pickle
import json

stem_tags = pickle.load(open('./temp/stem-tags.pkl', 'rb'))
words = stem_tags.keys()
stems = set([v[0] for k,v in stem_tags.items() if v[0]])
sorted_stems = sorted(stems, key=lambda x: -len(x))

def longest_stem_match(word):
    for s in sorted_stems:
        if word.find(s) != -1:
            return s
    return None


def reparse_all_moedict():
    from glob import glob
    fnx = glob('../amis-moedict/docs/s/*.json')


def example():
    lexicon = json.load(open("../amis-moedict/docs/s/'a'adingalen.json"))
    ex = lexicon['h'][0]['d'][0]['e'][0].split(u'\ufff9')[1].split(u'\ufffa')[0].replace('`', '').replace('~', '')
    for w in ex.split():
        print(w, longest_stem_match(w), sep='\t')

if __name__ == '__main__':
    example()
