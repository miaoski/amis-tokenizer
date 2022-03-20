# amis-tokenizer
蔡中涵字典的 tokenizer ，主要用在阿美語萌典的斷詞。

# 說明
1. 蔡中涵委員修改字典的權威來源，在 2022.3.20 之後是 https://github.com/g0v/amis-moedict/tree/master/docs/s
1. 以下檔案應該由 CI/CD 產生 (TODO):
  1. ch-mapping.json 
  1. stem-words.json
  1. index.json
1. 本 repo 的公用程式可用於單詞的成份分析，以及配合阿美語萌典的格式，產生如下的斷詞結果 (單字 `'a'adingalen` 字根: `'adingal`):
```
"￹`O~ 'a`'adingal~en `ira~ `itini~.￺￻她要在這裡洗頭髮。"
```

# 目錄結構
`./temp` 是從阿美語萌典抓下來的暫存檔。

# 版權
版權以 GPLv2 宣告。
