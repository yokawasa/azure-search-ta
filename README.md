# azure-search-ta
Azure Search Text Analyze command line tool that shows how an analyzer breaks text into tokens utlizing Azure Search [Text Analyze API](https://azure.microsoft.com/en-us/documentation/articles/search-api-2015-02-28-preview/#test-analyzer).

## Installation


## 1. Preparation
### 1-1. Create Azure Search Account and configure search.conf

To enjoy text analysis using this command, you must create an Azure Search service in the Azure Portal. Please follow the instrucftion below:
 * [Create a service](https://azure.microsoft.com/en-us/documentation/articles/search-create-service-portal/)

Then configure search.conf once an Azure search account is created

```
# Azure Search Service Name ( never put space before and after = )
SEARCH_SERVICE_NAME=<Azure Search Service name>
# Azure Search API Admin Key ( never put space before and after = )
SEARCH_API_KEY=<Azure Search API Admin Key>
```

### 1-2. Create Index Schema to Analyze Text

You also need an index and analyzer definitions in the index to construct Azure search Text Analyze API request internally. For creating an index, please follow the instruction below

 * [Create an Azure Search index](https://azure.microsoft.com/en-us/documentation/articles/search-what-is-an-index/)
 * [Azure Search Service REST API:Version 2015-02-28-Preview](https://azure.microsoft.com/en-us/documentation/articles/search-api-2015-02-28-preview/#create-index)

For example, you can create the following test index in order to do text analysis for both Japanese Lucene and Microsoft Analyzer:

```
{
    "name": "jaanalyzertest",
    "fields": [
        { "name":"id", "type":"Edm.String", "key": true, "searchable": false },
        { "name":"content1", "type":"Edm.String", "filterable":false, "sortable":false, "facetable":false, "analyzer":"ja.lucene" },
        { "name":"content2", "type":"Edm.String", "filterable":false, "sortable":false, "facetable":false, "analyzer":"ja.microsoft" }
     ]
}
```

## 2. Executing command line
### azure-search-ta usage
```
usage: azure-search-ta.py [-h] [-v] [-c CONF] [-i INDEX] [-a ANALYZER]
                          [-t TEXT] [-o OUTPUT]

This program do text analysis and generate formatted output by using Azure
Search Text Analyze API

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONF, --conf CONF  Azure Search Configuration file. Default:search.conf
  -i INDEX, --index INDEX
                        Azure Search index name
  -a ANALYZER, --analyzer ANALYZER
                        Azure Search analyzer name
  -t TEXT, --text TEXT  A file path or HTTP(s) URL from which the command line
                        reads the text to analyze
  -o OUTPUT, --output OUTPUT
                        Output format ("simple" or "normal"). Default:normal
```


### Example1: Analyzing text from a file and 'normal' output format 
Suppose you want to read text from simple1.txt and make analysis for the text with ja.microsoft analyzer in jaanalyzertest index
```
$ cat sample1.txt
吾輩は猫である

$ azure-search-ta.py -c ./search.conf -i jaanalyzertest -a ja.microsoft --t sample1.txt
INPUT: 吾輩は猫である
TOKENS: [吾輩] [猫] [ある]
```


### Example2: Analyzing text from a file and 'simple' output format 
Suppose you want to read text from simple1.txt and make analysis for the text with ja.microsoft analyzer in jaanalyzertest index
```
$ cat sample1.txt
吾輩は猫である

$ azure-search-ta.py -c ./search.conf -i jaanalyzertest -a ja.microsoft --t sample1.txt -o simple
'吾輩' '猫' 'ある'
```

### Example3: Analyzing text from URL and 'simple' output format 
Suppose you want to read text from URL(http://www.yahoo.co.jp) and make analysis for the text with ja.microsoft analyzer in jaanalyzertest index
```
$ azure-search-ta.py -i jaanalyzertest -a ja.microsoft --t http://www.yahoo.co.jp -o simple

'yahoo!' 'japan' 'ヘルプ' 'yahoo!' 'japan' 'トップ' 'ページ' '機能' '正しく' 'ご' '利用' 'いただく' '下記' '環境' '必要' 'です' 'windows' 'internet' 'explorer' '9.0' 'nn9' '以上' 'chrome' '最新' '版' 'firefox' '最新' '版' 'microsoft' 'edge' 'macintosh' 'safari' '5.0' 'nn5' '以上' 'internet' 'explorer' '9.0' 'nn9' '以上' 'ご' '利用' '場合' 'internet' 'explorer' '互換' '表示' 'つい' 'て' '参考' '互換' '
表示' '無効化' 'お' '試し' 'ください' '多数' '高級' '車' '1円' 'スタート' 'ヤフオク' '出品' '本日' 'まで' 'ホテル' 'や' '旅館' 'お得' 'な' 'タイム' 'セール' 'これ' 'から' '出会う' '重要' '人物' '名字' '無料' '占おう' 'ニュース' '12時' '2分' '更新' '馬毛島' '政府' '買収'
 '最終' '調整' '朴' '氏' '最' '側近' 'も' '拘束' '証言' '注目' '病院' '食' '異臭' '塩素' '系' '成分' '検出' '乱暴' '疑惑' '慶大' '学生' '4人' '処分' '渋谷' '駅' '移設' 'へ' '銀座' '線' '一部' '運休' 'ソフト' 'めん' '給食' 'から' '消える' '清宮' 'ある' 'か' '早大' '経由' 'メジャー' 'メジア' 'アマゾン' 'cm' 'パパ' '好演' '反響' 'もっと' '見る' '記事' '一覧' '黒田' 'ありがとう' '11月' '5日' '10時' '59分' '配信' '毎日' '新聞' 'ショッピング' 'ヤフオク' '旅行' 'ホテル' '予約' 'ニュース' '天気' 'スポーツ' 'ナビ' 'ファイナンス' 'テレビ' 'gyao' 'y' 'モバゲー' 'モバゲ' '地域' '地図' '路線' '食べ' 'ログ' '求人' 'アルバイト' '不動産' '自動車' '掲示' '板' 'ブログ' 'ビューティー' 'ビューチ' '出会い' '電子' '書籍' '映画' 'ゲーム' '占い' 'サービス' '一覧' 'ログイン' 'id' 'もっと' '便利' '新規' '取得' 'メール' 'メール' 'アドレス' '取得' 'カレンダー' 'カレンダ' 'カレンダー' 'カレンダ' '活用' 'ポイント' '確認' 'ログイン' '履歴' '確認' '会社' '概要' '
投資' '家' '情報' '社会的' '責任' '企業' '行動' '憲章' '広告' '掲載' 'つい' 'て' '採用' '情報' '利用' '規約' '免責' '事項' 'メディア' 'メデーア' 'ステートメント' 'ステトメント' 'セキュリティー' 'セキュリチ' '考え方' 'プライバシー' 'プライバシ' 'ポリシー' 'ポリシ' 'copyr
ight' 'c' '2016' 'nn2016' 'yahoo' 'japan' 'corporation' 'all' 'rights' 'reserved'

```

## Todo

* Support HTML output format option


### Example2: Output format normal
