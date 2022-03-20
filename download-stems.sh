#!/bin/bash
# 從阿美語萌典下載字典列表及詞幹檔
curl https://raw.githubusercontent.com/g0v/amis-moedict/master/docs/s/ch-mapping.json -o ./temp/ch-mapping.json
curl https://raw.githubusercontent.com/g0v/amis-moedict/master/docs/s/stem-words.json -o ./temp/stem-words.json
