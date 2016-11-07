# azure-search-ta
Azure Search Text Analyze command line tool that shows how an analyzer breaks text into tokens utlizing Azure Search [Analyze API](https://azure.microsoft.com/en-us/documentation/articles/search-api-2015-02-28-preview/#test-analyzer).

## 1. Installation
Install [azure-search-ta](https://pypi.python.org/pypi/azure-search-ta) python package by uinsg [pip](https://pip.pypa.io/en/stable/). Pip is a package management system used to install and manage software packages, such as those found in the [Python Package Index](https://pypi.python.org/pypi).
```
pip install azure-search-ta
```

## 2. Preparation
### 2-1. Create Azure Search Account and configure search.conf

To enjoy text analysis using this command, you must create an Azure Search service in the Azure Portal. Please follow the instrucftion below:
 * [Create a service](https://azure.microsoft.com/en-us/documentation/articles/search-create-service-portal/)

Once the Azure search account is created, add Azure Search service name and API Key to the following search.conf file. Regarding API Key, an admin key must be added instead of a query key as the Analyze API request requires an admin key.

```
# Azure Search Service Name ( never put space before and after = )
SEARCH_SERVICE_NAME=<Azure Search Service name>
# Azure Search API Admin Key ( never put space before and after = )
SEARCH_API_KEY=<Azure Search API Admin Key>
```

### 2-2. Create Index Schema to Analyze Text

You need an index name to construct Azure Search Analyze API request internally in the tool. For creating an index, please follow the instruction below

 * [Create an Azure Search index](https://azure.microsoft.com/en-us/documentation/articles/search-what-is-an-index/)
 * [Azure Search Service REST API:Version 2015-02-28-Preview](https://azure.microsoft.com/en-us/documentation/articles/search-api-2015-02-28-preview/#create-index)

Regardless of your index definitions you can test with any Azure Search's **predefined analyzers**. Therefore the following index schema (index name:'ta') is enough for the testing with predefined analyzers:
```
{
    "name": "ta",
    "fields": [
        { "name":"id", "type":"Edm.String", "key": true, "searchable": false },
        { "name":"content", "type":"Edm.String" }
     ]
}
```

In the meanwhile, in order for you to test with your **custom analyzer**, you need to define the custom analyzer in your index definition. Here is a sample index schema (index name: 'tacustom') that has custom analyzer definition:

```
{
    "name":"tacustom",
    "fields":[
        { "name":"id", "type":"Edm.String", "key":true, "searchable":false },
        { "name":"content","type":"Edm.String", "analyzer":"my_ngram" }
    ],
    "analyzers":[
        {
        "name":"my_ngram",
        "@odata.type":"#Microsoft.Azure.Search.CustomAnalyzer",
        "charFilters": ["html_strip"],
        "tokenizer":"my_tokenizer",
        "tokenFilters":[ "cjk_width","lowercase" ]
        }
    ],
    "tokenizers":[
        {
        "name":"my_tokenizer",
        "@odata.type":"#Microsoft.Azure.Search.NGramTokenizer",
        "minGram":2,
        "maxGram":5
        }
    ]
}
```

[NOTE] For **predefined analyzers**, please refer to [Language support (Azure Search Service REST API)](https://msdn.microsoft.com/en-us/library/azure/dn879793.aspx) and [this document](https://msdn.microsoft.com/en-us/library/azure/mt605304.aspx)'s [Analyzers' section](https://msdn.microsoft.com/en-us/library/azure/mt605304.aspx#AnalyzerTable). For **custom analyzers**, please refer to [Custom analyzers in Azure Search](https://msdn.microsoft.com/en-us/library/azure/mt605304.aspx).


## 3. Executing command
### azure-search-ta usage
```
usage: azure-search-ta [-h] [-v] [-c CONF] [-i INDEX] [-a ANALYZER]
                          [-t TEXT] [-o OUTPUT]

This program do text analysis and generate formatted output by using Azure
Search Analyze API

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


### Example1: Analyzing text from a file with ja.microsoft analyzer and 'normal' output format 
Suppose you want to read text from simple1.txt and make analysis for the text with ja.microsoft analyzer
```
$ cat sample1.txt
吾輩は猫である

$ azure-search-ta -c ./search.conf -i ta -a ja.microsoft --t sample1.txt
INPUT: 吾輩は猫である
TOKENS: [吾輩] [猫] [ある]
```


### Example2: Analyzing text from a file with ja.microsoft analyzer and 'simple' output format 
Suppose you want to read text from simple1.txt and make analysis for the text with ja.microsoft analyzer
```
$ cat sample1.txt
吾輩は猫である

$ azure-search-ta -c ./search.conf -i ta -a ja.microsoft --t sample1.txt -o simple
'吾輩' '猫' 'ある'
```

### Example3: Analyzing text from a file with custome analyzer and 'simple' output format 
Suppose you want to read text from simple1.txt and make analysis for the text with custom analyzer ('my_ngram') defined in tacustom index
```
$ cat sample1.txt
吾輩は猫である

$ azure-search-ta -c ./search.conf -i tacustom -a my_ngram --t sample1.txt -o simple
'吾輩' '吾輩は' '吾輩は猫で' '吾輩は猫' '輩は猫であ' '輩は' '輩は猫' '輩は猫で' 'は猫であ' 'は猫で' 'は猫' 'は猫である' '猫であ' '猫で' '猫で ある' 'である' 'であ' 'ある'
```

### Example4: Analyzing text from URL with ja.lucene analyzer and 'simple' output format 
Suppose you want to read text from URL(http://www.yahoo.co.jp) and make analysis for the text with ja.lucene analyzer

```
$ azure-search-ta -i ta -a ja.lucene --t http://www.yahoo.co.jp -o simple

'yahoo' 'japan' 'ヘルプ' 'yahoo' 'japan' 'トップページ' '機能' '正しく' 'ご' '利用' 'いただく' '下記' '環境' '必要' 'windows' 'internet' 'explorer' '9' '0' '以上' 'chrome' '最新' '版' 'firefox' '最新' '版' 'microsoft' 'edge' 'macintosh' 'safari' '5' '0' '以上' 'internet' 'explorer' '9' '0' '以上' 'ご' '利用' '場合' 'internet' 'explorer' '互換' '表示' '参考' '互換' '表示' '無効' '化' '試し' 'くださる' 'キャンペーン' '参加' '家電' 'ブランド' '品' 'ポイント' '11' '倍' 'ユニバーサル' 'スタジオ' 'ジャパン' 'ご' '招待' '電子' '書籍' '5' '冊' '購入' '555' 'ポイント' ' 進呈' 'ニュース' '6' '時' '34' '分' '更新' '韓国' '前' '首席' '秘書官' '逮捕' '男児' '不明' '父' '供述' '浮かぶ' '謎' '事故' '車外' '出る' 'はねる' '死亡' '麻薬' '取引' '疑惑' '市長' '射殺' '比' 'パナ' 'led' '電球' '5' '年' '保証' '過去' 'ジョコビッチ' '世界' '1' '位' '陥落' 'ガイア' '夜明け' '心' '刺さる' '訳' 'さんま' '初' '紅白' '出演' '濃厚' 'もっと' '見る' '記事' '一覧' '夜' 'ワラ' 'ゴジラ' '11' '月' '5' '日' '19' '時' '40' '分' '配信' '時事' '時事通信' '通信' 'ショッピング' 'ヤフオク' '旅行' 'ホテル' '予約' 'ニュース' '天気' 'スポーツナビ' 'ファイナンス' 'テレビ' 'gyao' 'y' 'モバゲ' '地域' '地図' '路線' '食べる' 'ログ' '求人' 'アルバイト' '不動産' '自動車' '掲示板' 'ブログ' 'ビューティ' '出会い' '電子' '書籍' '映画' 'ゲーム' '占い' 'サービス' '一覧' 'ログイン' 'id' 'もっと' '便利' '新規' '取得' 'メール' 'メールアドレス' '取得' 'カレンダ' 'カレンダ' '活用' 'ポイント' '確認' 'ログイン' '履歴' '確認' '会社' '概要' '投資' '家' '情報' '社会' '的' '責任' '企業' '行動' '憲章' '広 告' '掲載' '採用' '情報' '利用' '規約' '免責' '事項' 'メディア' 'ステートメント' 'セキュリティ' '考え方' 'プライバシ' 'ポリシ' 'copyright' 'c' '2016' 'yahoo' 'japan' 'corporation' 'all' 'rights' 'reserved'
```

Suppose you want to read text from URL(http://news.microsoft.com/ja-jp/) and get the 10 most popular keywords that are contained in the results of test analysis with ja.lucene analyzer

```
azure-search-ta -i ta -a ja.lucene --t http://news.microsoft.com/ja-jp/ -o simple | tr " " "\n" | sort |uniq -c | sort -nr |head -10

     97 'ストア'
     74 'デバイス'
     71 'マイクロソフト'
     39 '日本'
     32 '株式会社'
     32 '株式'
     32 '会社'
     30 'ソフトウェア'
     29 'microsoft'
     27 '2016'
```

## Todo

* Support HTML output format option

## Change log

* [Changelog](ChangeLog.md)

## Links

* https://pypi.python.org/pypi/azure-search-ta/
* [Azure Search Analyze API](https://azure.microsoft.com/en-us/documentation/articles/search-api-2015-02-28-preview/#test-analyzer)
* [Language support (Azure Search Service REST API)](https://msdn.microsoft.com/en-us/library/azure/dn879793.aspx) 
* [Custom analyzers in Azure Search](https://msdn.microsoft.com/en-us/library/azure/mt605304.aspx)

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/yokawasa/azure-search-ta.

## Copyright

<table>
  <tr>
    <td>Copyright</td><td>Copyright (c) 2016- Yoichi Kawasaki</td>
  </tr>
  <tr>
    <td>License</td><td>MIT</td>
  </tr>
</table>
