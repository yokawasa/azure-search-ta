#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
if sys.version_info[0] == 3:
    import http.client as httplib
    import urllib.request, urllib.parse, urllib.error
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from io import StringIO
else:
    import httplib
    from urllib import urlopen
    from urlparse import urlparse
    from io import open
    from StringIO import StringIO
import simplejson as json
from bs4 import BeautifulSoup, NavigableString, Declaration, Comment

### Global Defines
_AZURE_SEARCH_TEXT_ANALYZE_VERSION = '0.3.0'
_AZURE_SEARCH_API_VERSION = '2017-11-11'
_AZURE_SEARCH_CONFIG_FILE = 'search.conf'

def print_out(s):
    #print (type(outs))
    if sys.version_info[0] == 3:
        sys.stdout.buffer.write(u"{}\n".format(s).encode('utf-8'))
    else:
        print(s.encode('utf-8'))

def print_err(s):
    sys.stderr.write(u"[ERROR] {}\n".format(s))

def print_quit(s):
    print(s)
    quit()

def format_join(l,f):
    o = u''
    n = 0
    for i in l:
        if n==0:
            o = o + f.format(i)
        else:
            o = o + u' '
            o = o + f.format(i)
        n += 1
    return o

def is_URL(s):
    o = urlparse(s)
    if len(o.scheme) > 0:
        return True
    return False

def read_config(s):
    config = {}
    f = open(s)
    line = f.readline().strip()
    while line:
        #print line
        line = f.readline().strip()
        # skip if line start from sharp
        if line[0:1] == '#':
            continue
        arrs=line.split('=')
        if len(arrs) != 2:
            continue
        config[arrs[0]] = arrs[1]
    f.close
    return config

class WebScraper:
    def __init__(self, url):
        res = urlopen(url)
        self.__content = res.read().decode('utf-8')

    def __get_navigable_strings(self,soup):
        if isinstance(soup, NavigableString):
            if type(soup) not in (Comment, Declaration) and soup.strip():
                yield soup
        elif soup.name not in ('script', 'style'):
            for c in soup.contents:
                for g in self.__get_navigable_strings(c):
                    yield g
    
    def __get_Html_tag_stripped_text(self,s):
        soup = BeautifulSoup(s, "html.parser")
        return ' '.join(self.__get_navigable_strings(soup))

    def get_content(self):
        return self.__content

    def get_html_stripped_content(self):
        return self.__get_Html_tag_stripped_text(self.__content)


class AzureSearchClient:
    def __init__(self, api_url, api_key):
        self.__api_url=api_url
        self.__api_key=api_key
        self.headers={
            'Content-Type': "application/json; charset=UTF-8",
            'Api-Key': self.__api_key,
            'Accept': "application/json", 'Accept-Charset':"UTF-8"
        }

    def textanalyze(self,index_name, analyzer, text):
        # Create JSON string for request body
        reqobject={}
        reqobject['text'] = text
        reqobject['analyzer'] = analyzer
        io=StringIO()
        json.dump(reqobject, io)
        req_body = io.getvalue()
        # HTTP request to Azure search REST API
        conn = httplib.HTTPSConnection(self.__api_url)
        conn.request("POST",
                u"/indexes/{0}/analyze?api-version={1}".format(index_name, _AZURE_SEARCH_API_VERSION),
                req_body, self.headers)
        response = conn.getresponse()
        #print "status:", response.status, response.reason
        data = (response.read()).decode('utf-8')
        #print("data:{}".format(data))
        conn.close()
        return data 


def main():
    parser = argparse.ArgumentParser(description='This program do text analysis and generate formatted output by using Azure Search Text Analyze API')
    parser.add_argument(
        '-v','--version', action='version', version=_AZURE_SEARCH_TEXT_ANALYZE_VERSION)
    parser.add_argument(
        '-c','--conf', default=_AZURE_SEARCH_CONFIG_FILE,
        help='Azure Search Configuration file. Default:search.conf')
    parser.add_argument(
        '-i','--index',
        help='Azure Search index name')
    parser.add_argument(
        '-a','--analyzer',
        help='Azure Search analyzer name')
    parser.add_argument(
        '-t','--text',
        help='A file path or HTTP(s) URL from which the command line reads the text to analyze')
    parser.add_argument(
        '-o','--output', default='normal',
        help='Output format ("simple" or "normal"). Default:normal')
    args = parser.parse_args()

    ### Args Validation
    if not os.path.exists(args.conf):
        print_err(u"Azure Search config file doesn't exist: {0}\n"
                  u"Please speicify the file with --conf option\n".format(args.conf))
        print_quit(parser.parse_args(['-h']))
    if not args.index: 
        print_err(u"Please specify index name with --index option!\n")
        print_quit(parser.parse_args(['-h']))
    if not args.analyzer: 
        print_err(u"Please specify analyzer name with --analyzer option!\n")
        print_quit(parser.parse_args(['-h']))
    if not args.text: 
        print_err(u"Please specify text file with --text option!\n")
        print_quit(parser.parse_args(['-h']))
    if not is_URL(args.text) and not os.path.exists(args.text):
        print_err(u"Please speicfiy either URL or text file path that really does exist for --text option value!: {}\n".format(args.text))
    if args.output !="simple" and args.output !="normal":
        print_err(u"Please specify either \"simple\" or \"normal\" for --output option value!\n")

    ## Read from URL
    target_text = u''
    if (is_URL(args.text)):
        ## Read from URL
        ws = WebScraper(args.text)
        target_text = ws.get_html_stripped_content()
    else: 
        ## Read from file
        so = u''
        with open(args.text, encoding='utf-8') as f:  
            lines = f.readlines()
            for l in lines:
                l = l.strip()
                if len(l) > 1 and not l.isspace():
                    so = so + l
        target_text = so
 
    ### do Azure Search operations
    c = read_config(args.conf)
    client=AzureSearchClient(
        u"{0}.search.windows.net".format(c["SEARCH_SERVICE_NAME"]),
        c["SEARCH_API_KEY"])
    resstr = client.textanalyze(args.index, args.analyzer, target_text)

    tokens=[]
    resobj=json.loads(resstr)
    if "error" in resobj:
        errobj=resobj['error']
        if "message" in errobj:
            print_quit(u"[ERROR] {}\n".format(errobj['message']))
        else:
            print_quit(u"[ERROR] Unknown error occured\n")
    tokenobjs = resobj['tokens']
    for tokenobj in tokenobjs:
        tokens.append(tokenobj['token'])
   
    ### print TOKENS with specified output format
    outs = u''
    if (args.output == 'simple'):
        outs = outs + format_join(tokens, u"'{}'" )
    else:
        outs = outs + u'INPUT: '
        outs = outs + target_text
        outs = outs + u'\n'
        outs = outs + u'TOKENS: '
        outs = outs + format_join(tokens, u"[{}]" )

    print_out(outs)
