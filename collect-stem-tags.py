# Python3
# coding: utf-8

from glob import glob
import json
import pickle
from tqdm import tqdm

stem_tags = {}
fnx = glob('../amis-moedict/docs/s/*.json')     # 請先 git clone 到 ../amis-moedict/
for fn in tqdm(fnx):
    try:
        with open(fn) as f:
            word = json.load(f)
            stem = word.get('stem')
            tag = word.get('tag')
            stem_tags[word['t']] = [stem, tag]
    except KeyboardInterrupt:
        break
    except:
        print('無法解析檔案:', fn)
        pass

with open('./temp/stem-tags.pkl', 'wb') as f:
    pickle.dump(stem_tags, f)
