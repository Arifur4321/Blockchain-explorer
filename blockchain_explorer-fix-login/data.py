# -*- coding: utf-8 -*-

# MultiChain Explorer 2 (c) Coin Sciences Ltd
# All rights reserved under BSD 3-clause license

from datetime import datetime
from doctest import script_from_examples
from time import gmtime, strftime
from itertools import chain
from tkinter import *
from tkcalendar import Calendar
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as soup
import pprint
import pandas as pd
from tabulate import tabulate
import cfg
from urllib import parse
import json
from collections import OrderedDict
#from cgi import escape
from html import escape
from datetime import datetime
import webbrowser
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTableView, QHeaderView, QVBoxLayout
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from reportlab.lib import colors  
from reportlab.lib.pagesizes import letter, inch  
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle   


from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import requests
from dash import Dash, dash_table
from dash.dependencies import Input, Output

import dashboard


NAV_SYMBOL_FIRST='&laquo;'
NAV_SYMBOL_PREV='&lt;'
NAV_SYMBOL_NEXT='&gt;'
NAV_SYMBOL_LAST='&raquo;'

DEFAULT_NONAV_COUNT=5
DEFAULT_PAGE_SHIFT=3
DEFAULT_NATIVE_CURRENCY_ID='0-0-0'
DEFAULT_COUNTS=[20,50,100,200,500]
MAX_SHOWN_DATA=40
MAX_DEFAULT_QTY=9223372036854775807
PERMISSION_TEMPLATES={
            "admin"    : {"display-name":"admin"},
            "activate" : {"display-name":"activate"},
            "mine"     : {"display-name":"mine"},
            "issue"    : {"display-name":"issue"},
            "create"   : {"display-name":"create"},
            "send"     : {"display-name":"send"},
            "receive"  : {"display-name":"receive"},
            "write"    : {"display-name":"write"},
            "read"     : {"display-name":"read"},
            "connect"  : {"display-name":"connect"},
            "low1"     : {"display-name":"low1"},
            "low2"     : {"display-name":"low2"},
            "low3"     : {"display-name":"low3"},
            "high1"    : {"display-name":"high1"},
            "high2"    : {"display-name":"high2"},
            "high3"    : {"display-name":"high3"},
        }       

ALLOWED_PERMISSIONS_GLOBAL=["admin","activate","mine","issue","create","send","receive","low1","low2","low3","high1","high2","high3"]
ALLOWED_PERMISSIONS_ASSET=["admin","activate","issue","send","receive"]
ALLOWED_PERMISSIONS_STREAM=["admin","activate","write","read"]
ALLOWED_PERMISSIONS_VARIABLE=["admin","activate","write"]
ALLOWED_PERMISSIONS_LIBRARY=["admin","activate","write"]
SHOW_PERMISSION_ONLY_IF_PRESENT=["low1","low2","low3","high1","high2","high3"]
        
TAG_TO_LABEL_TEXT={
            "pay-to-script-hash" : "P2SH Address",
            "not-p2pkh-p2sh" : "Unusual Address",
            "coinbase" : "Coinbase",
            "grant-high" : "Grant Permission (high)",
            "revoke-high" : "Revoke Permission (high)",
            "grant-low" : "Grant Permission",
            "revoke-low" : "Revoke Permission",
            "grant-per-entity" : "Grant Per-Entity",
            "revoke-per-entity" : "Revoke Per-Entity",
            "issue-license-unit" : "New License Token",
            "issue-asset-units" : "Issue Asset",
            "transfer-license" : "Transfer License",
            "transfer-asset" : "Transfer Asset",
            "transfer-native" : "Native Transfer",
            "license" : "License Token",
            "asset" : "Asset",
            "native" : "Native",
            "multiple-assets" : "2+ Assets",
            "combine-utxos" : "Combine",
            "issuemore-asset-units" : "Issue More",
            "issue-asset-details" : "Issue Asset (Metadata)",
            "create-stream" : "Create Stream",
            "create-pseudo-stream" : "",
            "create-upgrade" : "Create Upgrade",
            "create-filter" : "Create Filter",
            "create-license" : "Create License",
            "create-variable" : "Create Variable",
            "create-library" : "Create Library",
            "issuemore-asset-details" : "Issue Asset Follow-On (Metadata)",
            "update-asset" : "Update Asset",
            "update-variable" : "Update Variable",
            "update-library" : "Update Library",
            "approve-filter-library" : "Approve Filter Or Library",
            "approve-upgrade" : "Approve Upgrade",
            "inline-data" : "Inline Metadata",
            
            "offchain-stream-item" : "Offchain Item",
            "onchain-stream-item" : "Onchain Item",
            "multiple-stream-items" : "2+ Stream Items",
            "inline-data" : "Inline Data",
            "raw-data" : "Raw Metadata",
            "unspendable" : "",
        }

TAG_TO_LABEL_TYPE={
            "coinbase" : "default",
            "not-p2pkh-p2sh" : "warning",
            "permission-admin-mine" : "warning",
            "approve-filter-library" :  "warning",       
            "approve-upgrade" :  "warning",       
        }

TAG_REMOVE_IF_OTHER_PRESENT={"grant-low":"grant-high",
                             "revoke-low":"revoke-high",
                             "issue-asset-details":"issue-asset-units",
                             "issuemore-asset-details":"issuemore-asset-units",
                             "transfer-asset":"multiple-assets",
                             "issue-license-unit":"create-license"}

def decode_script(script):
    
    tokens=[]
    for t in script.split(' '):
        if (len(t) > 3) and (t[0:3] == 'OP_'):
            tokens.append(t[3:])
        else:
            if (len(t) % 2) != 0:
                tokens.append(t)
            else:                 
                token=str(len(t) // 2) + ':'
                if len(t)<= 8:
                    token += t
                else:
                    token += t[0:4] + '...' + t[-4:]
                tokens.append(token)
    
    return ' '.join(tokens)

def format_time(nTime):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(nTime)))

def signed_amount_html(amount):
    if amount<0:
        return str(amount)
    if amount>0:
        return '+' + str(amount)
    return '0'        
    
def range_title(start,size,min_start,items_name):
    return "(" + items_name + str(start + size - 1 + min_start)+ '...'+str(start + min_start) + ")"
#    return str(start + min_start) + ' - ' + str(start + size - 1 + min_start)

def nav_bar(base_url,nparams,items_name="", downloadlink=None, downloadsummary=None , searchboxmain = None  ):

    all_pages=[]
    
    all_pages.append(0)    
    all_pages.append(nparams['thispage']-1)
    all_pages.append(0)    
    last_page=0
    for this_page in range((nparams['thispage']-DEFAULT_PAGE_SHIFT),(nparams['thispage']+DEFAULT_PAGE_SHIFT)+1):
        if (this_page >= 0) and (this_page < nparams['totalpages']):
            if this_page > last_page:
                if this_page > last_page+1:
                    all_pages.append(None)    
                all_pages.append(this_page)    
                last_page=this_page
    this_page=nparams['totalpages'] - 1
    if this_page > last_page:
        if this_page > last_page+1:
            all_pages.append(None)    
        all_pages.append(this_page)    
        last_page=this_page
    all_pages.append(nparams['thispage']+1)
    all_pages.append(nparams['totalpages'] - 1)
    
    pages=all_pages.copy()
    if not nparams['forward']:
        pages=list(reversed(all_pages))
        
    bar='<div class="navbar">'
    bar+='<span class="navbar-pages">'
    bar+='<span class="navbar-caption">Page: </span>&nbsp;'
    top_item=0
    
    count=0
    for this_page in pages:      
        has_link=False
        title=''
        body='...'
        selected=False
        skip=False
        if this_page is not None:
            start=this_page*nparams['pagesize']
            size=nparams['pagesize']
            if this_page == nparams['totalpages'] - 1:
                size=nparams['lastpagesize']
            
            min_item=start+nparams['minstart']
            max_item=min_item+size-1
                
            min_max_title="(" + items_name
            if nparams['forward']:
                min_max_title += str(min_item) + "..." + str(max_item)
            else:
                min_max_title += str(max_item) + "..." + str(min_item)
            min_max_title+=")"
    
            if count == 0:
                body=NAV_SYMBOL_FIRST#'&laquo;'
                has_link=True
                start=None
                title='First page ' + min_max_title
                skip=True
            elif count == 1:
                body=NAV_SYMBOL_PREV#'&lt;'
                if (this_page >= 0) and (this_page < nparams['totalpages']):
                    has_link=True
                    title='Previous page ' + min_max_title
            elif count == len(pages)-2:                    
                body=NAV_SYMBOL_NEXT#'&gt;'
                if (this_page >= 0) and (this_page < nparams['totalpages']):
                    has_link=True
                    title='Next page ' + min_max_title
            elif count == len(pages)-1:                    
                body=NAV_SYMBOL_LAST#'&raquo;'
                has_link=True
                title='Last page ' + min_max_title
                skip=True
            elif this_page == nparams['thispage']:
                body=str(this_page+1)
                top_item=start
                if not nparams['forward']:
                    body=str(nparams['totalpages']-this_page)                    
                    top_item=start+size-1
                has_link=False
                title='Page '+ body + ' ' + min_max_title
                selected=True
            else:
                body=str(this_page+1)
                if not nparams['forward']:
                    body=str(nparams['totalpages']-this_page)
                has_link=True
                title='Go to page '+ body + ' ' + min_max_title
        if skip:
            bar+=''
        elif has_link:
            link=base_url + '?size=' + str(nparams['pagesize']) 
            if start is not None:
                link += '&from=' + str(start)            
            bar+='<a class="navbar-link" href="' + link + '" title="' + title + '">'+body+'</a>&nbsp;'
        else:
            if selected:
                bar+='<a class="navbar-selected" title="' + title + '">'+body+'</a>&nbsp;'
            elif body=='...':
                bar+='<a class="navbar-ellipsis" title="' + title + '">'+body+'</a>&nbsp;'
            else:
                bar+='<a class="navbar-disabled" title="' + title + '">'+body+'</a>&nbsp;'
            
        count += 1
    
    bar+='</span>'
    bar+='&nbsp;&nbsp;'
    bar+='<span class="navbar-sizes">'
    bar+='<span class="navbar-caption">'+items_name.capitalize()+' per page: </span>&nbsp;'
                
    for ct in DEFAULT_COUNTS:
        title=str(ct) + ' ' + items_name + ' per page'
        body=str(ct)
        if ct == nparams['pagesize']:
            bar+='<a class="navbar-selected"' + '" title="' + str(ct) + " " + items_name + ' per page">'+str(ct)+'</a>&nbsp;'
        else:            
            link=base_url + '?size=' + str(ct) + '&from=' + str(top_item)
            bar+='<a class="navbar-link" href="' + link + '" title="' + title + '">'+body+'</a>&nbsp;'
    bar+='</span>'
    if downloadlink:
       bar+='<a href="'+  downloadlink +'" > <img  style="float:right; " src="PDF-ICON.png" alt="MultiChain logo" data-toggle="tooltip" data-placement="top" title="Generate PDF" />   </a>'
    if downloadsummary: 
        bar+='<a href="'+  downloadsummary +'" > <img  style="float:right; "  src="PDF-ICON.png" alt="MultiChain logo" data-toggle="tooltip" data-placement="top" title="Generate PDF" />   </a>'
    if searchboxmain:
        bar+='<a href="'+  searchboxmain +'" > <input type="text" placeholder="Search.." name="search2" style ="float:left">  <button type="submit" style ="float:left"><i class="fa fa-search"></i></button>    </a>'

    #<input type="text" placeholder="Search.." name="search2" style ="float:left">  <button type="submit" style ="float:left"><i class="fa fa-search"></i></button>
   
    bar+='</div>'
        
    return bar
    
def field_in_dict(obj,field_name,default_value):
    if field_name in obj:
        if obj[field_name] is not None:
            return obj[field_name]
    return default_value
    
def tags_to_labels(tags):
    labels=[]
    
    for tag in tags:
        take_it=True
        if tag not in TAG_TO_LABEL_TEXT:
            this_label_type='danger'
            labels.append((this_label_type,"Unknown MultiChain Command"))
            take_it=False
        else:
            if len(TAG_TO_LABEL_TEXT[tag]) == 0:
                take_it=False
                
        if tag in TAG_REMOVE_IF_OTHER_PRESENT:
            if TAG_REMOVE_IF_OTHER_PRESENT[tag] in tags:
                take_it=False
                
        this_label_type='info'
        if take_it:
            this_label=TAG_TO_LABEL_TEXT[tag]
            if len(this_label) > 0:
                if tag in TAG_TO_LABEL_TYPE:
                    this_label_type = TAG_TO_LABEL_TYPE[tag]
                labels.append((tag,this_label))
            
    return labels
    
def tags_to_label_html(tags):
    labels=tags_to_labels(tags)
    label_html=''
    
    if len(labels)>0:
        label_html += '<div>'
        for label in labels:
#            label_html += '<span class="tag">' + label[1] + '</span>&nbsp;'
            label_html += '<span class="tag tag-' + label[0] + '">' + label[1] + '</span>&nbsp;'
#            label_html += '<span class="label label-info">' + label[1] + '</span>&nbsp;'
        label_html += '</div>'
        
    return label_html
    
