#!/usr/bin/env python3
# coding: utf-8
# 提供幾種斷詞方法

# 一些語言學上的例外:
# itini, tini, aitinisa, anohatini => ini

import pickle
import json
from colorama import Fore, Style

COMMON_PREFIXES = {
        'mapapipa': 'mapa-pipa',
        'mapaka': 'ma-paka',
        'mipaka': 'mi-paka',
        'sakaci': 'saka-ci',
        'sapipa': 'sapi-pa',
        'mapa': 'mapa',
        'masa': 'masa',
        'miki': 'miki',
        'misa': 'misa',
        'saka': 'saka',
        'sapi': 'sapi',
        'paka': 'paka',
        'ka': 'ka',
        'ma': 'ma',
        'mi': 'mi',
        'pa': 'pa',
        'pi': 'pi',
        'sa': 'sa',
        }

stem_tags = pickle.load(open('./temp/stem-tags.pkl', 'rb'))
words = stem_tags.keys()
stems = set([v[0] for k,v in stem_tags.items() if v[0]])
sorted_stems = sorted(stems, key=lambda x: -len(x))

def longest_stem_match(word):
    for s in sorted_stems:
        if word.find(s) != -1:
            return s
    return None

def phoneme_encode(w):
    return w.replace('ng', 'G')

def phoneme_decode(w):
    return w.replace('G', 'ng')

def dashes(*args):
    xs = [x for x in args if len(x) > 0]
    return '-'.join(xs)

def tokenize(word):
    """假設 word 是字典中已知的詞
    """
    import re
    if word not in stem_tags:
        print('不在字典中的詞:', word)
        return None
    stem = stem_tags[word][0]
    frame = {'word': word, 'stem': '', 'prefix': '', 'suffix': '', 'type': None, 'tokens': word, 'dup': ''}
    if stem is None:
        return frame

    frame['stem'] = stem
    p = word.rfind(stem)
    if p == -1:
        # 'apilis -> 'a-pili-pilisan
        core = re.match('(.+)([^aeiou][aeiou][^aeiou][aeiou])(.+)', stem)
        if len(stem) >= 6 and core:
            pre, mid, suf = core.groups()
            if word.startswith(pre + mid + mid + suf):
                frame['type'] = 'IN_CVCV'
                suffix = word[len(pre + mid + mid + suf):]
                frame['tokens'] = dashes(pre, mid, mid+suf, suffix)
                return frame
        else:
            return frame
    prefix = word[:p]
    suffix = word[p + len(stem):]

    p = phoneme_encode(prefix)
    s = phoneme_encode(stem)
    w = phoneme_encode(word)
    dup = None
    if prefix in COMMON_PREFIXES:
        frame['prefix'] = COMMON_PREFIXES[prefix]
        frame['suffix'] = suffix
        frame['tokens'] = dashes(frame['prefix'], stem, suffix)
        return frame

    # Ca-C
    dup = s[0] + 'a'
    if len(p) == 2 and w.startswith(dup + s):
            frame['type'] = 'Ca-CV'
            frame['prefix'] = ''
            frame['dup']    = phoneme_decode(dup)
            frame['suffix'] = suffix
            frame['tokens'] = dashes(phoneme_decode(dup), stem, suffix)
            return frame
    # pa-CVCV-CVCVC-an, e.g., pa-tera-tera'-han (疑為 pateraterahan), masa-hefo-hefong
    # mi-CVCV-CVCV-an, e.g., misa-moli-moli-an
    if len(s) >= 4:
        dup = s[:4]
        if p[-len(dup):] == dup and p[:-4] in COMMON_PREFIXES:
            frame['type'] = 'CVCVC'
            real_prefix = phoneme_decode(p[:-len(dup)])
            frame['prefix'] = COMMON_PREFIXES.get(real_prefix, real_prefix)
            frame['dup']    = phoneme_decode(dup)
            frame['suffix'] = suffix
            frame['tokens'] = dashes(frame['prefix'], phoneme_decode(dup), stem, suffix)
            return frame
    # mi-CaCVCV-CVCVC-an, e.g., mi-tatongo-tongod-an
        dup = '{}a{}'.format(s[0], s[:4])
        if p[-len(dup):] == dup:
            frame['type'] = 'CaCVCVC'
            real_prefix = phoneme_decode(p[:-len(dup)])
            frame['prefix'] = COMMON_PREFIXES.get(real_prefix, real_prefix)
            frame['dup']    = phoneme_decode(dup)
            frame['suffix'] = suffix
            frame['tokens'] = dashes(frame['prefix'], stem, suffix)
            return frame

    # 不負責猜測
    frame['prefix'] = COMMON_PREFIXES.get(prefix, prefix)
    frame['suffix'] = suffix
    frame['tokens'] = dashes(frame['prefix'], stem, suffix)
    return frame

def strip_moedict_hyperlink(w):
    return w.replace('`', '').replace('~', '')

def parse_moedict(lexicon):
    for h in lexicon['h']:
        for d in h['d']:
            for e in d['e']:
                ami = e.split(u'\ufff9')[1].split(u'\ufffa')[0]
                eng, cmn = e.split(u'\ufff9')[1].split(u'\ufffa')[1].split(u'\ufffb')
                ami = strip_moedict_hyperlink(ami)


def reparse_all_moedict():
    from glob import glob
    fnx = glob('../amis-moedict/docs/s/*.json')
    for fn in fnx:
        with open(fn) as f:
            word = json.load(f)
            if 't' in word:
                k = word['t']
                v = stem_tags.get(k, (None, None))
                if v[0] is None:
                    continue
                tok = tokenize(k)
                if tok['type'] is None:
                    continue
                print(f'{v[1]}\t{k:30}{Fore.YELLOW}{tok["prefix"]} {Fore.RED}{tok["dup"]} {Fore.GREEN}{tok["stem"]}{Fore.LIGHTBLUE_EX} {tok["suffix"]}{Style.RESET_ALL}\t{tok["type"]}\t{tok["tokens"]}')

def evaluate(fm, to):
    for k in list(stem_tags.keys())[fm:to]:
        v = stem_tags[k]
        if v[0] is None:
            continue
        tok = tokenize(k)
        if k == tok['stem']:
            assert 0, 'word == stem'
        print(f'{v[1]}\t{k:30}{Fore.YELLOW}{tok["prefix"]} {Fore.RED}{tok["dup"]} {Fore.GREEN}{tok["stem"]}{Fore.LIGHTBLUE_EX} {tok["suffix"]}{Style.RESET_ALL}\t{tok["type"]}\t{tok["tokens"]}')

if __name__ == '__main__':
    pass
