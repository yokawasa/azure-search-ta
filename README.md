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
                          [-t TEXTFILE] [-o OUTPUT]

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
  -t TEXTFILE, --textfile TEXTFILE
                        Text file to read and analyze
  -o OUTPUT, --output OUTPUT
                        Output format ("simple" or "normal"). Default:normal
```


### Example1: Output format normal
Suppose you want to do text analysis for ja.microsoft analyzer in jaanalyzertest index
```
$ cat sample1.txt
吾輩は猫である

$ azure-search-ta.py -c ./search.conf -i jaanalyzertest -a ja.microsoft --t sample1.txt
INPUT: 吾輩は猫である
TOKENS: [吾輩] [猫] [ある]
```


### Example2: Output format normal
Suppose you want to do text analysis for ja.microsoft analyzer in jaanalyzertest index
```
$ cat sample1.txt
吾輩は猫である

$ azure-search-ta.py -c ./search.conf -i jaanalyzertest -a ja.microsoft --t sample1.txt -o simple
'吾輩' '猫' 'ある'
```






