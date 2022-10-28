# -*- coding: utf-8 -*-

# MultiChain Explorer 2 (c) Coin Sciences Ltd
# All rights reserved under BSD 3-clause license
from itertools import chain
from tkinter import *
from flask import make_response
import io 
import pprint
import pandas as pd

import cfg
from urllib import parse
import json
from collections import OrderedDict
#from cgi import escape
from html import escape
from datetime import datetime
import webbrowser
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from traceback import print_list
from turtle import left, title
from xml.dom.minidom import Document
from reportlab.lib import colors
from reportlab.lib.colors import red
from reportlab.lib.pagesizes import A3, inch, landscape 
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,PageBreak
from reportlab.pdfgen import canvas
import numpy as np
import pandas as pd
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
from MediaticaTable import addPageNumber

import cfg
import pages
import data
import readconf
import utils
from html import escape
import urllib.parse
from reportlab.lib import colors  
from reportlab.lib.pagesizes import letter, inch  
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle  , Image, PageBreak
from reportlab.lib.units import mm

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

#from data import MCEDataHandler

DEFAULT_CONTENT_TYPE = "text/html; charset=utf-8"
DEFAULT_HOMEPAGE = "chains"
DEFAULT_SEARCHPAGE = "search"
DEFAULT_NOTFOUNDPAGE = "notfound"
DEFAULT_CHAINPAGE = "chain"
DEFAULT_DATA_SUFFIX = "-data"



class MCEServer(BaseHTTPRequestHandler):
            
    timeout=2    
    tokenverified = False 
    nok ="True"       
     
    def parse_path(self):
        
        path=self.path
        if len(path) >= 2:
            if (path[0] == '/') and (path[1] == '/'):
                path = path[1:]
                
        self.nparams={}
        parsed_path=path.split('?')
        if len(parsed_path) == 2:
            self.nparams=urllib.parse.parse_qs(parsed_path[-1])
            for k,v in self.nparams.items():
                self.nparams[k]=v[0]

            path=parsed_path[0]
            
