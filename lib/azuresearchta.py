#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import httplib
import urllib
import simplejson as json
from StringIO import StringIO
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, NavigableString, Declaration, Comment

### Global Defines
_AZURE_SEARCH_TEXT_ANALYZE_VERSION = '0.1.0'
_AZURE_SEARCH_API_VERSION = '2015-02-28-Preview'
_AZURE_SEARCH_CONFIG_FILE = 'search.conf'

def print_err(s):
    sys.stderr.write("[ERROR] {}\n".format(s))

def print_quit(s):
    print s
    quit()

def format_join(l,f):
    o = StringIO()
    n = 0
    for i in l:
        if n==0:
            o.write(f.format(i))
        else:
            o.write(' ')
            o.write(f.format(i) )
        n += 1
    return o.getvalue()

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
        res = urllib.urlopen(url)
        self.__content = res.read()

    def __get_navigable_strings(self,soup):
        if isinstance(soup, NavigableString):
            if type(soup) not in (Comment, Declaration) and soup.strip():
                yield soup
        elif soup.name not in ('script', 'style'):
            for c in soup.contents:
                for g in self.__get_navigable_strings(c):
                    yield g
    
    def __get_Html_tag_stripped_text(self,s):
        soup = BeautifulSoup(s, convertEntities="html")
        return ' '.join(self.__get_navigable_strings(soup))

    def get_content(self):
        return self.__content.encode('utf8')

    def get_html_stripped_content(self):
        return self.__get_Html_tag_stripped_text(self.__content).encode('utf8')


class AzureSearchClient:
    def __init__(self, api_url, api_key):
        self.__api_url=api_url
        self.__api_key=api_key
        self.headers={
            'Content-Type': "application/json; charset=UTF-8",
            'Api-Key': self.__api_key,
            'Accept': "application/json", 'Accept-Charset':"UTF-8"
        }

    def textanalze(self,index_name, analyzer, text):
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
                "/indexes/{0}/analyze?api-version={1}".format(index_name, _AZURE_SEARCH_API_VERSION),
                req_body, self.headers)
        response = conn.getresponse()
        #print "status:", response.status, response.reason
        data = response.read()
        #print "data:", data
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
        print_err("Azure Search config file doesn't exist: {0}\n"
                  "Please speicify the file with --conf option\n".format(args.conf))
        print_quit(parser.parse_args(['-h']))
    if not args.index: 
        print_err("Please specify index name with --index option!\n")
        print_quit(parser.parse_args(['-h']))
    if not args.analyzer: 
        print_err("Please specify analyzer name with --analyzer option!\n")
        print_quit(parser.parse_args(['-h']))
    if not args.text: 
        print_err("Please specify text file with --text option!\n")
        print_quit(parser.parse_args(['-h']))
    if not is_URL(args.text) and not os.path.exists(args.text):
        print_err("Please speicfiy either URL or text file path that really does exist for --text option value!: {}\n".format(args.text))
    if args.output !="simple" and args.output !="normal":
        print_err("Please specify either \"simple\" or \"normal\" for --output option value!\n")

    ### Read text into String Buffer
    ## Read from URL
    target_text = StringIO()
    if (is_URL(args.text)):
        ## Read from URL
        ws = WebScraper(args.text)
        target_text = ws.get_html_stripped_content()
    else: 
        ## Read from file
        f = open(args.text)
        sio = StringIO()
        l = f.readline()
        while l:
            l = l.strip()
            if len(l) > 1 and not l.isspace():
                sio.write(l)
            l = f.readline()
        f.close
        target_text=sio.getvalue()
  
    ### do Azure Search operations
    c = read_config(args.conf)
    client=AzureSearchClient(
        "{0}.search.windows.net".format(c["SEARCH_SERVICE_NAME"]),
        c["SEARCH_API_KEY"])
    resstr = client.textanalze(args.index, args.analyzer, target_text)

    tokens=[]
    resobj=json.loads(resstr)
    tokenobjs = resobj['tokens']
    for tokenobj in tokenobjs:
        tokens.append(tokenobj['token'].encode('utf8'))
   
    ### print TOKENS with specified output format
    outs = StringIO()
    if (args.output == 'simple'):
        outs.write( format_join(tokens, "'{}'" ) ) 
    else:
        outs.write('INPUT: ')
        outs.write(target_text)
        outs.write('\n')
        outs.write('TOKENS: ')
        outs.write( format_join(tokens, "[{}]" ) ) 
       
    print outs.getvalue()
