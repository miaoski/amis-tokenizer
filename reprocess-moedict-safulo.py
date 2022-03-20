#!/usr/bin/env python3
# coding: utf-8
# 阿美語萌典蔡中涵大辭中: 重新產生例句的超連結

import pickle
import json
from tokenizer import COMMON_PREFIXES
from glob import glob
import re

stem_tags = pickle.load(open('./temp/stem-tags.pkl', 'rb'))
vocabulary = [x.lower() for x in stem_tags.keys()]
stems = set([v[0].lower() for k,v in stem_tags.items() if v[0]])
sorted_stems = sorted(stems, key=lambda x: -len(x))

PUNCTUATIONS = re.compile(r"""([".,:;?/ -])""")

def longest_stem_match(word):
    for s in sorted_stems:
        p = word.rfind(s)
        if p != -1:
            return (p, p + len(s))
    return None


def remove_links(ami):
    return ami.replace('~', '').replace('`', '')

def add_links(ami):
    words = PUNCTUATIONS.split(ami)
    for i, w in enumerate(words):
        if PUNCTUATIONS.match(w):
            continue
        if w.lower() in vocabulary:
            words[i] = '`' + w + '~'
        else:
            p = longest_stem_match(w.lower())
            if p:
                words[i] = w[:p[0]] + '`' + w[p[0]:p[1]] + '~' + w[p[1]:]
    return ''.join(words)

def process(lexicon):
    for i_h, h in enumerate(lexicon['h']):
        for i_d, d in enumerate(h['d']):
            if 'e' in d:
                for i_e, e in enumerate(d['e']):
                    ami, xs = e.split(u'\ufff9')[1].split(u'\ufffa', 1)
                    eng, cmn = xs.split(u'\ufffb', 1)
                    ami = remove_links(ami)
                    ami = add_links(ami)
                    lexicon['h'][i_h]['d'][i_d]['e'][i_e] = u'\ufff9{}\ufffa{}\ufffb{}'.format(ami, eng, cmn)
            if 'r' in d:
                for i_r, r in enumerate(d['r']):
                    nr = remove_links(r)
                    nr = add_links(nr)
                    lexicon['h'][i_h]['d'][i_d]['r'][i_r] = nr
            if 's' in d:
                for i_s, r in enumerate(d['s']):
                    nr = remove_links(r)
                    nr = add_links(nr)
                    lexicon['h'][i_h]['d'][i_d]['s'][i_s] = nr
    return lexicon

if __name__ == '__main__':
    from pprint import pprint
    from colorama import Fore, Style
    from copy import deepcopy
    fnx = glob('../amis-moedict/docs/s/*.json')
    num_i = 0

    DEBUG = False
    for fn in fnx:
        pro = json.load(open(fn))
        if 't' not in pro:                      # Not a lexicon
            print('Ignore file:', fn)
            continue
        org = deepcopy(pro)
        process(pro)
        if pro != org:
            if DEBUG:
                print(Fore.YELLOW, end='')
                pprint(org)
                print(Style.RESET_ALL, end='')
                print(Fore.GREEN, end='')
                pprint(pro)
                print(Style.RESET_ALL, end='')
            else:
                print('* Updating', fn)
                with open(fn, 'w') as f:
                    f.write(json.dumps(pro, ensure_ascii=False, separators=(',', ':')))
        else:
            if DEBUG:
                print('!!! Identical:', org['t'])
            num_i += 1

    print(f'{num_i} / {len(fnx)} are identical.')