#        print(path)
        if path[0] == '/':
            path = path[1:]
        if len(path) > 0:
            if path[-1] == '/':
                path = path[:-1]
        if len(path) == 0:

            path=DEFAULT_HOMEPAGE
        self.params=path.split('/')    
        self.chain=None
        self.handler=None
        self.is_data=False
        if path== "downloadpdf":
            self.pdf_generator()
        if path== "downloadsummarypdf":
            self.pdf_generator2nd()
        if path=="searchboxmainsa":
            self.searchboxmaindo()    

        if path== DEFAULT_HOMEPAGE : 
            myvar = self.checkToken()
            #if not myvar :
            #    tokennotvalid = "The token is not valid or Expired" 
            #    self.content=  tokennotvalid
            #    self.handler= getattr(cfg.tokennotfound, 'handle_connerror', None)
            #else : 


            for chain in cfg.chains:
                if (self.chain is None) and (chain.config["path-name"] == self.params[0]):
                    self.chain=chain
                    self.params=self.params[1:]
                    if len(self.params) == 0:
                        self.params.append(DEFAULT_CHAINPAGE)
            if (len(self.params[0])>len(DEFAULT_DATA_SUFFIX)) and (self.params[0][-len(DEFAULT_DATA_SUFFIX):] == DEFAULT_DATA_SUFFIX):
                self.handler=getattr(cfg.data_handler, 'handle_' + self.params[0][0:-len(DEFAULT_DATA_SUFFIX)].replace('-','_'), None)
            else:
                self.handler=getattr(cfg.page_handler, 'handle_' + self.params[0], None)
                
            if self.handler is not None:
                self.params=self.params[1:]
        else : 
              
            
            for chain in cfg.chains:
                if (self.chain is None) and (chain.config["path-name"] == self.params[0]):
                    self.chain=chain
                    self.params=self.params[1:]
                    if len(self.params) == 0:
                        self.params.append(DEFAULT_CHAINPAGE)
            if (len(self.params[0])>len(DEFAULT_DATA_SUFFIX)) and (self.params[0][-len(DEFAULT_DATA_SUFFIX):] == DEFAULT_DATA_SUFFIX):
                self.handler=getattr(cfg.data_handler, 'handle_' + self.params[0][0:-len(DEFAULT_DATA_SUFFIX)].replace('-','_'), None)
            else:
                self.handler=getattr(cfg.page_handler, 'handle_' + self.params[0], None)
                
            if self.handler is not None:
                self.params=self.params[1:]                   


    def handle_static(self):
        try:
            path="/".join(self.params)
            found = open(cfg.htdocspath + path, "rb")
            import mimetypes
            type, enc = mimetypes.guess_type(path)
            result=found.read()
            found.close();
            return(200, [('Content-type', type or 'text/plain')],result)
        except IOError:
            self.handler=cfg.notfound_handler
            return None
        

    def checkToken(self):
        path = self.path 
        parsedpath = urllib.parse.urlparse(path)
        query = urllib.parse.parse_qs(parsedpath.query)
        token = None 
        try:
            token = query["classifaitoken"][0]
        except:
            return False 
        # i have to implement the token verification here 
       # print(token)
        if token: 
            r = requests.get("http://192.168.99.21:8189/InplaceAPI/InplaceAPI_ValidazioneToken/EseguiValidazioneToken?valoreToken=" + str(token))
            print(r.json()) 
            respond= r.json()
            if respond['ValidazioneOK'] :
                return True  
        return False    

    def searchboxmaindo(self):
        print ("create the search item")  

    def pdf_generator2nd (self):
        print("today method is called " , cfg.data_handler.alldetails)
        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')
        self.send_header('Content-Disposition', 'attachment; filename="DettaglioTransazione.pdf"')
        self.end_headers()
        import tempfile
        filename = tempfile.NamedTemporaryFile( suffix='.pdf' ) 
        imgpath1 = 'LogocassifAi.png'
        im2path = 'Untitled.png'
        imgpath2 = 'MEdiaticalogo.png'

        doc = SimpleDocTemplate( filename.name, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
        im1 = Image(imgpath1, 1.9*inch, 0.6*inch )
        im2 = Image(im2path, 1.9*inch, 0.6*inch )
        im3 = Image(imgpath2, 1.9*inch, 0.5*inch )
       
        data = [
        ["Nome Utente",
         "Data Transazione",
         "Tipo Operazione", 
         "Descrizione ", 
         "ID Fascicolo", 
         "Vecchio Stato", 
         "Nuovo Stato",
         ]  
        ]

        data1 = [
        ["idMessaggioAlert",
         "Nome File Doc",
         "ID Documento", 
         "Descrizione Tipo Doc", 
         "Stato Documento",
         "Prima Transazione", 
         "Riferimento Asset",  
         ]
        ]

        data5 = [
        ["NFT Token Aperto",
         "NFT Token",
         "Issues", 
         "Indrizzo Blockchain", 
         "Numero di Transazioni", 
         "Unita", 
         "Indirizzo User",
         ]
        ]

        for asset in cfg.data_handler.alldetails :
                temp = []
                
                nome= asset['name']
                
                    
                temp.append(nome.partition('-')[0] )
                    
                temp.append(nome.partition('-')[2])

                details=asset['details']
                ari_dict=json.dumps(details)
                my_dict = json.loads(ari_dict)

                inz = cfg.data_handler.alldetails
                ari_d=json.dumps(inz)
                info = json.loads(ari_d)

                temp.append(my_dict['tipo_oprazione'])
                nothing = "N/A"
                tipo_operazione = my_dict['tipo_oprazione']

                cambiostato = "Cambio Stato Fascicolo"
                if tipo_operazione == cambiostato :
                    descrizione = my_dict['descrizione'] 
                    temp.append( str(descrizione)   ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append(str(idFascicolo)   ) 
                    statoOld = my_dict['statoOld']
                    temp.append( str(statoOld)  )      
                    statoNew = my_dict['statoNew'] 
                    temp.append( str(statoNew)  )    
                    
                NuovoScoringFascicolo = "Nuovo Scoring del Fascicolo"
                if tipo_operazione == NuovoScoringFascicolo:
                    descrizione = my_dict['descrizione'] 
                    temp.append( str(descrizione)   )  
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) ) 
                    scoreOld = my_dict['scoreOld']
                    temp.append(str(scoreOld)   )      
                    scoreNew = my_dict['scoreNew'] 
                    temp.append( str(scoreNew)   )   
                    
                CancellazioneAlert = "Cancellazione Alert Fascicolo"
                if tipo_operazione == CancellazioneAlert:  
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))
                     
                CancellazioneMessaggio = "Cancellazione Messaggio Fascicolo"
                if tipo_operazione == CancellazioneMessaggio:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))
                                    
                CaricamentoNuovoDocumento = "Caricamento Nuovo Documento nel Fascicolo"
                if tipo_operazione == CaricamentoNuovoDocumento:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))
                    
                ModificaDocumento = "Modifica Documento nel Fascicolo"
                if tipo_operazione == ModificaDocumento:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))
                

                VisualizzazioneDocumento = "Visualizzazione Documento nel Fascicolo"
                if tipo_operazione == VisualizzazioneDocumento:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))

                CancellazioneDocumento = "Cancellazione Documento nel Fascicolo"
                if tipo_operazione == CancellazioneDocumento:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))
                    
                
                ConfermaLetturaMessagio = "Conferma Lettura Messagio nel Fascicolo"
                if tipo_operazione  == ConfermaLetturaMessagio:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))  
                    
                spegnimentoAlert = "Spegnimento Alert del Fascicolo"
                if tipo_operazione  == spegnimentoAlert:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))
                    
                NuovoMessaggio = "Nuovo Messaggio nel Fascicolo"
                if tipo_operazione  == NuovoMessaggio:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))
                    
                NuovoAlert = "Nuovo Alert nel Fascicolo"
                if tipo_operazione  == NuovoAlert:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing)) 

                    
                ModificaMessaggio = "Modifica Messaggio nel Fascicolo"
                if tipo_operazione  == ModificaMessaggio:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing))    
                
                
                ModificaAlert = "Modifica Alert nel Fascicolo"
                if tipo_operazione  == ModificaAlert:
                    descrizione = my_dict['descrizione'] 
                    temp.append(str(descrizione)  ) 
                    idFascicolo = my_dict['idFascicolo']
                    temp.append( str(idFascicolo) )  
                    temp.append(str(nothing))
                    temp.append(str(nothing)) 
                
                    
                data.append(temp)     

        for asset in cfg.data_handler.alldetails :
                temp = []
                
                nome= asset['name']
                nothing = "N/A"
                tipo_operazione = my_dict['tipo_oprazione']

                cambiostato = "Cambio Stato Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(nothing))
                    temp.append(str( nothing  ))
                    temp.append(str( nothing  ))
                    temp.append(str( nothing  )) 
                    temp.append(str( nothing  ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))
   
                cambiostato = "Nuovo Scoring del Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(nothing))
                    temp.append(str( nothing  ))
                    temp.append(str( nothing  ))
                    temp.append(str( nothing  )) 
                    temp.append(str( nothing  ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))   

                cambiostato = "Caricamento Nuovo Documento nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(nothing))
                    temp.append(str( my_dict['nomeFileDoc'] ))
                    temp.append(str(my_dict['idDocumento']))
                    temp.append(str( my_dict['descrizioneTipoDoc'])) 
                    temp.append(str( nothing  ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref'])) 
 

                cambiostato = "Cancellazione Messaggio Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(my_dict['idMessaggioAlert']))
                    temp.append(str( nothing ))
                    temp.append(str( nothing))
                    temp.append(str(nothing)) 
                    temp.append(str( my_dict['statoCancellazione'] ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))  

                cambiostato = "Visualizzazione Documento nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(nothing))
                    temp.append(str( my_dict['nomeFileDoc'] ))
                    temp.append(str( my_dict['idDocumento']))
                    temp.append(str(my_dict['descrizioneTipoDoc'])) 
                    temp.append(str( nothing ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))    
                 
                cambiostato = "Modifica Documento nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(nothing))
                    temp.append(str( my_dict['nomeFileDoc'] ))
                    temp.append(str( my_dict['idDocumento']))
                    temp.append(str(my_dict['descrizioneTipoDoc'])) 
                    temp.append(str( nothing ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))    

        
                cambiostato = "Cancellazione Documento nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(nothing))
                    temp.append(str( my_dict['nomeFileDoc'] ))
                    temp.append(str( my_dict['idDocumento']))
                    temp.append(str(my_dict['descrizioneTipoDoc'])) 
                    temp.append(str( my_dict['statoDocumento'] ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))  

                cambiostato = "Conferma Lettura Messagio nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(my_dict['idMessaggioAlert']))
                    temp.append(str( nothing ))
                    temp.append(str( nothing))
                    temp.append(str(nothing)) 
                    temp.append(str( my_dict['statoLettura'] ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))    

                cambiostato = "Spegnimento Alert del Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(my_dict['idMessaggioAlert']))
                    temp.append(str( nothing ))
                    temp.append(str( nothing))
                    temp.append(str(nothing)) 
                    temp.append(str( my_dict['statoLettura'] ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))       

                cambiostato = "Nuovo Alert nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(my_dict['idMessaggioAlert']))
                    temp.append(str( nothing ))
                    temp.append(str( nothing))
                    temp.append(str(nothing)) 
                    temp.append(str( nothing ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))

                cambiostato = "Modifica Alert nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(my_dict['idMessaggioAlert']))
                    temp.append(str( nothing ))
                    temp.append(str( nothing))
                    temp.append(str(nothing)) 
                    temp.append(str( nothing ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))   

                cambiostato = "Nuovo Messaggio nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(my_dict['idMessaggioAlert']))
                    temp.append(str( nothing ))
                    temp.append(str( nothing))
                    temp.append(str(nothing)) 
                    temp.append(str( nothing ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))   
 

                cambiostato = "Cancellazione Alert Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(my_dict['idMessaggioAlert']))
                    temp.append(str( nothing ))
                    temp.append(str( nothing))
                    temp.append(str(nothing)) 
                    temp.append(str( my_dict['statoCancellazione'] ))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))  

                cambiostato = "Modifica Messaggio nel Fascicolo"
                if tipo_operazione == cambiostato :
                    temp.append(str(my_dict['idMessaggioAlert']))
                    temp.append(str( nothing ))
                    temp.append(str( nothing))
                    temp.append(str(nothing)) 
                    temp.append(str( nothing))
                    temp.append(str( asset['issuetxid'] ))
                    temp.append(str( asset['assetref']))                    
                 
   
                data1.append(temp)    
 
        for asset in cfg.data_handler.alldetails :
                temp = []
                nome= asset['name']
                NFTTokenAperto = "True"
                NFTToken = "True"
                Issues = "1"
                IndrizzoBlockchain = "19VtPtyCwehcCsnxB5HzcBR3V8sWPSJ2kJ"
                NumeroTransaction = "1"
                Unita = "1"
                IndrizzoUser="1"

                temp.append( str(NFTTokenAperto)  ) 
                temp.append( str(NFTToken)  ) 
                temp.append( str(Issues)  ) 
                temp.append( str(IndrizzoBlockchain)  ) 
                temp.append( str(NumeroTransaction)  ) 
                temp.append( str(Unita)  )
                temp.append( str(IndrizzoUser)  ) 
                data5.append(temp)    

      # Configure style and word wrap
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, s) for cell in row] for row in data]

        # for 2nd table 
        s1 = getSampleStyleSheet()
        s1 = s1["BodyText"]
        s1.wordWrap = 'CJK'
        data3 = [[Paragraph(cell, s1) for cell in row] for row in data1]

        # for 3nd table 
        s2 = getSampleStyleSheet()
        s2 = s2["BodyText"]
        s2.wordWrap = 'CJK'
        data4 = [[Paragraph(cell, s2) for cell in row] for row in data5]
            
        table = Table(data2,repeatRows=1, colWidths=(None, 33*mm, None, 60*mm,45*mm, None,None))    
        table1 = Table(data3,repeatRows=1, colWidths=(33*mm, 40*mm, 33*mm, 67*mm,None, 40*mm,33*mm)) 
        table2 = Table(data4,repeatRows=1, colWidths=(33*mm, 33*mm, 33*mm, 67*mm,45*mm, None,33*mm))   
        style = TableStyle([
                            ('BACKGROUND', (0,0), (6,0), colors.lightsteelblue),
                            ('TEXTCOLOR',(0,0),(6,0),colors.white),
                            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                             ('VALIGN',(0,0),(0,-1),'CENTER'),
                            ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                            ('VALIGN',(0,0),(0,-1),'CENTER'),
                            ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                            ('VALIGN',(0,-1),(-1,-1),'CENTER'),
                            ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                            ])

        table.setStyle(style)
        table1.setStyle(style)
        table2.setStyle(style)

        # 2) Alternate backgroud color

        rowNumb = len(data)
        for i in range(1, rowNumb):
 
            if i % 2 == 0:
                bc = colors.white
            else:
                bc = colors.lightgrey
        
            ts = TableStyle(
                [('BACKGROUND', (0,i),(-1,i), bc)]
            )
            table.setStyle(ts)
            table1.setStyle(ts)
            table2.setStyle(ts)
        
        # 3) Add borders
        ts = TableStyle(
            [
            ('BOX',(0,0),(-1,-1),2,colors.black),

            ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
            ('LINEABOVE',(0,2),(-1,2),2,colors.green),

            ('GRID',(0,1),(-1,-1),2,colors.black),
            ]
        )

        #adding the row color style 
        table.setStyle(ts)
        table1.setStyle(ts)
        table2.setStyle(ts)
        styles = getSampleStyleSheet()
        #title style 
        title_style = styles['Heading1']
        title_style.alignment = 1
        title = Paragraph("Dettaglio Transazione", title_style)

        elems = []
        chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                          ('VALIGN', (0, 0), (-1, -1), 'CENTER')])

        elems.append(Table([[im1,im3]],
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[1.1 * inch], style=chart_style))

        #title adding in the pdf
        elems.append(title)      

        elems.append(table)
        elems.append(Table([[im1,im3]],
                     colWidths=[19.2* inch, 18.9*inch, 18*inch],
                     rowHeights=[1.1 * inch], style=chart_style))
        elems.append(table1)
        elems.append(Table([[im1,im3]],
                     colWidths=[19.2* inch, 18.9*inch, 18*inch],
                     rowHeights=[1.1 * inch], style=chart_style))
        elems.append(table2)
        #legend1 = "NFT Token (Non Fungible Token)  NFT Block (aperto per il futuro)  Riferimento Asset (Numero di transazione dell'asset)  Restrizione (Permesso di dettaglio)  Prima Transazione (Dettagli Informazioni sulla transazione)"
        #elems.append(legend1)
        doc.build(elems, onFirstPage= addPageNumber, onLaterPages=addPageNumber)  
        
        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')
        self.send_header('Content-Disposition', 'attachment; filename="table.pdf"')
        self.end_headers()
        with open(filename.name, 'rb') as file: 
            self.wfile.write(file.read())
 


    def pdf_generator (self):

        print(cfg.data_handler.allresult)

        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')
        self.send_header('Content-Disposition', 'attachment; filename="ClassifAI.pdf"')
        self.end_headers()
        import tempfile
        filename = tempfile.NamedTemporaryFile( suffix='.pdf' ) 
    
        imgpath1 = 'LogocassifAi.png'
        imgpath2 = 'MEdiaticalogo.png'
        doc = SimpleDocTemplate( filename.name, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
        
        im1 = Image(imgpath1, 1.9*inch, 0.6*inch )
        im2 = Image(imgpath1, 1*inch, 1*inch )
        im3 = Image(imgpath2, 1.9*inch, 0.5*inch )
       
        data = [
        ["Nome Utente", "Data Transazione", "Tipo Operazione", "Descrizione ", "Stato", "Blockchain Indirizzo"]
        ]
        
        for asset in cfg.data_handler.allresult:
            temp = []
            
            details=asset['details']
            ari_dict=json.dumps(details)
            my_dict = json.loads(ari_dict)
            nome= asset['name']
            temp.append(nome.partition('-')[0] )  
            #temp.append(nome.partition('-')[2])

            if  my_dict['tipo_oprazione'] ==  "Visualizzazione Documento nel Fascicolo" :
                    togettime =  my_dict['userName']
                    temp.append(str(togettime[-19:]))
                        
            else : 
                    temp.append(str(nome.partition('-')[2]))

            
            temp.append(my_dict['tipo_oprazione'])
            temp.append(my_dict['descrizione'])
            
            if my_dict['tipo_oprazione'] == "Cambio Stato Fascicolo" :
               statocancel= my_dict['statoNew'] 
               temp.append(  str(statocancel)  )  
            elif my_dict['tipo_oprazione'] ==  "Cancellazione Messaggio Fascicolo" :
               statocancel= my_dict['statoCancellazione']  
               temp.append(  str(statocancel) ) 
            elif my_dict['tipo_oprazione'] ==  "Nuovo Scoring del Fascicolo" :
               statocancel= my_dict['scoreNew']  
               temp.append(  str(statocancel) )     
             
            elif my_dict['tipo_oprazione'] ==  "Visualizzazione Documento nel Fascicolo" :
               statocancel= "visualizzato" 
               temp.append(  str(statocancel))      
            elif my_dict['tipo_oprazione'] ==  "Conferma Lettura Messagio nel Fascicolo" :
               statocancel=  my_dict['statoLettura']
               temp.append(  str(statocancel) )      
            elif my_dict['tipo_oprazione'] ==  "Spegnimento Alert del Fascicolo" :
               statocancel=  my_dict['statoLettura']
               temp.append(  str(statocancel))    
                
            elif my_dict['tipo_oprazione'] ==  "Cancellazione Alert Fascicolo" :
               statocancel=  "Ripristinato"
               temp.append(  str(statocancel)) 
            
            elif my_dict['tipo_oprazione'] ==  "Cancellazione Documento nel Fascicolo" :
               statocancel=  my_dict['statoDocumento'] 
               temp.append(  str(statocancel))   

            elif my_dict['tipo_oprazione'] ==  "Caricamento Nuovo Documento nel Fascicolo" :
               statocancel=  my_dict['descrizioneTipoDoc']   
               temp.append(  str(statocancel) )       
            else :  
                statocancel =" "    
                temp.append(  str(statocancel)) 
             
            temp.append(asset['issues'][0]['issuers'][0]) 

            data.append(temp)

      # Configure style and word wrap
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, s) for cell in row] for row in data]
            
        table = Table(data2,repeatRows=1, colWidths=(None, None, None, 67*mm,25*mm, None))        
        style = TableStyle([
                            ('BACKGROUND', (0,0), (6,0), colors.lightsteelblue),
                            ('TEXTCOLOR',(0,0),(6,0),colors.white),
                            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                            ('VALIGN',(0,0),(0,-1),'CENTER'),
                            ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                            ('VALIGN',(0,0),(0,-1),'CENTER'),
                            ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                            ('VALIGN',(0,-1),(-1,-1),'CENTER'),
                            ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                            ])
        table.setStyle(style)

        # 2) Alternate backgroud color
        rowNumb = len(data)
        for i in range(1, rowNumb):
 
            if i % 2 == 0:
                bc = colors.white
            else:
                bc = colors.lightgrey
            
            ts = TableStyle(
                [('BACKGROUND', (0,i),(-1,i), bc)]
            )
            table.setStyle(ts)
        
        # 3) Add borders
        ts = TableStyle(
            [
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
            ('LINEABOVE',(0,2),(-1,2),2,colors.green),
            ('GRID',(0,1),(-1,-1),2,colors.black),
            ]
        )
      
        table.setStyle(ts)
        elems = []
        chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                          ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
        elems.append(Table([[im1,im3]],
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[1.1 * inch], style=chart_style))
        elems.append(table)
        doc.build(elems, onFirstPage= addPageNumber, onLaterPages=addPageNumber)  
        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')
        self.send_header('Content-Disposition', 'attachment; filename="table.pdf"')
        self.end_headers()
        with open(filename.name, 'rb') as file: 
            self.wfile.write(file.read())
                
    def addPageNumber(canvas, doc):
        
        page_num = canvas.getPageNumber()
        text = "Page #%s" % page_num
        canvas.drawRightString(200*mm, 20*mm, text)    
   
    def do_GET(self):
        
        self.parse_path()
        if self.handler is None:
            content=self.handle_static()
        if self.handler is not None:
            print(self.path)
            content=self.handler(self.chain,self.params,self.nparams)
        
        if content is None:
            content=cfg.notfound_handler()
            
        self.send_response(content[0])
        for header in content[1]:
            self.send_header(header[0], header[1])
        self.end_headers()
        #print(content[2])
        try:
            result=content[2]
            size=len(result)
            bytes_written=0
            while bytes_written<size:
                bytes_written += self.wfile.write(result[bytes_written:])
        except IOError:
            self.handler=cfg.connerror_handler
            return None
            
    def log_message(self, format, *args):
        return
        
    def log_message(self, format, *args):
        return
   
