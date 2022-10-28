from typing_extensions import Self
from reportlab.lib import colors  
from reportlab.lib.pagesizes import letter, inch  
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle   
import json
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors  
from reportlab.lib.pagesizes import letter, inch  
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle  , Image, PageBreak
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A3, inch, landscape 

from flask import Flask, send_file

#from MediaticaTable import addPageNumber

def pdf_generatordetails (assetToPass, app_instance_path):
    
        #filename = tempfile.NamedTemporaryFile( suffix='.pdf' ) 
        #cod = datetime.now()
        from datetime import datetime
        import os
    
        import tempfile
         
        filename ="report.pdf"
        
        header_path=os.path.join(app_instance_path, os.path.normpath('static/img/headerupdated3.png'))
        whitespace_path = os.path.join(app_instance_path, os.path.normpath('static/img/whitespace.JPG'))
        #doc = SimpleDocTemplate( filename.name, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
        doc = SimpleDocTemplate( filename, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
         
        im2 = Image(header_path, 14.1*inch, 0.7*inch )

        im3 = Image(whitespace_path, 0.5*inch, 0.5*inch )
       
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
        asset = assetToPass
        #for asset in cfg.data_handler.alldetails :
        temp = []
        
        nome= asset['name']
        
            
        temp.append(nome.partition('-')[0] )
            
        temp.append(nome.partition('-')[2])

        details=asset['details']
        ari_dict=json.dumps(details)
        my_dict = json.loads(ari_dict)
 

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

        #for asset in cfg.data_handler.alldetails :
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

        #for asset in cfg.data_handler.alldetails :
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
  
        # for 3nd table 
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
                            ('BACKGROUND', (0,0), (6,0),  '#dedede' ),
                          #  ('TEXTCOLOR',(0,0),(6,0),colors.white),
                            ('ALIGN',(0, 0), (0, 0),'CENTER'),
                            ('VALIGN',(0, 0), (0, 0),'CENTER'),
                            #('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                            ('VALIGN',(0, 0), (0, 0),'CENTER'),
                          #  ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                            ('ALIGN',(0, 0), (0, 0),'CENTER'),
                            ('VALIGN',(0, 0), (0, 0),'CENTER'),
                           # ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                            #('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            #('BOX', (0,0), (-1,-1), 0.25, colors.black),
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
                bc = '#f9f9f9'
            
            ts = TableStyle(
                [('BACKGROUND', (0,i),(-1,i), bc)]
            )
            table.setStyle(ts)
            table1.setStyle(ts)
            table2.setStyle(ts)
        
        # 3) Add borders
        ts = TableStyle(
            [
        # ('BOX',(0,0),(-1,-1),2,colors.white),
          #  ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
          #  ('LINEABOVE',(0,2),(-1,2),2,colors.green),
          #  ('GRID',(0,1),(-1,-1),2,colors.black),
          #('GRID',(0,1),(-1,-1),2,'#f9f9f9'),
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

        elems.append(Table([[im2 ]],

                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[0 * inch ], style=chart_style))

        #title adding in the pdf
        #elems.append(title)  
        elems.append(Table([[im3] ], 
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[1* inch ]  ) )    

        elems.append(table)
        elems.append(Table([[im3]],
                     colWidths=[19.2* inch, 18.9*inch, 18*inch],
                     rowHeights=[1.1 * inch], style=chart_style))
        elems.append(table1)
        elems.append(Table([[im3] ], 
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[1* inch ]  ) )
        elems.append(table2)
        #legend1 = "NFT Token (Non Fungible Token)  NFT Block (aperto per il futuro)  Riferimento Asset (Numero di transazione dell'asset)  Restrizione (Permesso di dettaglio)  Prima Transazione (Dettagli Informazioni sulla transazione)"
        #elems.append(legend1)
        doc.build(elems, onFirstPage= addPageNumber, onLaterPages=addPageNumber)  
        
       
        return send_file(filename, as_attachment=True)


def addPageNumber(canvas, doc):
        page_num = canvas.getPageNumber()
        text = "Page #%s" % page_num
        canvas.drawRightString(200*mm, 20*mm, text)    
 