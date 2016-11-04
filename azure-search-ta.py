#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import httplib
import simplejson as json
from StringIO import StringIO

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

if __name__ == '__main__':
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
        '-t','--textfile',
        help='Text file to read and analyze')
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
    if not args.textfile: 
        print_err("Please specify text file with --textfile option!\n")
        print_quit(parser.parse_args(['-h']))
    if not os.path.exists(args.textfile):
        print_err("text file {} does not exist\n".format(args.textfile))
        print_quit(parser.parse_args(['-h']))
    if args.output !="simple" and args.output !="normal":
        print_err("Please specify either \"simple\" or \"normal\" for --output option value!\n")
        print_quit(parser.parse_args(['-h']))
    ### Read text file into String Buffer
    f = open(args.textfile)
    target_text = StringIO()
    l = f.readline()
    while l:
        l = l.strip()
        if len(l) > 1 and not l.isspace():
            target_text.write(l)
        l = f.readline()
    f.close

    c = read_config(args.conf)
    client=AzureSearchClient(
        "{0}.search.windows.net".format(c["SEARCH_SERVICE_NAME"]),
        c["SEARCH_API_KEY"])
    resstr = client.textanalze(args.index, args.analyzer, target_text.getvalue())

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
        outs.write(target_text.getvalue())
        outs.write('\n')
        outs.write('TOKENS: ')
        outs.write( format_join(tokens, "[{}]" ) ) 
       
    print outs.getvalue()
