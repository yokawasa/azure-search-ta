#!/bin/sh

SERVICE_NAME='Azure Search Service Name'
ADMIN_KEY='Azure Search API Admin Key'
API_VER='2015-02-28-Preview'
CONTENT_TYPE='application/json'
URL="https://${SERVICE_NAME}.search.windows.net/indexes?api-version=${API_VER}"

curl -s\
 -H "Content-Type: ${CONTENT_TYPE}"\
 -H "api-key: ${ADMIN_KEY}"\
 -XPOST ${URL} -d'{
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
}'