class MCEDataHandler():

    allresult = None 
    alldetails = None
    detailresult = None  
    display_local=False  
    def standard_response(self,data):
        return (200, [("Content-type", "text/html")], bytes(data,"utf-8"))

    def error_response(self,response):        
        if ('connection-error' in response) and response['connection-error']:
            return self.standard_response('<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
        else:
            return self.standard_response('<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
            
    def chain_native_flag(self,chain,getchaintotals_response):
        if ('native-flag' in chain.config) and (chain.config['native-flag'] is not None):
            return chain.config['native-flag']
            
        response=None
        if getchaintotals_response is not None:
            response=getchaintotals_response.copy()
            
        if response is None:
            response=chain.request("getchaintotals",[])
            if (response['result'] is None) or ('assets' not in response['result']):
                if not ( ('connection-error' in response) and response['connection-error'] ):
                    response=chain.request("getinfo",[])
            
        if response['result'] is not None:
            if 'rewards' in response['result']:
                if response['result']['rewards'] > 0:
                    chain.config['native-flag']=True
                else:
                    chain.config['native-flag']=False
            return chain.config['native-flag']
            
        return False            
    
    def chain_native_units(self,chain):
        if ('native-units' in chain.config) and (chain.config['native-units'] is not None):
            return chain.config['native-units']
            
        response=chain.request("getblockchainparams",[])            
        if (response['result'] is not None) and ("native-currency-multiple" in response['result']) and (response['result']["native-currency-multiple"] > 0):
            chain.config['native-units'] = 1 / response['result']["native-currency-multiple"]
            return chain.config['native-units']

        return None                

    def printFilter():
        pass 
                
    def handle_chains(self,chain,params,nparams):
        response=cfg.chains[0].request("getinfo",[])
        transazioni = field_in_dict(response['result'],'transactions','0')
        blocks = response['result']['blocks']

        if response['result'] is not None:
            #native_flag=self.chain_native_flag(cfg.chains[0],response)
            assets=field_in_dict(response['result'],'assets','0') 
            #native_text='' 
            #if assets !=  '?':
            #    if native_flag:
            #        assets=str(assets+1) 
            #        native_text=' (includes native currency)'

        #script,div, js_resources, css_resources , top,blocks,transazioni,assets
        script,div, js_resources, css_resources, html= dashboard.homePageGraph(width=750,height=350, blocks=blocks,transazioni=transazioni,assets=assets)

        #<object style="margin:0 auto;text-align:center" type="text/html" width="850px" height="400px" style="overflow:auto; data={html}">
        #</object>
        #<iframe src="dashboard.html" width="850px" height="400px">
        #    
        #    </iframe>
        # <div id="columnchart_values" style="width: 900px; height: 300px;"></div>
        body = f'''
            <table class="table table-striped">
            <tr>
            <th>Stato</th>
            <th>Nome Nodo</th>
            <th>Numero Transazioni</th>
            <th>Transazioni</th>
            <th>Dettaglio Transazioni</th>
            <th>Data</th>
            <th>Indirizzo</th>
            </tr>
            '''
        
        for chain in cfg.chains:
            body += '<tr>'
            response=chain.request("getchaintotals",[])
            if (response['result'] is None) or ('assets' not in response['result']):
                if not ( ('connection-error' in response) and response['connection-error'] ):
                    response=chain.request("getinfo",[])
                
            body += '<td>'
            if response['result'] is not None:
                body += '<span class="label label-success">Connected</span>'
            else:
                body += '<span class="label label-danger">No Connection</span>'
            body += '</td>'
            body += '<td><a href="' + chain.config['path-name'] +  '/chain">' + chain.config['name'] + '</a></td>'
            if response['result'] is not None:
                native_flag=self.chain_native_flag(chain,response)
                assets=field_in_dict(response['result'],'assets','?') 
                native_text='' 
                if assets !=  '?':
                    if native_flag:
                        assets=str(assets+1) 
                        native_text=' (includes native currency)'

                body += '<td><a href="' + chain.config['path-name'] + '/blocks">' + str(response['result']['blocks']) +  '</a></td>'
                body += '<td><a href="' + chain.config['path-name'] + '/transactions">' + str(field_in_dict(response['result'],'transactions','?')) +  '</a></td>'
                body += '<td><a href="' + chain.config['path-name'] + '/assets">' + str(assets) +  '</a>'+native_text+'</td>'
                body += '<td><a href="' + chain.config['path-name'] + '/streams">' + str(field_in_dict(response['result'],'streams','?')) +  '</a></td>'
                body += '<td><a href="' + chain.config['path-name'] + '/addresses">' + str(field_in_dict(response['result'],'addresses','?')) +  '</a></td>'
            else:
                body += '<td></td><td></td><td></td><td></td><td></td>'
                
            body += '</tr>'

        body+='</table>'
        body+=script

        return self.standard_response(body)

    

    def handle_chainsummary(self,chain,params,nparams):
        body = '<h3>Summary</h3>'
        if chain is None:        
            return self.standard_response(body + '<div class="alert alert-danger" role="alert">Chain not found</div>')
            
        response=chain.request("getchaintotals",[])
        if (response['result'] is None) or ('assets' not in response['result']):
            if not ( ('connection-error' in response) and response['connection-error'] ):
                response=chain.request("getinfo",[])
            
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response(body + '<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response(body + '<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
                
        native_flag=self.chain_native_flag(chain,response)
        assets=field_in_dict(response['result'],'assets','?') 
        native_text=''
        if assets !=  '?':
            if native_flag:
                assets=str(assets + 1)
                native_text=' (includes native currency)'
                
        chain_rewards=0
        if 'rewards' in response['result']:
            chain_rewards=response['result']['rewards']            
        
        body += '<table class="table table-bordered table-striped table-condensed">'
        body += '<tr><td>Blocks</td><td><a href="' + chain.config['path-name'] + '/blocks">' + str(response['result']['blocks']) +  '</a>'+' <a href="' + chain.config['path-name'] + '/miners">(view miners)</a></td></tr>'
        tx_count=field_in_dict(response['result'],'transactions','?')
        if tx_count == '?':
            body += '<tr><td>Transactions</td><td>' + str(tx_count) +  '</td></tr>'
        else:
            body += '<tr><td>Transactions</td><td><a href="' + chain.config['path-name'] + '/transactions">' + str(field_in_dict(response['result'],'transactions','?')) +  '</a></td></tr>'
        body += '<tr><td>Assets </td><td><a href="' + chain.config['path-name'] + '/assets">' + str(assets) +  '</a>'+native_text+'</td></tr>'
        body += '<tr><td>Streams</td><td><a href="' + chain.config['path-name'] + '/streams">' + str(field_in_dict(response['result'],'streams','?')) +  '</a></td></tr>'
        address_count=field_in_dict(response['result'],'addresses','?')
        if address_count == '?':
            body += '<tr><td>Addresses</td><td>' + str(address_count) + ' <a href="' + chain.config['path-name'] + '/globalpermissions">(view permissions)</a></td></tr>'
        else:
            body += '<tr><td>Addresses</td><td><a href="' + chain.config['path-name'] + '/addresses">' + str(address_count) +  '</a>'+' <a href="' + chain.config['path-name'] + '/globalpermissions">(view permissions)</a></td></tr>'
        if chain_rewards > 0:        
            body += '<tr><td>Native Currency</td><td>' + str(chain_rewards) +  ' units <a href="' + chain.config['path-name'] + '/assetholders/'+DEFAULT_NATIVE_CURRENCY_ID+'">(view holders)</a></td></tr>'
            
        body += '</table>'
        
#        body += '<h3>Node</h3>'
#        body += '<table class="table table-bordered table-striped table-condensed">'
#        body += '<tr><td>Local Addresses</td><td><a href="' + chain.config['path-name'] + '/localaddresses">' + '?' +  '</a></td></tr>'
#        body += '<tr><td>Peers</td><td><a href="' + chain.config['path-name'] + '/peers">' + str(field_in_dict(response['result'],'peers','?')) +  '</a></td></tr>'
#        body += '</table>'
        
        body += '<h3>General Information</h3>'
        body += '<table class="table table-bordered table-striped table-condensed">'
        for key,value in sorted(response['result'].items()):
            if key in ('relayfee'):
                value = ('%.20f' % value).rstrip('0') 
            if key != 'rewards':
                body +=  '<tr><td>' + key + '</td><td>' + str(value) + '</td></tr>'
            
        body += '</table>'

        return self.standard_response(body)
        
    def handle_chainparameters(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
            
        response=chain.request("getblockchainparams",[])
        if response['result'] is None:
            return self.standard_response('')
                
            
        body = '<h3>Blockchain Parameters</h3>'
        body += '<table class="table table-bordered table-striped table-condensed">'
        td='<td style="word-wrap: break-word;min-width: 50px;max-width: 300px;white-space:normal;">'
        for key,value in sorted(response['result'].items()):
            body += '<tr>'+ td + str(key) + '</td>'+ td + str(value) + '</td></tr>'
            
        body += '</table>'
        
        return self.standard_response(body)

    def expand_params(self,nparams,list_size=-1,forward=False,min_start=1):
        
        if list_size<=0:
            return
            
        nparams['nav']=True
        if 'onlylast' in nparams:
            if int(nparams['onlylast']) > 0:
                nparams['nav']=False
                if 'count' not in nparams:
                    nparams['count']=DEFAULT_NONAV_COUNT 
                else:
                    nparams['count']=int(nparams['count'])
        else:
            if ('size' not in nparams) or (int(nparams['size']) <= 0):
                nparams['count']=DEFAULT_COUNTS[0]     
            else:
                nparams['count']=int(nparams['size'])
                
                
        nparams['pagesize']=nparams['count']      
        nparams['listsize']=list_size
        nparams['minstart']=min_start
        nparams['forward']=forward
        nparams['totalpages']=(list_size-1) // nparams['pagesize'] + 1
        nparams['lastpagesize']=list_size-(nparams['totalpages']-1)*nparams['pagesize']
        if not forward and (nparams['totalpages'] > 1) and (nparams['lastpagesize'] != nparams['pagesize']):
            nparams['lastpagesize'] += nparams['pagesize']
            nparams['totalpages'] -= 1
                    
        if nparams['nav']:        
            if 'from' not in nparams:
                if forward:
                    nparams['start']=0
                else:
                    nparams['start']=(nparams['totalpages']-1)*nparams['pagesize']
                    if nparams['lastpagesize'] > nparams['pagesize']:
                        nparams['count'] += nparams['pagesize']
                nparams['thispage']=nparams['start'] // nparams['pagesize']               
            else:
                nparams['start']=int(nparams['from'])            
                nparams['thispage']=nparams['start'] // nparams['pagesize']               
                if nparams['lastpagesize'] > nparams['pagesize']:
                    if nparams['thispage'] >= nparams['totalpages']:
                        nparams['thispage']=nparams['totalpages']-1 
                        nparams['count'] += nparams['pagesize']
                nparams['start']=nparams['thispage']*nparams['pagesize']
        else:
            nparams['start']=-nparams['count']
                        
    def handle_blocks(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')

        block_count=chain.request("getblockcount",[])
        if block_count['result'] is None:
            return self.standard_response('')
        last=block_count['result']+1
        
        self.expand_params(nparams,last,False,0)
        response=chain.request("listblocks",[str(nparams['start']) + '-' + str(nparams['start'] + nparams['count'] -1)])
            
        if response['result'] is None:
            return self.error_response(response)
        
        body=nav_bar(chain.config['path-name'] + '/blocks',nparams,"blocks ")                
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Block</th>
            <th>Hash</th>
            <th>Miner</th>
            <th>Time</th>
            <th>Transactions</th>
            </tr>
            '''
            
        for block in reversed(response['result']):
            body += '<tr>'
            body += '<td><a href="' + chain.config['path-name'] + '/block/' + str(block['height']) + '">' + str(block['height']) + '</a></td>'                        
            body += '<td><a href="' + chain.config['path-name'] + '/block/' + str(block['height']) + '">' + str(block['hash']) + '</a></td>'
            body += '<td><a href="' + chain.config['path-name'] + '/address/' + str(block['miner']) + '">' + str(block['miner']) + '</a></td>'
            body += '<td>' + format_time(block['time']) + '</td>'
            body += '<td>' + str(block['txcount']) + '</td>'
            body += '</tr>'

        body+='</table>'
            
        return self.standard_response(body)
            
    def handle_addresses(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        entity_counts=chain.request("getchaintotals",[])            
        if entity_counts['result'] is None:
            return self.error_response(entity_counts)
        last=entity_counts['result']['addresses']
        
        if last is None:
            return self.standard_response('<div class="alert alert-danger" role="alert">Explorer APIs are not enabled. To enable them, please run "multichaind -explorersupport=1 -rescan"</div>')

            
        self.expand_params(nparams,last,True)
        
        response=chain.request("explorerlistaddresses",['*',True,nparams['count'],nparams['start']])
            
        if response['result'] is None:
            return self.error_response(response)
            
        body=nav_bar(chain.config['path-name'] + '/addresses',nparams,"addresses ")
        
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Address</th>
            <th>Transactions</th>
            <th>Confirmed</th>
            <th>Assets</th>
            <th>Streams</th>
            </tr>
            '''
            
        for address in response['result']:
            body += '<tr>'
            body += '<td><a href="' + chain.config['path-name'] + '/address/' + address['address'] + '">' + address['address'] + '</a></td>'                
            body += '<td><a href="' + chain.config['path-name'] + '/addresstransactions/' + address['address'] + '">'  +str(address['txs']) +'</a></td>'
            body += '<td>'  +str(address['confirmed']) +'</td>'
            body += '<td><a href="' + chain.config['path-name'] + '/addressassets/' + address['address'] + '">'  +str(address['assets']) +'</a></td>'
            body += '<td><a href="' + chain.config['path-name'] + '/addressstreams/' + address['address'] + '">'  +str(address['streams']) +'</a></td>'
            body += '</tr>'

        body+='</table>'
            
        return self.standard_response(body)
                        
    def handle_miners(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        response=chain.request("listminers")
            
        if response['result'] is None:
            return self.error_response(response)
            
        body = '''
            <table class="table table-striped">
            <tr>
            <th>Address</th>
            <th>Permitted</th>
            <th>Wait blocks</th>
            <th>Last Mined</th>
            <th>State</th>
            </tr>
            '''
#            <th>Local State</th>
            
        for miner in response['result']:
            body += '<tr>'
            body += '<td><a href="' + chain.config['path-name'] + '/address/' + miner['address'] + '">' + miner['address'] + '</a></td>'                
            if miner['permitted']:                
                body += '<td><span class="label label-success">Yes</span></td>'        
                if miner['diversitywaitblocks'] == 0:                
                    body += '<td><span class="label label-success">0</span></td>'        
                else:
                    body += '<td><span class="label label-warning">'+str(miner['diversitywaitblocks'])+'</span></td>'         
            else:
                body += '<td><span class="label label-warning">No</span></td>'                        
                body += '<td></td>'        
            if miner['lastmined'] is None:
                body += '<td></td>'        
            else:
                body += '<td>'+str(miner['lastmined'])+'</td>'        
            body += '<td>'+str(miner['chainstate'])+'</td>'        
            
#            if miner['islocal']:
#                body += '<td>'+str(miner['localstate'])+'</td>'        
#            else:
#                body += '<td><span class="label label-warning">Not Local</span></td>'                                        
            
            body += '</tr>'

        body+='</table>'
            
        return self.standard_response(body)
            
    def handle_transactions(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        entity_counts=chain.request("getchaintotals",[])            
        if entity_counts['result'] is None:
            return self.error_response(entity_counts)
        last=entity_counts['result']['transactions']
        
        if last is None:
            return self.standard_response('<div class="alert alert-danger" role="alert">Explorer APIs are not enabled. To enable them, please run "multichaind -explorersupport=1 -rescan"</div>')
            
        self.expand_params(nparams,last)
        
        response=chain.request("explorerlisttransactions",[True,nparams['count'],nparams['start']])
            
        if response['result'] is None:
            return self.error_response(response)
            
            
        body=nav_bar(chain.config['path-name'] + '/transactions',nparams,"transactions ")                
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Txid</th>
            <th>Type</th>
            <th>Time</th>
            <th>Block</th>
            </tr>
            '''
            
        for tx in reversed(response['result']):
            label_html=tags_to_label_html(tx['tags'])
            body += '<tr>'
            body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + tx['txid'] + '">' + tx['txid'] + '</a>'  + '</td>'                        
            body += '<td>' +  label_html + '</td>'                        
            if tx['blockheight'] is not None:                
                body += '<td>' + format_time(tx['blocktime']) + '</td>'                        
                body += '<td><a href="' + chain.config['path-name'] + '/block/' + str(tx['blockheight']) + '">' + str(tx['blockheight']) + '</a></td>'                        
            else:
                body += '<td></td><td></td>'
            body += '</tr>'
            
        body+='</table>'
            
        return self.standard_response(body)
        
    def handle_addresssummary(self,chain,params,nparams):
        body = '<h3>Summary</h3>'
        if chain is None:        
            return self.standard_response(body + '<div class="alert alert-danger" role="alert">Chain not found</div>')
            
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
            
        address=params[0]            
        
        response=chain.request("listpermissions",['*', address])
            
        if response['result'] is None:
            return self.error_response(response)
            
        allowed_permissions=ALLOWED_PERMISSIONS_GLOBAL.copy()
        
        permissions={}
        for p in allowed_permissions:
            permission_def=PERMISSION_TEMPLATES[p].copy()
            permission_def['value']=False
            permissions[p]=permission_def            

        for p in response['result']:
            if p['type'] in permissions:
                permissions[p['type']]['value']=True
                
        found_permissions=[]                        
        for p in allowed_permissions:
            if permissions[p]['value']:
                found_permissions.append(permissions[p]['display-name'])
            
        permission_string=', '.join(found_permissions)            
                        
        
        response=chain.request("explorerlistaddresses",[address,True])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response(body + '<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response(body + '<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
                
        info=response['result'][0]
        
        body += '<table class="table table-bordered table-striped table-condensed">'
            
        body += '<tr><td>Address</td><td>'+address+'</td></tr>'    
        body += '<tr><td>Permissions</td><td>'+permission_string+'</td></tr>'    
        body += '<tr><td>Transactions</td><td><a href="' + chain.config['path-name'] + '/addresstransactions/' + address + '">' + str(info['txs']) + '</a></td>'
        body += '<tr><td>Confirmed</td><td>'+str(info['confirmed'])+'</td></tr>'    
        body += '<tr><td>Assets</td><td><a href="' + chain.config['path-name'] + '/addressassets/' + address + '">' + str(info['assets']) + '</a></td>'
        body += '<tr><td>Streams</td><td><a href="' + chain.config['path-name'] + '/addressstreams/' + address + '">' + str(info['streams']) + '</a></td>'
        
        body += '</table>'

        return self.standard_response(body)
                
    def handle_addresspermissions(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')

        address=params[0]       

        response=chain.request("listpermissions",['*', address])
            
        if response['result'] is None:
            return self.error_response(response)
            
        allowed_permissions=ALLOWED_PERMISSIONS_GLOBAL.copy()
            
        permissions={}
        for p in allowed_permissions:
            permission_def=PERMISSION_TEMPLATES[p].copy()
            permission_def['value']=False
            permissions[p]=permission_def            

        for p in response['result']:
            if p['type'] in permissions:
                permissions[p['type']]['value']=True
                
        found_permissions=[]                        
        for p in allowed_permissions:
            if permissions[p]['value']:
                found_permissions.append(permissions[p]['display-name'])
            
        body=', '.join(found_permissions)            
            
        return self.standard_response(body)
            
    def handle_assetholdertransactions(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 2:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')


        entity_quoted=params[0]            
        entity_name=parse.unquote_plus(entity_quoted)
        if entity_quoted == DEFAULT_NATIVE_CURRENCY_ID:
            entity_name=""
        
        address=params[1]       
        
        tx_count=chain.request("explorerlistaddressassettransactions",[entity_name,address,"-"])
        if tx_count['result'] is None:
            return self.error_response(tx_count)
        last=tx_count['result']
                        
        if last<=0:
            return self.standard_response('<div class="empty-list">This address has not transacted this asset</div>')            
            
        self.expand_params(nparams,last)
        
        response=chain.request("explorerlistaddressassettransactions",[entity_name,address,True,nparams['count'],nparams['start']])
            
        if response['result'] is None:
            return self.error_response(response)
                        
        body = ''
        if nparams['nav']:
            body=nav_bar(chain.config['path-name'] + '/assetholdertransactions/' + entity_quoted + '/' + address,nparams,"transaction ")
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Txid</th>
            <th style="text-align:right">Change</th>
            <th style="text-align:right">Balance</th>
            <th>Time</th>
            <th>Block</th>
            </tr>
            '''
            
        for tx in reversed(response['result']):
            body += '<tr>'
            body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + tx['txid'] + '">' + tx['txid'] + '</a>'  + '</td>'                        
            body += '<td align="right">' + signed_amount_html(tx['amount']) + '</td>'                        
            body += '<td align="right">' + str(tx['balance']) + '</td>'                        
                
            if tx['blockheight'] is not None:                
                body += '<td>' + format_time(tx['blocktime']) + '</td>'                        
                body += '<td><a href="' + chain.config['path-name'] + '/block/' + str(tx['blockheight']) + '">' + str(tx['blockheight']) + '</a></td>'                        
            else:
                body += '<td></td><td></td>'
            body += '</tr>'
            
        body+='</table>'
            
        return self.standard_response(body)
        
    def handle_addresstransactions(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')

        address=params[0]       
            
        tx_count=chain.request("explorerlistaddresses",[address])
        if tx_count['result'] is None:
            return self.error_response(tx_count)
        last=tx_count['result'][0]['txs']
                        
        self.expand_params(nparams,last)
        
        response=chain.request("explorerlistaddresstransactions",[address,True,nparams['count'],nparams['start']])
        if response['result'] is None:
            return self.error_response(response)
                        
        body = ''
        if nparams['nav']:
            body=nav_bar(chain.config['path-name'] + '/addresstransactions/' + address,nparams,"transactions ")
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Txid</th>
            <th>Type</th>
            <th>Time</th>
            <th>Block</th>
            </tr>
            '''
            
        for tx in reversed(response['result']):
            label_html=tags_to_label_html(tx['tags'])
            body += '<tr>'
            body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + tx['txid'] + '">' + tx['txid'] + '</a>'  + '</td>'                        
            body += '<td>' +  label_html + '</td>'                        
            if tx['blockheight'] is not None:                
                body += '<td>' + format_time(tx['blocktime']) + '</td>'                        
                body += '<td><a href="' + chain.config['path-name'] + '/block/' + str(tx['blockheight']) + '">' + str(tx['blockheight']) + '</a></td>'                        
            else:
                body += '<td></td><td></td>'
            body += '</tr>'
            
        body+='</table>'
            
        return self.standard_response(body)
        
    def handle_blocktransactions(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')

        block=int(params[0])       
            
        tx_count=chain.request("explorerlistblocktransactions",[block,"-"])
        if tx_count['result'] is None:
            return self.error_response(tx_count)
        last=tx_count['result']
                        
        self.expand_params(nparams,last,True)
        
        response=chain.request("explorerlistblocktransactions",[block,True,nparams['count'],nparams['start']])
        if response['result'] is None:
            return self.error_response(response)
                        
        body = ''
        if nparams['nav']:
            body=nav_bar(chain.config['path-name'] + '/blocktransactions/' + params[0],nparams,"transactions ")
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Txid</th>
            <th>Type</th>
            </tr>
            '''
            
        for tx in response['result']:
            label_html=tags_to_label_html(tx['tags'])
            body += '<tr>'
            body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + tx['txid'] + '">' + tx['txid'] + '</a>'  + '</td>'                        
            body += '<td>' +  label_html + '</td>'                        
            body += '</tr>'
            
        body+='</table>'
            
        return self.standard_response(body)
        
    def handle_addressassets(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
            
        address=params[0]       
        
        asset_count=chain.request("explorerlistaddressassets",[address,"-"])
        if asset_count['result'] is None:
            return self.error_response(asset_count)
        last=asset_count['result']
        
        if last<=0:
            return self.standard_response('<div class="empty-list">This address has not transacted any assets</div>')            
            
        self.expand_params(nparams,last)
        
        response=chain.request("explorerlistaddressassets",[address,True,nparams['count'],nparams['start']])
            
        if response['result'] is None:
            return self.error_response(response)
                        
        body = ''
        if nparams['nav']:
            body+=nav_bar(chain.config['path-name'] + '/addressassets/' + address,nparams,"assets ")
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Asset</th>
            <th>Balance</th>
            </tr>
            '''
            
        for asset in reversed(response['result']):
            body += '<tr>'
            
            entity_quoted=asset['issuetxid'] 
            
            if ('name' in asset) and (asset['name'] is not None) and (len(asset['name']) > 0):                
                entity_quoted=parse.quote_plus(asset['name'])
                entity_name=asset['name']
            else:
                entity_name="with no name"
                
            asset_link="Native Currency"
            if entity_quoted is not None:
                asset_link='<a href="' + chain.config['path-name'] + '/asset/' + entity_quoted + '">' + entity_name + '</a>'
            
            body += '<td>'+asset_link+'</td>'    
            
            if entity_quoted is None:
               entity_quoted=DEFAULT_NATIVE_CURRENCY_ID 
               
            if entity_quoted is not None:
                body += '<td>'+str(asset['qty'])+' <a href="' + chain.config['path-name'] + '/assetholdertransactions/' + entity_quoted + '/' + address + '">(transactions)</a></td>'    
            else:
                body += '<td>'+str(asset['qty'])+'</td>'    
                
            body += '</tr>'
            
        body+='</table>'
            
        return self.standard_response(body)

    
  

            
    def handle_addressstreams(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
            
        address=params[0]       
        
        stream_count=chain.request("explorerlistaddressstreams",[address,"-"])
        if stream_count['result'] is None:
            return self.error_response(stream_count)
        last=stream_count['result']
        
        if last<=0:
            return self.standard_response('<div class="empty-list">This address has not published in any streams</div>')            
            
        self.expand_params(nparams,last)
        
        response=chain.request("explorerlistaddressstreams",[address,True,nparams['count'],nparams['start']])
            
        if response['result'] is None:
            return self.error_response(response)
                        
        body = ''
        if nparams['nav']:
            body+=nav_bar(chain.config['path-name'] + '/addressstreams/' + address,nparams,"streams ")
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Stream</th>
            <th>Items</th>
            <th>Confirmed</th>
            </tr>
            '''
            
        for stream in reversed(response['result']):
            body += '<tr>'
            
            entity_quoted=stream['createtxid'] 
            if ('name' in stream) and (len(stream['name']) > 0):                
                entity_quoted=parse.quote_plus(stream['name'])
                body += '<td><a href="' + chain.config['path-name'] + '/stream/' + entity_quoted + '">' + stream['name'] + '</a></td>'    
            else:  
                body += '<td><a href="' + chain.config['path-name'] + '/stream/' + entity_quoted + '">No name</a></td>'    

            if stream["items"] is not None:              
                body += '<td><a href="' + chain.config['path-name'] + '/publisheritems/' + entity_quoted + '/' + address + '">'+str(stream['items'])+'</a></td>'                
                body += '<td>'+str(stream['confirmed'])+'</td>'    
            else:
                body += '<td colspan="2">Not subscribed</td>'                
                
            body += '</tr>'
            
        body+='</table>'
            
        return self.standard_response(body)

    def search_form(self):
        #q = (self['params'].get('q') or [''])[0]
        print("search result :",cfg.data_handler.allresult)
       # searchresult = list[self.alldetails]
              
        return [
            '<p>Search by any name ,address, block number, or chain name: </p>'
            '<form class="form-inline" action="', 'search"><p>'
            '<div class="form-group">'
            '<input id="search1" type="text" name="q" size="64" value="" style="height: 32px; margin-right: 10px;"/>'
            '<button type="submit" class="btn" style="height: 32px; vertical-align: middle;">Search</button> </div></form>'
            ]

            




            
    

    def handle_assets(self,chain,params,nparams):

        print("handle asset is called now") 
        
        
        if chain is None:        
            return self.standard_response('')

        last=-1                    
        entity_counts=chain.request("getchaintotals",[])     
        if entity_counts['result'] is None:
            return self.error_response(entity_counts)
        if entity_counts['result'] is not None:
            last=entity_counts['result']['assets']
                 
        chain_rewards=0
        native_flag=self.chain_native_flag(chain,entity_counts)
        if native_flag:
            if 'rewards' in entity_counts['result']:
                chain_rewards=entity_counts['result']['rewards']            

        if (last<=0) and not native_flag:
            return self.standard_response('<div class="empty-list">No assets have been issued in this chain</div>')            
        
        self.expand_params(nparams,last,True)
        
        response=chain.request("listassets",['*', False,  nparams['count'], nparams['start']])

               
        if response['result'] is None:
            return self.error_response(response)
                    
        max_count=0
        for asset in response['result']:
            if 'issuecount' in asset:
                issue_count=asset['issuecount']
                if issue_count > max_count:
                    max_count=issue_count
            else:
                max_count=1000
                
        show_issuer=False
        if max_count < 100:
            response=chain.request("listassets",['*', True,  nparams['count'], nparams['start']])
            show_issuer=True
            
       # B = Button(text = "Generate PDF")
       # B.place(x = 50,y = 50)     
        
        body=nav_bar(chain.config['path-name'] + '/assets',nparams,"assets" , downloadlink = "downloadpdf"  )
        
        #body=nav_bar(chain.config['path-name'] + '/assets',nparams,"assets", searchboxmain = "searchboxmainsa"  )

        #keyword = input("Enter a search value: \n")
        #mylist= str (self.search_form())
        #mylist = [item[1:-1] for item in mylist]
        #body +=''' <input class="form-control" id="myInput" name="myInput" type="text" placeholder="Search..">   '''
        #body += ''' <br> '''
        
        #inputstyu=soup.find("input", {"name": "myInput"}).get("value")
        #print ( "search box value :" ,inputstyu)  

        body += '''
            <table class="table table-striped">
            <tr>
            <th>Nome Utente
            
            </th>
            '''
        
        body +='''<th>Data Transazione </th>'''

        if self.display_local:            
            body += '<th>Asset Transactions</th>'
            
        body += '''<th >Tipo Operazione effettuata 
        
                 </th>'''
        if max_count>0:
            body += '<th>Descrizione</th>'            
            
        body += '''
            <th>Stato </th>
            
            '''
        if show_issuer:
            body += '''<th >Blockchain Indirizzo</th> </tr>'''

        # body += '''
        #     <tr> 
        #     <th>  <input class="form-control" id="myInput" name="myInput" type="text" placeholder="Search..">  </th>
        #     <th>  <input class="form-control" id="myInput" name="myInput" type="text" placeholder="Search..">  </th>
        #     <th>  <input class="form-control" id="myInput" name="myInput" type="text" placeholder="Search..">   </th>
        #     <th>  <input class="form-control" id="myInput" name="myInput" type="text" placeholder="Search..">   </th>
        #     <th>  <input class="form-control" id="myInput" name="myInput" type="text" placeholder="Search..">   </th>
        #     <th>  <input class="form-control" id="myInput" name="myInput" type="text" placeholder="Search..">  </th>
        #     </tr>
        #     '''
            
        if native_flag:
            if nparams['start'] == 0:
                native_units=self.chain_native_units(chain)            
                body += '<tr>'
                body += '<td>Native</td>'
                body += '<td>'+str(chain_rewards)+'</td>'
                if max_count>0:
                    body += '<td></td>'            
                body += '<td>'+str(native_units)+'</td>'
                body += '<td></td><td></td><td></td>'
                body += '</tr>'            
        
       
        #search box code 
     
        if response['result'] : 
            self.allresult = reversed(response['result'])

        for asset in reversed(response['result']):
            body += '<tr id="myTable">'
             
            entity_quoted=asset['issuetxid'] 
            if ('name' in asset) and (len(asset['name']) > 0):                
                entity_quoted=parse.quote_plus(asset['name'])
                splitword = '-'
                nome= asset['name']
                
                body +=   '<td> <a href="' + chain.config['path-name'] + '/asset/' + entity_quoted +  '"   target="_blank"  >' + nome.partition(splitword)[0] + '</a> </td>'  
                   
            else:  
                body += '<td><a href="' + chain.config['path-name'] + '/asset/' + entity_quoted + '">No name</a></td>'    

            orario =asset['name']
            # afterword = orario.split("--",1)[1]     str(orarion[-19:])
            now = datetime.now()
            
            details=asset['details']
            ari_dict=json.dumps(details)
            my_dict = json.loads(ari_dict)
            orarion=asset['name']
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            if orario is not None:
                if  my_dict['tipo_oprazione'] ==  "Visualizzazione Documento nel Fascicolo" :
                    togettime =  my_dict['userName']
                    
                    body += '<td>' +  str(togettime[-19:]) + '</td>'    
                else : 
                    body += '<td>' +  str(orarion[-19:])   + '</td>'             
            if self.display_local:
                if asset['subscribed']:                
                    body += '<td><a href="' + chain.config['path-name'] + '/assettransactions/' + entity_quoted + '">' +   + '</a></td>'
                else:
                    body += '<td>Not subscribed</td>'
                
            qty_str=str(asset['issueqty'])
            limits=[]
            if ("totallimit" in asset) and (asset['totallimit'] is not None):
                limits.append("limit " + str(asset['totallimit']))
            if ("issuelimit" in asset) and (asset['issuelimit'] is not None):
                limits.append("max " + str(asset['issuelimit']) + " per issue")
            if len(limits) > 0:
                qty_str += ' (' + ', '.join(limits) + ')'

            info=response['result'][0]
                         
            body += '<td>'+  my_dict['tipo_oprazione']    +'</td>'    
           
            if max_count>0:
                body += '<td>'+my_dict['descrizione']   +'</td>'
            units_str=str(asset['units'])  
            
            if my_dict['tipo_oprazione'] == "Cambio Stato Fascicolo" :
               statocancel= my_dict['statoNew'] 
               body += '<td>'+  str(statocancel) +'</td>'
            elif my_dict['tipo_oprazione'] ==  "Cancellazione Messaggio Fascicolo" :
               statocancel= my_dict['statoCancellazione']  
               body += '<td>'+  str(statocancel) +'</td>'  
            elif my_dict['tipo_oprazione'] ==  "Nuovo Scoring del Fascicolo" :
               statocancel= my_dict['scoreNew']  
               body += '<td>'+  str(statocancel) +'</td>'    
             
            elif my_dict['tipo_oprazione'] ==  "Visualizzazione Documento nel Fascicolo" :
               statocancel= "visualizzato" 
               body += '<td>'+  str(statocancel) +'</td>'     
            elif my_dict['tipo_oprazione'] ==  "Conferma Lettura Messagio nel Fascicolo" :
               statocancel=  my_dict['statoLettura']
               body += '<td>'+  str(statocancel) +'</td>'     
            elif my_dict['tipo_oprazione'] ==  "Spegnimento Alert del Fascicolo" :
               statocancel=  my_dict['statoLettura']
               body += '<td>'+  str(statocancel) +'</td>'   
                
            elif my_dict['tipo_oprazione'] ==  "Cancellazione Alert Fascicolo" :
               statocancel=  "Ripristinato"
               body += '<td>'+  str(statocancel) +'</td>' 
            
            elif my_dict['tipo_oprazione'] ==  "Cancellazione Documento nel Fascicolo" :
               statocancel=  my_dict['statoDocumento'] 
               body += '<td>'+  str(statocancel) +'</td>'   

            elif my_dict['tipo_oprazione'] ==  "Caricamento Nuovo Documento nel Fascicolo" :
               statocancel=  my_dict['descrizioneTipoDoc']   
               body += '<td>'+  str(statocancel) +'</td>'       
            else : 
                statocancel =" "    
                body += '<td>'+  str(statocancel) +'</td>'
                
            open_str=str(asset['open'])
            can_open=False
            can_close=False
            if ("canopen" in asset) and asset['canopen']:
                can_open=True
            if ("canclose" in asset) and asset['canclose']:
                can_close=True
            if can_open:
                if can_close:
                    open_str += ' (can open and close)'
                else:
                    open_str += ' (can open)'
            else:
                if can_close:
                    open_str += ' (can close)'
           # body += '<td>'+open_str+'</td>'
            
            fungible_str=str(True)
            if ("fungible" in asset):
                fungible_str=str(asset['fungible'])
            # body += '<td>'+fungible_str+'</td>'
            
            if show_issuer:
                body += '<td style="width: 240px"> ' + asset['issues'][0]['issuers'][0] + '</td>'
                
           # body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + asset['issuetxid'] + '">' + asset['issuetxid'][0:10]+ '...</a></td>'                        
            body += '</tr>'

        body+='</table>'
            
        return self.standard_response(body)
    #testing method     
    def pdfgenerator2nd():
        print ("something")

    def handle_assetsummary(self,chain,params,nparams):

        body ='<h3>Summary</h3>'

        body = '<a href="downloadsummarypdf" style="float:right"> <img  style="float:right; "  src="PDF-ICON.png" alt="MultiChain logo" data-toggle="tooltip" data-placement="top" title="Generate PDF" /></a>'
        
        if chain is None:        
            return self.standard_response(body + '<div class="alert alert-danger" role="alert">Chain not found</div>')
            
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
            
        entity_quoted=params[0]            
        entity_name=parse.unquote_plus(entity_quoted)
        
        response=chain.request("listassets",[entity_name,False])
        first_issue=chain.request("listassetissues",[entity_name,True,1,0])
        if response['result'] : 
            self.alldetails = response['result']
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response(body + '<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response(body + '<div class="alert alert-danger" role="warning">'+response['error']+'</div>')

        #all result is here for details  
        info=response['result'][0]
        
        self.detailresult = info

        first_issue=chain.request("listassetissues",[entity_name,True,1,0])        
        
        body += '<table class="table table-bordered table-striped table-condensed">'
        details=info['details']
        if (type(details) is OrderedDict) or (type(details) is dict):
            details=json.dumps(info['details'])
        
        my_dict = json.loads(details) 
        splitw='-'
        if 'name' in info:
            nomet =info['name']
            body += '<tr><td>Nome</td><td>'+info['name'].partition(splitw)[0]+ '</td></tr>'  
        orarion=info['name']
        # datetime object containing current date and time
        now = datetime.now()
        
        print("now =", now)

        # dd/mm/YY H:M:S     str(orarion[-19:])
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)	
        
        if orarion is not None:
                if  my_dict['tipo_oprazione'] ==  "Visualizzazione Documento nel Fascicolo" :
                    togettime =  my_dict['userName']
                    body += '<tr><td> Data </td><td>'+  str(togettime[-19:])  +'</td></tr>'    
                else : 
                    body += '<tr><td> Data </td><td>'+  str(orarion[-19:])  +'</td></tr>'
       
        tipo_oprazione = my_dict['tipo_oprazione']
        body += '<tr><td> Tipo Operazione effettuata </td><td>'+ str(tipo_oprazione)   +'</td></tr>'      
            
        cambiostato = "Cambio Stato Fascicolo"
        if my_dict['tipo_oprazione'] == cambiostato:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>' 
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>' 
           statoOld = my_dict['statoOld']
           body += '<tr><td> Vecchio Stato   </td><td>'+ str(statoOld)   +'</td></tr>'      
           statoNew = my_dict['statoNew'] 
           body += '<tr><td> Nuovo Stato   </td><td>'+ str(statoNew)   +'</td></tr>'    
         
        NuovoScoringFascicolo = "Nuovo Scoring del Fascicolo"
        if my_dict['tipo_oprazione'] == NuovoScoringFascicolo:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>'  
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>' 
           scoreOld = my_dict['scoreOld']
           body += '<tr><td> Vecchio Score  </td><td>'+ str(scoreOld)   +'</td></tr>'      
           scoreNew = my_dict['scoreNew'] 
           body += '<tr><td> Nuovo Score   </td><td>'+ str(scoreNew)   +'</td></tr>'    
          
        CancellazioneAlert = "Cancellazione Alert Fascicolo"
        if my_dict['tipo_oprazione'] == CancellazioneAlert:
           statoCancellazione = my_dict['statoCancellazione']
           body += '<tr><td> Stato Cancellazione  </td><td>'+ str(statoCancellazione)   +'</td></tr>'   
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>' 
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'             
           idMessaggioAlert = my_dict['idMessaggioAlert'] 
           body += '<tr><td> Id Messaggio Alert   </td><td>'+ str(idMessaggioAlert)   +'</td></tr>'  
           
        CancellazioneMessaggio = "Cancellazione Messaggio Fascicolo"
        if my_dict['tipo_oprazione'] == CancellazioneMessaggio:
           statoCancellazione = my_dict['statoCancellazione']
           body += '<tr><td> Stato Cancellazione  </td><td>'+ str(statoCancellazione)   +'</td></tr>'  
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>' 
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           idMessaggioAlert = my_dict['idMessaggioAlert'] 
           body += '<tr><td> Id Messaggio Alert   </td><td>'+ str(idMessaggioAlert)   +'</td></tr>'  
          
        CaricamentoNuovoDocumento = "Caricamento Nuovo Documento nel Fascicolo"
        if my_dict['tipo_oprazione'] == CaricamentoNuovoDocumento:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>'  
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'   
           nomeFileDoc = my_dict['nomeFileDoc']
           body += '<tr><td> Nome File Doc  </td><td>'+ str(nomeFileDoc)   +'</td></tr>'  
           idDocumento = my_dict['idDocumento']
           body += '<tr><td> Id Documento  </td><td>'+ str(idDocumento)   +'</td></tr>'  
           descrizioneTipoDoc = my_dict['descrizioneTipoDoc'] 
           body += '<tr><td> Descrizione Tipo Doc  </td><td>'+ str(descrizioneTipoDoc)   +'</td></tr>'
          
        ModificaDocumento = "Modifica Documento nel Fascicolo"
        if my_dict['tipo_oprazione'] == ModificaDocumento:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>'  
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>' 
           nomeFileDoc = my_dict['nomeFileDoc']
           body += '<tr><td> Nome File Doc  </td><td>'+ str(nomeFileDoc)   +'</td></tr>'  
           idDocumento = my_dict['idDocumento']
           body += '<tr><td> Id Documento  </td><td>'+ str(idDocumento)   +'</td></tr>'  
           descrizioneTipoDoc = my_dict['descrizioneTipoDoc'] 
           body += '<tr><td> Descrizione Tipo Doc  </td><td>'+ str(descrizioneTipoDoc)   +'</td></tr>' 
           
        VisualizzazioneDocumento = "Visualizzazione Documento nel Fascicolo"
        if my_dict['tipo_oprazione'] == VisualizzazioneDocumento:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>'  
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           nomeFileDoc = my_dict['nomeFileDoc']
           body += '<tr><td> Nome File Doc  </td><td>'+ str(nomeFileDoc)   +'</td></tr>'  
           idDocumento = my_dict['idDocumento']
           body += '<tr><td> Id Documento  </td><td>'+ str(idDocumento)   +'</td></tr>'  
           descrizioneTipoDoc = my_dict['descrizioneTipoDoc'] 
           body += '<tr><td> Descrizione Tipo Doc  </td><td>'+ str(descrizioneTipoDoc)   +'</td></tr>' 
            
        CancellazioneDocumento = "Cancellazione Documento nel Fascicolo"
        if my_dict['tipo_oprazione'] == CancellazioneDocumento:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>' 
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           nomeFileDoc = my_dict['nomeFileDoc']
           body += '<tr><td> Nome File Doc  </td><td>'+ str(nomeFileDoc)   +'</td></tr>'  
           idDocumento = my_dict['idDocumento']
           body += '<tr><td> Id Documento  </td><td>'+ str(idDocumento)   +'</td></tr>'  
           descrizioneTipoDoc = my_dict['descrizioneTipoDoc'] 
           body += '<tr><td> Descrizione Tipo Doc  </td><td>'+ str(descrizioneTipoDoc)   +'</td></tr>' 
           statoDocumento = my_dict['statoDocumento'] 
           body += '<tr><td> Stato Documento  </td><td>'+ str(statoDocumento)   +'</td></tr>' 
           
        ConfermaLetturaMessagio = "Conferma Lettura Messagio nel Fascicolo"
        if my_dict['tipo_oprazione']  == ConfermaLetturaMessagio:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>' 
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           idMessaggioAlert = my_dict['idMessaggioAlert'] 
           body += '<tr><td> Id Messaggio Alert   </td><td>'+ str(idMessaggioAlert)   +'</td></tr>'  
           statoLettura = my_dict['statoLettura']
           body += '<tr><td> Stato Lettura  </td><td>'+ str(statoLettura)   +'</td></tr>'  

        spegnimentoAlert = "Spegnimento Alert del Fascicolo"
        if my_dict['tipo_oprazione']  == spegnimentoAlert:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>' 
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           idMessaggioAlert = my_dict['idMessaggioAlert'] 
           body += '<tr><td> Id Messaggio Alert   </td><td>'+ str(idMessaggioAlert)   +'</td></tr>'  
           statoLettura = my_dict['statoLettura']
           body += '<tr><td> Stato Lettura  </td><td>'+ str(statoLettura)   +'</td></tr>'  
           
        NuovoMessaggio = "Nuovo Messaggio nel Fascicolo"
        if my_dict['tipo_oprazione']  == NuovoMessaggio:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>'  
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           idMessaggioAlert = my_dict['idMessaggioAlert'] 
           body += '<tr><td> Id Messaggio Alert   </td><td>'+ str(idMessaggioAlert)   +'</td></tr>'  
           
        NuovoAlert = "Nuovo Alert nel Fascicolo"
        if my_dict['tipo_oprazione']  == NuovoAlert:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>'  
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           idMessaggioAlert = my_dict['idMessaggioAlert'] 
           body += '<tr><td> Id Messaggio Alert   </td><td>'+ str(idMessaggioAlert)   +'</td></tr>'  
          
        ModificaMessaggio = "Modifica Messaggio nel Fascicolo"
        if my_dict['tipo_oprazione']  == ModificaMessaggio:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>'  
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           idMessaggioAlert = my_dict['idMessaggioAlert'] 
           body += '<tr><td> Id Messaggio Alert   </td><td>'+ str(idMessaggioAlert)   +'</td></tr>'  
          
        ModificaAlert = "Modifica Alert nel Fascicolo"
        if my_dict['tipo_oprazione']  == ModificaAlert:
           descrizione = my_dict['descrizione'] 
           body += '<tr><td> Descrizione  </td><td>'+ str(descrizione)   +'</td></tr>'  
           idFascicolo = my_dict['idFascicolo']
           body += '<tr><td> ID Fascicolo  </td><td>'+ str(idFascicolo)   +'</td></tr>'  
           idMessaggioAlert = my_dict['idMessaggioAlert'] 
           body += '<tr><td> Id Messaggio Alert   </td><td>'+ str(idMessaggioAlert)   +'</td></tr>'  
          
        body += '<tr><td>Prima Transazione</td><td><a href="' + chain.config['path-name'] + '/transaction/' + info['issuetxid'] + '">' + info['issuetxid']+ '</a></td></tr>'        
        if ('assetref' in info) and (info['assetref'] is not None):
            body += '<tr><td>Riferimento Asset</td><td>'+str(info['assetref'])+'</td></tr>'        
        if "restrict" in info:
            restrict = info["restrict"]
        else:
            restrict = {}
        restrict_str = ', '.join(k for k, v in restrict.items() if v)
        if restrict_str == '':
            restrict_str="None"
        open_str=str(info['open'])
        can_open=False
        can_close=False
        if ("canopen" in info) and info['canopen']:
            can_open=True
        if ("canclose" in info) and info['canclose']:
            can_close=True
        if can_open:
            if can_close:
                open_str += ' (can open and close)'
            else:
                open_str += ' (can open)'
        else:
            if can_close:
                open_str += ' (can close)'
        body += '<tr><td>NFT Block Aperto</td><td>'+open_str+'</td></tr>'        
        fungible_str=str(True)
        if ("fungible" in info):
            fungible_str=str(info['fungible'])
        body += '<tr><td>NFT Token</td><td>'+fungible_str+'</td></tr>'        
        
        body += '<tr><td>Restrizione</td><td>'+restrict_str+' <a href="' + chain.config['path-name'] + '/assetpermissions/' + entity_quoted + '">(view permissions)</a></td></tr>'        
        
        qty_str=str(info['issueqty'])
        limits=[]
        if ("totallimit" in info) and (info['totallimit'] is not None):
            limits.append("limit " + str(info['totallimit']))
        if ("issuelimit" in info) and (info['issuelimit'] is not None):
            limits.append("max " + str(info['issuelimit']) + " per issue")
        if len(limits) > 0:
            qty_str += ' (' + ', '.join(limits) + ')'
            
        body += '<tr><td>Issues </td><td>'+qty_str+'</td></tr>'        
        if first_issue['result'] is not None:
            if len(first_issue['result'][0]['issuers'])==1:
                creator = first_issue['result'][0]['issuers'][0]
                creator_address = '<a href="' + chain.config['path-name'] + '/address/'+ creator + '">' + creator + '</a>'
            else:
                creator_address = ''
                for creator in first_issue['result'][0]['issuers']:
                    creator_link = '<a href="' + chain.config['path-name'] + '/address/' + creator + '">' + creator + '</a>'
                    creator_address += '{0}<br/>'.format(creator_link)
            body += '<tr><td>Indirizzo Blockchain</td><td>'+creator_address+'</td></tr>'        
        issue_count='?'
        if "issuecount" in info:
            issue_count=info['issuecount']
            body += '<tr><td>Numero di Transazioni</td><td><a href="' + chain.config['path-name'] + '/assetissues/' + entity_quoted + '">'+str(issue_count)+'</a></td></tr>'        
            
        body += '<tr><td>Multipile</td><td>'+str(info['multiple'])+'</td></tr>'        
        units_str=str(info['units'])                
        if ("issueonlysingleunit" in info) and info['issueonlysingleunit']:
            units_str += " (single unit per issuance)"
            
        body += '<tr><td>Unità</td><td>'+units_str+'</td></tr>'  
           
        if self.display_local:            
            if info['subscribed']:
                body += '<tr><td>Transazioni</td><td><a href="' + chain.config['path-name'] + '/assettransactions/' + entity_quoted + '">' + str(info['transactions']) + '</a></td>'
                body += '<tr><td>Confirmed</td><td>' + str(info['confirmed']) + '</td>'
            
        address_count=chain.request("explorerlistassetaddresses",[entity_name,"-"])
        if address_count['result'] is not None:
            body += '<tr><td>Indirizzo User </td><td><a href="' + chain.config['path-name'] + '/assetholders/' + entity_quoted + '">'+str(address_count['result'])+'</a></td></tr>'
       
        body += '</table>'

        return self.standard_response(body)
    
    def handle_assetissues(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
            
        entity_quoted=params[0]            
        entity_name=parse.unquote_plus(entity_quoted)
        
        response=chain.request("listassets",[entity_name,False])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response('<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response('<div class="alert alert-danger" role="warning">'+response['error']+'</div>')

        if 'issuecount' not in response['result'][0]:
            return self.standard_response('<div class="alert alert-danger" role="warning">Not supported in this version of MultiChain</div>')
            
        fungible=True
        if ('fungible' in response['result'][0]):
            fungible=response['result'][0]['fungible']
        last=response['result'][0]['issuecount']
        
        self.expand_params(nparams,last,True)
        
        response=chain.request("listassetissues",[entity_name,True,nparams['count'],nparams['start']])
            
        if response['result'] is None:
            return self.error_response(response)                        
        
        body = ''
        if nparams['nav']:
            body+=nav_bar(chain.config['path-name'] + '/assetissues/' + entity_name,nparams,"issues ")

        body += '<table class="table table-striped"><tr>'
        body += '<th>Issue Amount</th>'
        if not fungible:
            body += '<th>Token</th>'
        body += '<th>Issuers</th>'
        body += '<th>Details</th>'
        body += '<th>Transaction</th>'
        body += '</tr>'

        for info in response['result']:
            body += '<tr>'
            body += '<td>'+str(info['qty'])+'</td>'        
            if not fungible:
                token_str=''
                if ('token' in info) and (info['token'] is not None):
                    token_str=info['token']
                body += '<td>'+token_str+'</td>'                            
            if len(info['issuers'])==1:
                creator = info['issuers'][0]
                creator_address = '<a href="' + chain.config['path-name'] + '/address/'+ creator + '">' + creator + '</a>'
            else:
                creator_address = ''
                for creator in info['issuers']:
                    creator_link = '<a href="' + chain.config['path-name'] + '/address/' + creator + '">' + creator + '</a>'
                    creator_address += '{0}<br/>'.format(creator_link)
            body += '<td>'+creator_address+'</td>'        
            details=info['details']
            if (type(details) is OrderedDict) or (type(details) is dict):
                details=json.dumps(info['details'])
            body += '<td>'+str(details)+'</td>'                                    
            body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + info['txid'] + '">' + info['txid'][0:10]+ '...</a></td>'        
            body += '</tr>'
            
        body += '</table>'
        return self.standard_response(body)
    
    
    def handle_streams(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        last=-1                    
        entity_counts=chain.request("getchaintotals",[])            
        if entity_counts['result'] is None:
            return self.error_response(entity_counts)
        if entity_counts['result'] is not None:
            last=entity_counts['result']['streams']
            
        if last<=0:            
            return self.standard_response('<div class="empty-list">No streams have been created in this chain</div>')            
            
        self.expand_params(nparams,last,True)
        
        response=chain.request("liststreams",['*', True, nparams['count'], nparams['start']])
            
        if response['result'] is None:
            return self.error_response(response)
                        
        body=nav_bar(chain.config['path-name'] + '/streams',nparams,"streams ")
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Name</th>
            <th>PDF Items</th>
            <th>Keys</th>
            <th>Publishers Details</th>
            <th>Restrict</th>
            <th>Creator Details</th>
            <th>Creation Transaction</th>
            </tr>
            '''
            
        for stream in response['result']:
            body += '<tr>'
            entity_quoted = stream['createtxid']                 
            if ('name' in stream) and (len(stream['name']) > 0):                
                entity_quoted=parse.quote_plus(stream['name'])
                body += '<td><a href="' + chain.config['path-name'] + '/stream/' + entity_quoted + '">' + stream['name'] + '</a></td>'    
            else:  
                body += '<td><a href="' + chain.config['path-name'] + '/stream/' + entity_quoted + '">No name</a></td>'    
                
            if stream['subscribed']:                
                body += '<td><a href="' + chain.config['path-name'] + '/streamitems/' + entity_quoted + '">' + str(stream['items']) + '</a></td>'
                body += '<td><a href="' + chain.config['path-name'] + '/streamkeys/' + entity_quoted + '">' + str(stream['keys']) + '</a></td>'
                body += '<td><a href="' + chain.config['path-name'] + '/streampublishers/' + entity_quoted + '">' + str(stream['publishers']) + '</a></td>'
            else:
                body += '<td colspan="3">Not subscribed</td>'
                
            if "restrict" in stream:
                restrict = stream["restrict"]
            else:
                restrict = {"write": stream["open"]}
            restrict_str = ', '.join(k for k, v in restrict.items() if v)
            if restrict_str == '':
                restrict_str="None"
            
            body += '<td>' + restrict_str + '</td>'            
            body += '<td><a href="' + chain.config['path-name'] + '/address/' + stream['creators'][0] + '">' + stream['creators'][0] + '</a></td>'
            body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + stream['createtxid'] + '">' + stream['createtxid']+ '</a></td>'                        
            body += '</tr>'

        body+='</table>'
            
        return self.standard_response(body)
        
            
    def handle_streamsummary(self,chain,params,nparams):
        body = '<h3>Summary</h3>'
        if chain is None:        
            return self.standard_response(body + '<div class="alert alert-danger" role="alert">Chain not found</div>')
            
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
            
        entity_quoted=params[0]            
        entity_name=parse.unquote_plus(entity_quoted)
        
        response=chain.request("liststreams",[entity_name,True])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response(body + '<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response(body + '<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
                
        info=response['result'][0]
        
        body += '<table class="table table-bordered table-striped table-condensed">'
            
        if 'name' in info:
            body += '<tr><td>Name</td><td>'+info['name']+'</td></tr>'        
        body += '<tr><td>Creation Transaction</td><td><a href="' + chain.config['path-name'] + '/transaction/' + info['createtxid'] + '">' + info['createtxid']+ '</a></td></tr>'        
        if ('streamref' in info) and (info['streamref'] is not None):
            body += '<tr><td>Stream Reference</td><td>'+str(info['streamref'])+'</td></tr>'        
        if "restrict" in info:
            restrict = info["restrict"]
        else:
            restrict = {"write": info["open"]}
        restrict_str = ', '.join(k for k, v in restrict.items() if v)
        if restrict_str == '':
            restrict_str="None"
        body += '<tr><td>Restrict</td><td>'+restrict_str+' <a href="' + chain.config['path-name'] + '/streampermissions/' + entity_quoted + '">(view permissions)</a></td></tr>'        
        if "salted" in info:
            body += '<tr><td>Salted</td><td>'+str(info['salted'])+'</td></tr>'        
        if len(info['creators'])==1:
            creator = info['creators'][0]
            creator_address = '<a href="' + chain.config['path-name'] + '/address/'+ creator + '">' + creator + '</a>'
        else:
            creator_address = ''
            for creator in info['creators']:
                creator_link = '<a href="' + chain.config['path-name'] + '/address/' + creator + '">' + creator + '</a>'
                creator_address += '{0}<br/>'.format(creator_link)
        body += '<tr><td>Creators</td><td>'+creator_address+'</td></tr>'        
        
        details=info['details']
        if (type(details) is OrderedDict) or (type(details) is dict):
            details=json.dumps(info['details'])
        body += '<tr><td>Details</td><td>'+str(details)+'</td></tr>'        
        
        if info['subscribed']:
            if self.display_local:            
                body += '<tr><td>Subscribed</td><td><span class="label label-success">Yes</span></td></tr>'        
            body += '<tr><td>Items</td><td><a href="' + chain.config['path-name'] + '/streamitems/' + entity_quoted + '">' + str(info['items']) + '</a></td>'
            body += '<tr><td>Confirmed</td><td>' + str(info['confirmed']) + '</td>'
            body += '<tr><td>Keys</td><td><a href="' + chain.config['path-name'] + '/streamkeys/' + entity_quoted + '">' + str(info['keys']) + '</a></td>'
            body += '<tr><td>Publishers</td><td><a href="' + chain.config['path-name'] + '/streampublishers/' + entity_quoted + '">' + str(info['publishers']) + '</a></td>'
        else:
            if self.display_local:            
                body += '<tr><td>Subscribed</td><td><span class="label label-warning">No</span></td></tr>'        
            
        body += '</table>'

        return self.standard_response(body)
        
    def handle_assettransactions(self,chain,params,nparams):
        return self.do_assettransactions(chain,params,nparams,params[0])
        
    def handle_assetholders(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
            
        entity_quoted=params[0]            
        entity_name=parse.unquote_plus(entity_quoted)
        if entity_quoted == DEFAULT_NATIVE_CURRENCY_ID:
            entity_name=""
            
        asset_count=chain.request("explorerlistassetaddresses",[entity_name,"-"])
        if asset_count['result'] is None:
            return self.error_response(asset_count)
        last=asset_count['result']
        
        if last<=0:            
            return self.standard_response('<div class="empty-list">No holders found for this asset</div>')            
            
        self.expand_params(nparams,last)
        
        response=chain.request("explorerlistassetaddresses",[entity_name,True,nparams['count'],nparams['start']])
            
        if response['result'] is None:
            return self.error_response(response)                        
        
        body = ''
        if nparams['nav']:
            body+=nav_bar(chain.config['path-name'] + '/assetsholders/' + entity_name,nparams,"addresses ")
            
        body += '''
            <table class="table table-striped">
            <tr>
            <th>Address</th>
            <th>Balance</th>
            </tr>
            '''
            
        for address in reversed(response['result']):
            body += '<tr>'
            body += '<td><a href="' + chain.config['path-name'] + '/address/' + address['address'] + '">' + address['address'] + '</a></td>'    
                
            body += '<td>'+str(address['qty'])+' <a href="' + chain.config['path-name'] + '/assetholdertransactions/' + entity_quoted + '/' + address['address'] + '">(transactions)</a></td>'    
            body += '</tr>'
            
        body+='</table>'
            
        return self.standard_response(body)
                   
    def do_assettransactions(self,chain,params,nparams,entity_quoted, keytype=None, holder = None):
        if chain is None:        
            return self.standard_response('')
            
        entity_name=parse.unquote_plus(entity_quoted)
        
        count_method="listassets"
        method="listassettransactions"
        field="transactions"
        link='/assettransactions/' + entity_quoted
        api_params=[entity_name]
        if keytype is None:            
            if holder is not None:
                method="listassetholdertransactions"
                count_method="listassetholders"
                link='/holdertransactions/'  + entity_quoted + '/' + holder
                api_params.append(holder)
            count_params=api_params
        else:
            field=keytype
            method="listasset" + keytype
            link='/asset' + keytype +'/' + entity_quoted
            count_params=api_params.copy()
            api_params.append("*")

        api_params.append(True)            
        
        last=-1            
        if keytype is None:            
            summary=chain.request(count_method,count_params)
            if summary['result'] is None:
                return self.error_response(summary)
            if summary['result'][0] is None:
                return self.standard_response('')
            if field not in summary['result'][0]:
                return self.standard_response('<div class="alert alert-danger" role="alert">Not subscribed to this asset</div>')
            last=summary['result'][0][field]
            
        self.expand_params(nparams,last)
        
        api_params.append(nparams['count'])
        api_params.append(nparams['start'])
                        
        if keytype is None:            
            response=chain.request(method,api_params)
        else:
            response={'result':[]}
            
        if response['result'] is None:
            return self.error_response(response)
            
            
        body=''
        if nparams['nav']:
            body+=nav_bar(chain.config['path-name'] + link,nparams,"transactions ")
            
        body += '<table class="table table-striped"><tr>'
        if keytype is None:
            body += '<th>Transazione</th>'
            body += '<th>Indirizzi interessati</th>'
            body += '<th>Data/Orario Inserimento</th>'
            body += '<th>Block</th>'
        else:
            if keytype == "holders":
                body += '<th>Indirizzo</th>'
                body += '<th style="text-align:right"> Balance</th>'
                body += '<th>Transazione</th>'
                body += '<th>Confermato</th>'
                body += '<th>Ultimo orario</th>'
                body += '<th>Ultimo Valore Transazioni</th>'
                body += '<th>Ultimo Transazione</th>'
                
        body += '</tr>'
            
        for res in reversed(response['result']):
               
            if keytype is None:                     
                tx=res
                            
            non_zero_count=0
            for h,v in tx['addresses'].items():
                if v != 0:
                    non_zero_count += 1
            
            holders_html=''
            if non_zero_count > 0:
                holders_html+='<table class="table table-bordered table-condensed inner-table">'
                for h,v in tx['addresses'].items():
                    holders_html+='<tr><td><a href="' + chain.config['path-name'] + '/assetholdertransactions/' + entity_quoted  + '/' + h + '">' + h + '</a></td>'
                    holders_html+='<td align="right">' + signed_amount_html(v) + '</td></tr>'
                holders_html+='</table>'
            else:
                holders_html="None"
                
            tx_html='<a href="' + chain.config['path-name'] + '/transaction/' + tx['txid'] + '">' + tx['txid']+ '</a>'                    
            body += '<tr style="width = 20px">>'
            if keytype is None:
                body += '<td>'+tx_html+'</td>'                        
                body += '<td>'+holders_html+'</td>'                
                if ('blockheight' in tx) and (tx['blockheight'] is not None):                
                    body += '<td>' + format_time(tx['blocktime']) + '</td>'                        
                    body += '<td><a href="' + chain.config['path-name'] + '/block/' + str(tx['blockheight']) + '">' + str(tx['blockheight']) + '</a></td>'                        
                else:
                    body += '<td></td><td></td>'
            body += '</tr>'
            legend1 = "NFT Token (Non Fungible Token)"
            legend2 = "NFT Block (aperto per il futuro)"
            legend3 = "Riferimento Asset (Numero di transazione dell'asset)"
            legend4 = "Restrizione (Permesso di dettaglio)"
            legend5 = "Prima Transazione (Dettagli Informazioni sulla transazione)"
            body = ''   
            body += '<div >' + legend1 + " , " +  legend2 +  " , " +legend3+  " , " +legend4 + " , "+ legend5+'</div>'
        

           

        body+='</table>'
       
        return self.standard_response(body)  

         

    def handle_streamitems(self,chain,params,nparams):
        
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')

        return self.do_streamitems(chain,params,nparams,params[0])
        
    def handle_streamkeys(self,chain,params,nparams):
        
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')

        return self.do_streamitems(chain,params,nparams,params[0],"keys")
        
    def handle_streampublishers(self,chain,params,nparams):
        
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')

        return self.do_streamitems(chain,params,nparams,params[0],"publishers")
        
    def handle_publisheritems(self,chain,params,nparams):
        
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 2:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
        
        return self.do_streamitems(chain,params,nparams,params[0],None,str(params[1]))
        
    def handle_keyitems(self,chain,params,nparams):
        
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 2:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
        return self.do_streamitems(chain,params,nparams,params[0],None,None,parse.unquote_plus(str(params[1])))
        
    def do_streamitems(self,chain, params, nparams, entity_quoted, keytype=None, publisher = None, streamkey = None):
        
        if chain is None:        
            return self.standard_response('')
            
        entity_name=parse.unquote_plus(entity_quoted)
                    
        count_method="liststreams"
        method="liststreamitems"
        field="items"
        link='/streamitems/' + entity_quoted
        api_params=[entity_name]
        if keytype is None:            
            if publisher is not None:
                method="liststreampublisheritems"
                count_method="liststreampublishers"
                link='/publisheritems/'  + entity_quoted + '/' + publisher
                api_params.append(publisher)
            if streamkey is not None:
                method="liststreamkeyitems"
                count_method="liststreamkeys"
                link='/keyitems/'  + entity_quoted + '/'  + parse.quote_plus(streamkey)
                api_params.append(streamkey)
            count_params=api_params
        else:
            field=keytype
            method="liststream" + keytype
            link='/stream' + keytype +'/' + entity_quoted
            count_params=api_params.copy()
            api_params.append("*")
            
        api_params.append(True)            

        summary=chain.request(count_method,count_params)

        if summary['result'] is None:
            return self.error_response(summary)
        if summary['result'][0] is None:
            return self.standard_response('')
        if field not in summary['result'][0]:
            return self.standard_response('<div class="alert alert-danger" role="alert">Not subscribed to this stream</div>')
        last=summary['result'][0][field]
        if last<=0:
            if publisher is not None:
                return self.standard_response('<div class="empty-list">No items have been published by this address in this stream</div>')            
            if streamkey is not None:
                return self.standard_response('<div class="empty-list">No items have been published with this key in this stream</div>')       
            if summary['result'][0]['items'] > 0:
                return self.standard_response('<div class="empty-list">The required index is not active for this subscription</div>')            
            else:
                return self.standard_response('<div class="empty-list">No items have been published in this stream</div>')            
                
        self.expand_params(nparams,last)
        
        api_params.append(nparams['count'])
        api_params.append(nparams['start'])
                        
        response=chain.request(method,api_params)
            
        if response['result'] is None:
            return self.error_response(response)
            
            
        body=''
        if nparams['nav']:
            body+=nav_bar(chain.config['path-name'] + link,nparams,"items ")
            
        body += '<table class="table table-striped"><tr>'
        if keytype is None:
            body += '<th>Time</th>'
            body += '<th>Key</th>'
            body += '<th>Value</th>'
            body += '<th>Publisher</th>'
            body += '<th>Offchain</th>'
            body += '<th>Transaction</th>'
        else:
            if keytype == "keys":
                body += '<th>Key</th>'
                body += '<th>Items</th>'
                body += '<th>Confirmed</th>'
                body += '<th>Last Time</th>'
                body += '<th>Last Value</th>'
                body += '<th>Last Publisher</th>'
#                body += '<th>Last Offchain</th>'
                body += '<th>Last Transaction</th>'
            else:
                body += '<th>Publisher</th>'
                body += '<th>Items</th>'
                body += '<th>Confirmed</th>'
                body += '<th>Last Time</th>'
                body += '<th>Last Key</th>'
                body += '<th>Last Value</th>'
#                body += '<th>Last Offchain</th>'
                body += '<th>Last Transaction</th>'
                
        body += '</tr>'
            
        for res in reversed(response['result']):
               
            if keytype is None:                     
                item=res
            else:
                item=res['last']
                items_count=str(res['items'])
                confirmed_count=str(res['confirmed'])
                
            if item['confirmations'] > 0:
                time_html=format_time(item['blocktime'])
            else:
                time_html="Unconfirmed"
            
            keys = []
            if 'key' in item:
                keys = [item['key']]
            else:  # Get all keys
                keys = item['keys']

            if (keytype == 'keys'):
                keys=[res['key']]
                
            # Create a list of key links
            prefix = chain.config['path-name'] + '/keyitems/' + entity_quoted
            keylinks = ['<a href="{0}/{1}">{2}</a>'.format(prefix, parse.quote_plus(key),key) for key in keys]
            keyshtml = ', '.join(keylinks)
            # If list is too long, display only first few keys, and enable a popover with the full list
            key_limit = 5
            if len(keylinks) >= key_limit:
                keyshtml = '{}, <span class="ellipses" data-toggle="popover" data-content="{}">...</span>'.format(
                    ', '.join(keylinks[:key_limit]), escape(', '.join(keylinks), quote=True))


            if item['available']:                
                txid = item['txid']  # data['txid'] should be the same
                data = item['data']
                vout = item['vout']
                
                data_html=self.general_data_html(chain,data,txid,vout)
            else:
                data_html="Not available"
                txid = item['data']['txid']
            
            if (len(item['publishers'])==1) or (keytype == 'publishers'):
                p = item['publishers'][0]
                if keytype == 'publishers':
                    p=res['publisher']
                publisher_address = '<a href="' + chain.config['path-name'] + '/publisheritems/' + entity_quoted + '/' + p + '">' + p + '</a>'
            else:
                publisher_address = ''
                for p in item['publishers']:
                    publisher_link = '<a href="' + chain.config['path-name'] + '/publisheritems/' + entity_quoted + '/' + p + '">' + p + '</a>'
                    publisher_address += '{0}<br/>'.format(publisher_link)
                
            offchain_html="No"
            if item['offchain']:
                offchain_html="Yes"
                
            tx_html='<a href="' + chain.config['path-name'] + '/transaction/' + txid + '">' + txid[0:10]+ '...</a>'                    
            body += '<tr>'
            if keytype is None:
                body += '<td>'+time_html+'</td>'
                body += '<td>'+keyshtml+'</td>'
                body += '<td>'+data_html+'</td>'
                body += '<td>'+publisher_address+'</td>'
                body += '<td>'+offchain_html+'</td>'                        
                body += '<td>'+tx_html+'</td>'                        
            else:
                if keytype == "keys":
                    body += '<td>'+keyshtml+'</td>'
                    body += '<td>'+items_count+'</td>'
                    body += '<td>'+confirmed_count+'</td>'
                    body += '<td>'+time_html+'</td>'
                    body += '<td>'+data_html+'</td>'
                    body += '<td>'+publisher_address+'</td>'
#                    body += '<td>'+offchain_html+'</td>'                        
                    body += '<td>'+tx_html+'</td>'                        
                else:
                    body += '<td>'+publisher_address+'</td>'
                    body += '<td>'+items_count+'</td>'
                    body += '<td>'+confirmed_count+'</td>'
                    body += '<td>'+time_html+'</td>'
                    body += '<td>'+keyshtml+'</td>'
                    body += '<td>'+data_html+'</td>'
#                    body += '<td>'+offchain_html+'</td>'                        
                    body += '<td>'+tx_html+'</td>'                        
                    
            body += '</tr>'

        body+='</table>'
            
        return self.standard_response(body)
            
    def handle_globalpermissions(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        return self.do_permissions(chain,params,params[1:],'',None)

    def handle_assetpermissions(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
        
        return self.do_permissions(chain,params,params[1:],params[0],"asset")

    def handle_streampermissions(self,chain,params,nparams):
        if chain is None:        
            return self.standard_response('')
                    
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
        
        return self.do_permissions(chain,params,params[1:],params[0],"stream")

    def do_permissions(self,chain, params, nparams, entity_quoted, entitytype=None):
        if chain is None:        
            return self.standard_response('')
        
        entity_name=parse.unquote_plus(entity_quoted)
        
        api_params=[]
        if entitytype is not None:
            api_params=[entity_name + ".*"]
            if entitytype == "stream":
                allowed_permissions=ALLOWED_PERMISSIONS_STREAM.copy()
            if entitytype == "asset":
                allowed_permissions=ALLOWED_PERMISSIONS_ASSET.copy()
            if entitytype == "variable":
                allowed_permissions=ALLOWED_PERMISSIONS_VARIABLE.copy()
            if entitytype == "library":
                allowed_permissions=ALLOWED_PERMISSIONS_LIBRARY.copy()
        else:
            allowed_permissions=ALLOWED_PERMISSIONS_GLOBAL.copy()
            
        permissions={}
        for p in allowed_permissions:
            permission_def=PERMISSION_TEMPLATES[p].copy()
            permission_def['addresses']=[]
            permissions[p]=permission_def
            
        response=chain.request("listpermissions",api_params)
            
        if response['result'] is None:
            return self.error_response(response)
            
        for p in response['result']:
            if p['type'] in permissions:
                permissions[p['type']]['addresses'].append(p['address'])
        
        body = ''
        for p in allowed_permissions:
            if (len(permissions[p]['addresses']) > 0) or (p not in SHOW_PERMISSION_ONLY_IF_PRESENT):                
                body += '<h3>'+permissions[p]['display-name']+'</h3>'                
                body += '<table class="table table-bordered table-striped table-condensed">'
                for address in permissions[p]['addresses']:                
                    body += '<tr><td><a href="' + chain.config['path-name'] + '/address/' + address + '">' + address + '</a></td></tr>'
                body += '</table>'
            
        return self.standard_response(body)
        
        
    def handle_block(self,chain,params,nparams):
        body = '<h3>Block Summary</h3>'
        if chain is None:        
            return self.standard_response(body + '<div class="alert alert-danger" role="alert">Chain not found</div>')

        if len(params) < 1:
            return self.standard_response(body + '<div class="alert alert-danger" role="alert">Bad request</div>')
            
        response=chain.request("getblock",[params[0]])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response(body + '<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response(body + '<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
                
        body += '<table class="table table-bordered table-striped table-condensed">'
        body += '<tr><td>Hash</td><td>' + str(response['result']['hash']) +  '</td></tr>'
        if  'previousblockhash' in response['result']:
            body += '<tr><td>Previous Block</td><td><a href="' + chain.config['path-name'] + '/block/'+str(response['result']['height']-1)+'">' + str(response['result']['previousblockhash']) +  '</a></td></tr>'
        else:
            body += '<tr><td>Previous Block</td><td></td></tr>'
        if  'nextblockhash' in response['result']:                    
            body += '<tr><td>Next Block</td><td><a href="' + chain.config['path-name'] + '/block/'+str(response['result']['height']+1)+'">' + str(response['result']['nextblockhash']) +  '</a></td></tr>'
        else:
            body += '<tr><td>Next Block</td><td></td></tr>'
            
        body += '<tr><td>Height</td><td>' + str(response['result']['height']) +  '</td></tr>'
        body += '<tr><td>Miner</td><td><a href="' + chain.config['path-name'] + '/address/'+str(response['result']['miner'])+'">' + str(response['result']['miner']) +  '</a></td></tr>'
        body += '<tr><td>Version</td><td>' + str(response['result']['version']) +  '</td></tr>'
        body += '<tr><td>Transaction Merkle Root</td><td>' + str(response['result']['merkleroot']) +  '</td></tr>'
        body += '<tr><td>Time</td><td>' + format_time(response['result']['time']) +  '</td></tr>'
        body += '<tr><td>Nonce</td><td>' + str(response['result']['nonce']) +  '</td></tr>'
        body += '<tr><td>Transactions</td><td>' + str(len(response['result']['tx'])) +  '</td></tr>'
        body += '</table>'
        
        body += '<h3>Transactions</h3>'
        exp_response=chain.request("explorerlistblocktransactions",[int(params[0]),True,99999999])
        if (exp_response is None) or (exp_response['result'] is None):
            body += '''
                    <table class="table table-striped"><tr><th>Transaction</th>
                    </tr>
                    '''
                    
            for tx in response['result']['tx']:
                body += '<tr>'
                body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + tx + '">' + tx+ '</a></td>'                        
                body += '</tr>'
        else:
            body += '''
                    <table class="table table-striped"><tr><th>Transaction</th>
                    <th>Type</th>
                    </tr>
                    '''
            for tx in exp_response['result']:
                label_html=tags_to_label_html(tx['tags'])
                body += '<tr>'
                body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + tx['txid'] + '">' + tx['txid'] + '</a>'  + '</td>'                        
                body += '<td>' +  label_html + '</td>'                        
                body += '</tr>'
                                
        body += '</table>'
            
        return self.standard_response(body)
        
    def handle_blocksummary(self,chain,params,nparams):
        body = '<h3>Block Summary</h3>'
        if chain is None:        
            return self.standard_response(body + '<div class="alert alert-danger" role="alert">Chain not found</div>')

        if len(params) < 1:
            return self.standard_response(body + '<div class="alert alert-danger" role="alert">Bad request</div>')
            
        response=chain.request("getblock",[params[0]])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response(body + '<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response(body + '<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
                
        body += '<table class="table table-bordered table-striped table-condensed">'
        body += '<tr><td>Hash</td><td>' + str(response['result']['hash']) +  '</td></tr>'
        if  'previousblockhash' in response['result']:
            body += '<tr><td>Previous Block</td><td><a href="' + chain.config['path-name'] + '/block/'+str(response['result']['height']-1)+'">' + str(response['result']['previousblockhash']) +  '</a></td></tr>'
        else:
            body += '<tr><td>Previous Block</td><td></td></tr>'
        if  'nextblockhash' in response['result']:                    
            body += '<tr><td>Next Block</td><td><a href="' + chain.config['path-name'] + '/block/'+str(response['result']['height']+1)+'">' + str(response['result']['nextblockhash']) +  '</a></td></tr>'
        else:
            body += '<tr><td>Next Block</td><td></td></tr>'
            
        body += '<tr><td>Height</td><td>' + str(response['result']['height']) +  '</td></tr>'
        body += '<tr><td>Miner</td><td><a href="' + chain.config['path-name'] + '/address/'+str(response['result']['miner'])+'">' + str(response['result']['miner']) +  '</a></td></tr>'
        body += '<tr><td>Version</td><td>' + str(response['result']['version']) +  '</td></tr>'
        body += '<tr><td>Transaction Merkle Root</td><td>' + str(response['result']['merkleroot']) +  '</td></tr>'
        body += '<tr><td>Time</td><td>' + format_time(response['result']['time']) +  '</td></tr>'
        body += '<tr><td>Nonce</td><td>' + str(response['result']['nonce']) +  '</td></tr>'
        body += '<tr><td>Transactions</td><td><a href="' + chain.config['path-name'] + '/blocktransactions/'+params[0]+'">' + str(len(response['result']['tx'])) +  '</a></td></tr>'
        body += '</table>'
        
            
        tx_body = '<h3><a href="' + chain.config['path-name'] + '/blocktransactions/'+params[0]+'">Transactions</a></h3>'
        
        tx_counts=[(len(response['result']['tx']),0),(0,0)]
        
        if tx_counts[0][0]>100:
            tx_counts[1]=(10,tx_counts[0][0]-10)
            tx_counts[0]=(90,0)

        tx_body += '''
            <table class="table table-striped">
            <tr>
            <th>Txid</th>
            <th>Type</th>
            </tr>
            '''
        for p in range(0,2):
            if (p == 1) and (tx_counts[p][0]>0):
                tx_body += '<tr><td>...</td><td></td>'
                
            response=chain.request("explorerlistblocktransactions",[int(params[0]),True,tx_counts[p][0],tx_counts[p][1]])
            if response['result'] is None:
                tx_counts[1]=(0,0)    
                tx_body=""
            else:
                for tx in response['result']:
                    label_html=tags_to_label_html(tx['tags'])
                    tx_body += '<tr>'
                    tx_body += '<td><a href="' + chain.config['path-name'] + '/transaction/' + tx['txid'] + '">' + tx['txid'] + '</a>'  + '</td>'                        
                    tx_body += '<td>' +  label_html + '</td>'                        
                    tx_body += '</tr>'
        body+=tx_body
        
        return self.standard_response(body)
        
    def handle_txoutdata(self,chain,params,nparams):            
        if len(params) < 2:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
        
        response=chain.request("gettxoutdata",[str(params[0]),int(params[1])])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response('<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response('<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
                
        data=json.dumps(response['result'],indent=4)                
        return (200, [("Content-type", "application/json")], bytes(data,"utf-8"))
        
    def handle_rawtransaction(self,chain,params,nparams):            
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
        
        response=chain.request("explorergetrawtransaction",[str(params[0]),1])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response('<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response('<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
                
        data=json.dumps(response['result'],indent=4)                
        return (200, [("Content-type", "application/json")], bytes(data,"utf-8"))

    def handle_rawtransactionhex(self,chain,params,nparams):            
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')
        
        response=chain.request("getrawtransaction",[str(params[0]),0])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response('<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response('<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
            
        return self.standard_response(str(response['result']))
    
    def handle_transaction(self,chain,params,nparams):          
        
        if len(params) < 1:
            return self.standard_response('<div class="alert alert-danger" role="alert">Bad request</div>')

        response=chain.request("explorergetrawtransaction",[str(params[0]),1])
        if response['result'] is None:
            if ('connection-error' in response) and response['connection-error']:
                return self.standard_response('<div class="alert alert-danger" role="alert">'+response['error']+'</div>')
            else:
                return self.standard_response('<div class="alert alert-danger" role="warning">'+response['error']+'</div>')
            
        info=response['result']
            
        body = '<table class="table table-bordered table-striped table-condensed">'            
        body += '<tr><td>Hash</td><td>'+info['txid']+'</td></tr>'        
        body += '<tr><td>Confirmed In</td><td>'
        if info['blockheight'] is not None:
            body += '<a href="' + chain.config['path-name'] + '/block/'+str(info['blockheight'])+'">Block ' + str(info['blockheight']) +  '</a> (' +format_time(info['blocktime']) +')'            
        body += '</td></tr>'        

        holders_html=''
        if len(info['assets']) > 0:
            holders_html+='<table class="table table-bordered table-condensed inner-table">'
            for asset in info['assets']:
                entity_quoted=asset['issuetxid'] 
                if ('name' in asset) and (len(asset['name']) > 0):                
                    entity_quoted=parse.quote_plus(asset['name'])
                    entity_name=asset['name']
                else:
                    entity_name="Asset with no name"
                
                asset_link='<a href="' + chain.config['path-name'] + '/asset/' + entity_quoted + '">' + entity_name + '</a>'
                holders_html+='<tr><td><a href="' + chain.config['path-name'] + '/assetholdertransactions/' + entity_quoted  + '/' + asset['address'] + '">' + asset['address'] + '</a></td>'
                holders_html+='<td>' + asset_link + '</td>'
                holders_html+='<td align="right">' + signed_amount_html(asset['qty']) + '</td></tr>'
            holders_html+='</table>'
        else:
            holders_html="None"
            
        license_tx=False
        if len(info['vout']) == 1:
            for vout in info['vout']:
                if "license" in vout['tags']:
                    license_tx=True
            

        body += '<tr><td>Affected address balances</td><td>'+holders_html+'</td></tr>'         
        body += '<tr><td>Type</td><td>'+tags_to_label_html(info['tags'])+'</td></tr>'         
        body += '</table>'
        body += '<p class="text-right">'
        body += '<a role="button" class="btn btn-default btn-xs" href="' + chain.config['path-name'] + '/rawtransaction-data/'+str(params[0])+'">JSON</a>'
        body += '<a role="button" class="btn btn-default btn-xs" href="' + chain.config['path-name'] + '/rawtransactionhex-data/'+str(params[0])+'">Hex</a>'
        body += '</p>'
        
        tokens_found=False
        
        output_body=''
        output_body += '<h3>Outputs</h3>'
        output_body += '<table class="table table-striped"><tr>'
        output_body += '<th>Index</th>'
        output_body += '<th>Spent at Input</th>'
        output_body += '<th>Addresses</th>'
        output_body += '<th></th>'
        output_body += '<th>ScriptPubKey</th>'
        output_body += '</tr>'                                
        index=0
        for vout in info['vout']:
            license_vout=False
            if ("issue-license-unit" in vout['tags']) or ("license" in vout['tags']):
                license_vout=True
            td_class=""
            if ('highlight' in nparams) and  nparams['highlight'] == "o"+str(index):
                td_class=' class="highlighted"'
            output_body += '<tr>'
            output_body += '<td '+td_class+'id="o'+str(index)+'">'+str(index)+'</td>'
            if vout['redeem'] is not None:
                output_body += '<td'+td_class+'><a href="' + chain.config['path-name'] + '/transaction/' + vout['redeem']['txid']+'?highlight=i'+str(vout['redeem']['vin'])+'#i'+str(vout['redeem']['vin'])+'">'+vout['redeem']['txid'][0:10]+ ':'+str(vout['redeem']['vin']) +'</a>'+'</td>'                        
            else:
                if "unspendable" in  vout['tags']:               
                    output_body += '<td'+td_class+'>Unspendable</td>'
                else:
                    output_body += '<td'+td_class+'>Not yet spent</td>'
                
            addresses = ''
            if 'addresses' in vout['scriptPubKey']:
                for address in vout['scriptPubKey']['addresses']:
                    address_link = '<a href="' + chain.config['path-name'] + '/address/' + address + '">' + address + '</a>'
                    addresses += '{0}<br/>'.format(address_link)                
                    

            details=''
            if license_vout:
                output_body += '<td'+td_class+'></td>'
                output_body += '<td'+td_class+'>'+tags_to_label_html(vout['tags']).replace("Transfer License","License Token")+'</td>'
                details+=self.vout_licensetoken(chain,vout)            
            else:
                output_body += '<td'+td_class+'>'+addresses+'</td>'
                output_body += '<td'+td_class+'>'+tags_to_label_html(vout['tags']).replace("Transfer Asset","Asset").replace("Native Transfer","Native")+'</td>'
                details+=self.vout_assettransfers(chain,vout)            
                if ('tokens' in vout) and vout['tokens']:
                    tokens_found=True

            if (("issue-asset-details" in vout['tags']) or ("issuemore-asset-details" in vout['tags']) or ("update-asset" in vout['tags'])) and ('issue' in info) :
                details+=self.vout_assetmetadata(chain,info['issue'],str(params[0]))                            
            details+=self.vout_streamitems(chain,vout,str(params[0]),index)            
            if ("create-stream" in vout['tags']) and ('create' in info) :
                details+=self.vout_streammetadata(chain,info['create'],str(params[0]))            
            if 'variable' in vout:
                details+=self.vout_variablemetadata(chain,vout['variable'],str(params[0]))                            
            details+=self.vout_permissions(chain,vout)            
            details+=self.vout_general_data(chain,vout,str(params[0]),index)            
            if len(details) > 0:
                details = '<br/><br/>' + details
            output_body += '<td'+td_class+'>'+decode_script(vout['scriptPubKey']['asm'])+details+'</td>'
            output_body += '</tr>'
            index += 1
            
        output_body += '</table>'
        
        input_body=''
        input_body += '<h3>Inputs</h3>'
        input_body += '<table class="table table-striped"><tr>'
        input_body += '<th>Index</th>'
        input_body += '<th>Previous Output</th>'
        input_body += '<th>Addresses</th>'
        input_body += '<th></th>'
        input_body += '<th>ScriptSig</th>'
        input_body += '</tr>'                                
        
        if tokens_found and len(info['vin'])>5:
            tokens_found=False
            
        index=0
        for vin in info['vin']:
            td_class=""
            if ('highlight' in nparams) and  nparams['highlight'] == "i"+str(index):
                td_class=' class="highlighted"'
            input_body += '<tr>'
            input_body += '<td'+td_class+' id="i'+str(index)+'">'+str(index)+'</td>'
            if 'txid' in vin:                
                input_body += '<td'+td_class+'><a href="' + chain.config['path-name'] + '/transaction/' + vin['txid']+'?highlight=o'+str(vin['vout']) +'#o'+str(vin['vout'])+'">'+vin['txid'][0:10]+ ':'+str(vin['vout']) +'</a>'+'</td>'                        
            else:
                input_body += '<td'+td_class+'>Coinbase</td>'
            addresses = ''
            if 'addresses' in vin:
                for address in vin['addresses']:
                    address_link = '<a href="' + chain.config['path-name'] + '/address/' + address + '">' + address + '</a>'
                    addresses += '{0}<br/>'.format(address_link)                
                    
            details=''
            if license_tx:
                input_body += '<td'+td_class+'>'+'</td>'
                input_body += '<td'+td_class+'>'+tags_to_label_html(vin['tags']).replace("Transfer License","License Token")+'</td>'
                details+=self.vout_licensetoken(chain,vin)            
            else:
                input_body += '<td'+td_class+'>'+addresses+'</td>'
                input_body += '<td'+td_class+'>'+tags_to_label_html(vin['tags']).replace("Transfer Asset","Asset").replace("Native Transfer","Native")+'</td>'
                assets_vin=vin
                if tokens_found and ('txid' in vin):
                    assets_response=chain.request("getrawtransaction",[vin['txid'],1])
                    if assets_response['result'] is not None:                        
                        assets_info=assets_response['result']
                        if vin['vout'] < len(assets_info['vout']):
                            assets_vin=assets_info['vout'][vin['vout']]                    
                details+=self.vout_assettransfers(chain,assets_vin)            
            if 'scriptSig' in vin:                
                input_body += '<td'+td_class+'>'+decode_script(vin['scriptSig']['asm'])+details+'</td>'
            else:
                input_body += '<td'+td_class+'>'+vin['coinbase']+'</td>'
            input_body += '</tr>'
            index += 1
            
        input_body += '</table>'
        
        body += input_body
        body += output_body
        
        return self.standard_response(body)

    def vout_licensetoken(self,chain,vout):
        if 'assets' not in vout:
            return ''
        if len(vout['assets']) == 0:
            return ''
        result='<div style="height:5px;"></div><div class="panel panel-default panel-success"><div class="panel-body" style="">'
        entity_name=vout['assets'][0]['name']
        result += "Token of " + entity_name
        result+='</div></div>'
        return result

    def vout_assettransfers(self,chain,vout):
        if 'assets' not in vout:
            return ''
        if len(vout['assets']) == 0:
            return ''
            
        result='<div style="height:5px;"></div><div class="panel panel-default panel-success"><div class="panel-body" style="">'
        first_row=True
        
        for p in range(2):
            for asset in vout['assets']:
                if ((p==0) and (asset['issuetxid'] is None)) or ((p!=0) and (asset['issuetxid'] is not None)):
                    if not first_row:
                        result += '<br/>'
                    first_row=False
                    entity_quoted=asset['issuetxid'] 
                    if ('name' in asset) and (asset['name'] is not None) and (len(asset['name']) > 0):                
                        entity_quoted=parse.quote_plus(asset['name'])
                        entity_name=asset['name']
                    else:
                        entity_name="with no name"
                    
                    asset_link="Native Currency"
                    if entity_quoted is not None:
                        asset_link='<a href="' + chain.config['path-name'] + '/asset/' + entity_quoted + '">' + entity_name + '</a>'
                    
                    token_str=''
                    if ('token' in asset) and (asset['token'] is not None):
                        vout['tokens']=True
                        token_str=' (token ' + asset['token'] + ')'
                    units='units'
                    if asset['qty'] == 1:
                        units='unit'
                    if 'type' in asset:
                        if asset['type'] == "issuefirst":
                            result+="Issue " + str(asset['qty']) + " " + units + " of new asset " + asset_link
                        elif asset['type'] == "issuemore":
                            result+="Issue " + str(asset['qty']) + " more " + units + " of asset " + asset_link + token_str
                        elif asset['type'] == "issuemore+transfer":
                            result+="Transfer and issue " + str(asset['qty']) + " more " + units + " of asset " + asset_link + token_str
                        elif asset['type'] == "transfer":
                            result+=str(asset['qty']) + " " + units + " of asset " + asset_link + token_str
                    else:
                        if entity_quoted is not None:
                            result+=str(asset['qty']) + " " + units + " of asset " + asset_link + token_str
                        else:
                            result+=str(asset['qty']) + " " + units + " of " + asset_link + token_str
                    
                
        
        result+='</div></div>'
        return result                        
        
        
    def vout_assetmetadata(self,chain,info,txid):
        entity_quoted=txid 
        if 'issuetxid' in info:
            entity_quoted=info['issuetxid'] 
                    
        if ('name' in info) and (len(info['name']) > 0):                
            entity_quoted=parse.quote_plus(info['name'])
            entity_name=info['name']
        else:
            entity_name="No name"
                        
        entity_link='<a href="' + chain.config['path-name'] + '/asset/' + entity_quoted + '">' + entity_name + '</a>'
            
        result='<table class="table table-bordered table-condensed inner-table">'
        if info['type'] == "issuefirst":
            result += '<tr><td>Name</td><td>'+entity_link+'</td></tr>'        
            if "restrict" in info:
                restrict = info["restrict"]
            else:
                restrict = {}
            restrict_str = ', '.join(k for k, v in restrict.items() if v)
            if restrict_str == '':
                restrict_str="None"
            open_str=str(info['open'])
            can_open=False
            can_close=False
            if ("canopen" in info) and info['canopen']:
                can_open=True
            if ("canclose" in info) and info['canclose']:
                can_close=True
            if can_open:
                if can_close:
                    open_str += ' (can open and close)'
                else:
                    open_str += ' (can open)'
            else:
                if can_close:
                    open_str += ' (can close)'
            result += '<tr><td>Open</td><td>'+open_str+'</td></tr>'        
            result += '<tr><td>Restrict</td><td>'+restrict_str+' <a href="' + chain.config['path-name'] + '/assetpermissions/' + entity_quoted + '">(view permissions)</a></td></tr>'        
            result += '<tr><td>Multiple</td><td>'+str(info['multiple'])+'</td></tr>'        
            result += '<tr><td>Units</td><td>'+str(1/info['multiple'])+'</td></tr>'        
            limits=[]
            if ("totallimit" in info) and (info['totallimit'] is not None):
                limits.append(str(info['totallimit']))
            if ("issuelimit" in info) and (info['issuelimit'] is not None):
                limits.append(str(info['issuelimit']) + " per issue")
            limits_str = ' total, '.join(limits)
            if limits_str == '':
                limits_str="None"
            result += '<tr><td>Limit</td><td>'+limits_str+'</td></tr>'        
            fungible_str=str(True)
            if ("fungible" in info):
                fungible_str=str(info['fungible'])
            result += '<tr><td>NFT Token </td><td>'+fungible_str+'</td></tr>'                        
        else:
            result += '<tr><td>Asset</td><td>'+entity_link+'</td></tr>'        
        details=info['details']
        if (type(details) is OrderedDict) or (type(details) is dict):
            details=json.dumps(info['details'])
        result += '<tr><td>Details</td><td>'+str(details)+'</td></tr>'        
        
        result+='</table>'
        return result                                
        
    def vout_variablemetadata(self,chain,info,txid):
        entity_quoted=txid 
        if 'createtxid' in info:
            entity_quoted=info['createtxid'] 
                    
        if ('name' in info) and (len(info['name']) > 0):                
            entity_quoted=parse.quote_plus(info['name'])
            entity_name=info['name']
        else:
            entity_name="Variable with txid " + entity_quoted
                        
        entity_link=entity_name
            
        result='<table class="table table-bordered table-condensed inner-table">'
        result += '<tr><td>Variable</td><td>'+entity_link+'</td></tr>'        
        value=json.dumps(info['value'])
        result += '<tr><td>Value</td><td>'+str(value)+'</td></tr>'        
        
        result+='</table>'
        return result                                
        
    def vout_streammetadata(self,chain,info,txid):
        entity_quoted=txid 
        if 'createtxid' in info:
            entity_quoted=info['issuetxid'] 
        
        if ('name' in info) and (len(info['name']) > 0):                
            entity_quoted=parse.quote_plus(info['name'])
            entity_name=info['name']
        else:
            entity_name="No name"
                        
        entity_link='<a href="' + chain.config['path-name'] + '/stream/' + entity_quoted + '">' + entity_name + '</a>'
        
        result='<table class="table table-bordered table-condensed inner-table">'
        result += '<tr><td>Name</td><td>'+entity_link+'</td></tr>'        
        if "restrict" in info:
            restrict = info["restrict"]
        else:
            restrict = {"write": info["open"]}
        restrict_str = ', '.join(k for k, v in restrict.items() if v)
        if restrict_str == '':
            restrict_str="None"
        result += '<tr><td>Restrict</td><td>'+restrict_str+' <a href="' + chain.config['path-name'] + '/streampermissions/' + entity_quoted + '">(view permissions)</a></td></tr>'        
        if "salted" in info:
            result += '<tr><td>Salted</td><td>'+str(info['salted'])+'</td></tr>'        
        
        details=info['details']
        if (type(details) is OrderedDict) or (type(details) is dict):
            details=json.dumps(info['details'])
        result += '<tr><td>Details</td><td>'+str(details)+'</td></tr>'        
        
        result+='</table>'
        return result                                
        
        
    def vout_streamitems(self,chain,vout,txid,index):
        if 'items' not in vout:
            return ''
        if len(vout['items']) == 0:
            return ''
            
        item=vout['items'][0]  
        
        if item['type'] != "stream":
            return ''
            
        entity_quoted=item['createtxid'] 
                    
        if ('name' in item) and (len(item['name']) > 0):                
            entity_quoted=parse.quote_plus(item['name'])
            entity_name=item['name']
        else:
            entity_name="No name"
            
        entity_link='<a href="' + chain.config['path-name'] + '/stream/' + entity_quoted + '">' + entity_name + '</a>'
        
        keys = []
        if 'key' in item:
            keys = [item['key']]
        else: 
            keys = item['keys']

        prefix = chain.config['path-name'] + '/keyitems/' + entity_quoted
        keylinks = ['<a href="{0}/{1}">{2}</a>'.format(prefix, parse.quote_plus(key),key) for key in keys]
        keyshtml = ', '.join(keylinks)
        # If list is too long, display only first few keys, and enable a popover with the full list
        key_limit = 5
        if len(keylinks) >= key_limit:
            keyshtml = '{}, <span class="ellipses" data-toggle="popover" data-content="{}">...</span>'.format(
                ', '.join(keylinks[:key_limit]), escape(', '.join(keylinks), quote=True))

        data_ref = '/' + chain.config['path-name'] + '/txoutdata-data/' + txid + '/' + str(index)
        data_html=''
        if not item['offchain']:
            data = item['data']
            data_html=self.general_data_html(chain,data,txid,index)
        else:
            data_html = '<a href="' + data_ref + '" title="Click to show all data">Offchain data</a>'
            
        result='<table class="table table-bordered table-condensed">'
        result+='<tr><td>Stream</td><td>' + entity_link + '</td></tr>'
        result+='<tr><td>Keys</td><td>' + keyshtml + '</td></tr>'
        result+='<tr><td>Data</td><td>' + data_html + '</td></tr>'
        result+='</table>'
        return result                                
        
    def vout_permissions(self,chain,vout):
        if 'permissions' not in vout:
            return ''
        if len(vout['permissions']) == 0:
            return ''
        
        result='<div style="height:5px;"></div><div class="panel panel-default panel-success"><div class="panel-body" style="">'
        
        first_row=True
        for grant in vout['permissions']:
            if not first_row:
                result += '<br/>'
            first_row=False
            row="grant "
            if grant['startblock'] >= grant['endblock']:
                row="revoke "
            
            entity_type=None
            if grant['for'] is not None:
                entity_quoted=''
                entity_type=grant['for']['type']     
                if ('name' in grant['for']) and (len(grant['for']['name']) > 0):                
                    entity_quoted=parse.quote_plus(grant['for']['name'])
                    entity_name=grant['for']['name']
                    entity_link='<a href="' + chain.config['path-name'] + '/'+entity_type+'/' + entity_quoted + '">' + entity_name + '</a>'
                else:
                    entity_name="with no name"
                    entity_link=entity_name
                
                row+="permission for "
                row+=entity_type + " " + entity_link               
            else:
                row+="global permission "
                
            if entity_type is not None:
                if entity_type == "stream":
                    allowed_permissions=ALLOWED_PERMISSIONS_STREAM.copy()
                if entity_type == "asset":
                    allowed_permissions=ALLOWED_PERMISSIONS_ASSET.copy()
                if entity_type == "variable":
                    allowed_permissions=ALLOWED_PERMISSIONS_VARIABLE.copy()
                if entity_type == "library":
                    allowed_permissions=ALLOWED_PERMISSIONS_LIBRARY.copy()
            else:
                allowed_permissions=ALLOWED_PERMISSIONS_GLOBAL.copy()
            
            permissions=[]
            for p in allowed_permissions:
                if (p in grant) and grant[p]:
                    permissions.append(p)
            if 'custom' in grant:
                for p in grant['custom']:
                    permissions.append(p)
            
            if len(permissions) > 0: 
                row += " for " + ', '.join(permissions)
              
            result += row              
            
                
        result+='</div></div>'
        
        return result                                
        
    def vout_general_data(self,chain,info,txid,vout):
        if 'data' not in info:
            return ''
        if len(info['data']) == 0:
            return ''
                
        result='<div style="height:5px;"></div><div class="panel panel-default panel-success"><div class="panel-body" style="">'
        htmls=[]
        for d in info['data']:
            htmls.append(self.general_data_html(chain,d,txid,vout))
        result+='<br/>'.join(htmls)
        result+='</div></div>'
        
        return result                                
        
                        
        
    def general_data_html(self, chain,data,txid,vout):
        
        data_ref = chain.config['path-name'] + '/txoutdata-data/' + txid + '/' + str(vout)
        result=''
        printdata = False
        mydata = None
        if (type(data) is OrderedDict) or (type(data) is dict):
            if 'text' in data:
                mydata = data['text']
                printdata = True
            elif 'json' in data:
                mydata = json.dumps(data['json'],indent=4)
                printdata = True
            else:
                mydata = 'Too large to show'
                vout = data['vout']                
        else:
            mydata = data
            printdata = True
            

        if printdata:
            
            result = mydata
            
            size = len(result)
            result = escape(result[:MAX_SHOWN_DATA], quote=True)
            if size > MAX_SHOWN_DATA:
                result += '<span class="ellipses" data-toggle="popover" data-trigger="hover" data-content=" '+escape(mydata, quote=True)+' ">...</span>'        
             
        else:
            result = '<a href="' + data_ref + '" title="Click to show all data">Too large to show</a>'
        
        return result