def start():
    
    cfg.htdocspath=utils.full_dir_name(utils.file_dir_name(__file__)) + "/htdocs/"        
    cfg.page_handler=pages.MCEPageHandler()
    cfg.data_handler=data.MCEDataHandler()
    cfg.notfound_handler=getattr(cfg.page_handler, 'handle_notfound', None)
    cfg.connerror_handler=getattr(cfg.page_handler, 'handle_connerror', None)

    for i in range(0,len(cfg.chains)):
        cfg.chains[i].config["display-name"]=escape(cfg.chains[i].config["name"])
        if cfg.chains[i].config["path-name"] in [DEFAULT_HOMEPAGE,DEFAULT_SEARCHPAGE,DEFAULT_NOTFOUNDPAGE,DEFAULT_CHAINPAGE]:
            cfg.chains[i].config["path-name"] = cfg.chains[i].config["path-name"] + '-' + cfg.chains[i].config["path-ini-name"]
            cfg.chains[i].config["display-name"]=escape(cfg.chains[i].config["name"]) + '(' + escape(cfg.chains[i].config["ini-name"]) + ')'
        else:            
            for j in range(0,i):
                if cfg.chains[i].config["path-name"] == cfg.chains[j].config["path-name"]:
                    cfg.chains[i].config["path-name"] = cfg.chains[i].config["path-name"] + '-' + cfg.chains[i].config["path-ini-name"]
                    cfg.chains[i].config["display-name"]=escape(cfg.chains[i].config["name"]) + '(' + escape(cfg.chains[i].config["ini-name"]) + ')'
                
    #print(cfg.chains[i].config)   
    hostName = "localhost"
    if not readconf.is_missing(cfg.settings['main'],'host'):
        hostName=cfg.settings['main']['host']
        
    serverPort = int(cfg.settings['main']['port'])
    try:
        webServer = HTTPServer((hostName, serverPort), MCEServer)        
    except Exception as e: 
        message="Failed to start web server: " + str(e)
        utils.log_error(message)
        print(message)
        return False        
            
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    

    webServer.server_close()
    utils.log_write("Web server stopped")
    
    return True


