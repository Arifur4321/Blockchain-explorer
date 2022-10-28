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

def pdf_generator_blocks (listBlocksArray ):
        print("arifur listBlocksArray :", listBlocksArray)
        from datetime import datetime
        import os

        # cod = datetime.now()
        # filename = os.path.join(app_instance_path, os.path.normpath( f'reports/Report {str(cod)}.pdf' ))
        # imgpath1 = os.path.join (app_instance_path, os.path.normpath('static/img/LogocassifAi.png'))
        # imgpath2 =os.path.join(app_instance_path, os.path.normpath('static/img/MEdiaticalogo.png'))
        #doc = SimpleDocTemplate( filename.name, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
        imgpath1 = './static/img/LogocassifAi.png'
        imgpath6='./static/img/headerupdated3.png'
        imgpath2 = './static/img/whitespace.JPG'
        filename="reportblocks.pdf"
        doc = SimpleDocTemplate( filename, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
        
        im1 = Image(imgpath1, 1.9*inch, 0.6*inch )
        im2 = Image(imgpath6, 14.1*inch, 0.7*inch )
        im3 = Image(imgpath2, 0.5*inch, 0.5*inch )
    
        data = [
        ["Blocco", "Hash", "Miner", "Data", "Transazioni"]
        ]
        
        for asset in listBlocksArray:
            temp = []
            # details=asset['details']
            ari_dict=json.dumps(asset)
            my_dict = json.loads(ari_dict)
            # nome= asset['name']
            temp.append(str(my_dict[0]['height']))  
            temp.append(str(my_dict[0]['hash']))  
            temp.append(str(my_dict[0]['miner']))  
            temp.append(str(format_time(my_dict[0]['time'])))  
            temp.append(str(my_dict[0]['txcount']))  

            #temp.append(nome.partition('-')[2])

            # if  my_dict['tipo_oprazione'] == "Visualizzazione Documento nel Fascicolo" :
            #         togettime =  my_dict['userName']
            #         temp.append(str(togettime[-19:]))
                        
            # else : 
            #         temp.append(str(nome.partition('-')[2]))

            
            # temp.append(my_dict['tipo_oprazione'])
            # temp.append(my_dict['descrizione'])
            
            # if my_dict['tipo_oprazione'] == "Cambio Stato Fascicolo" :
            #    statocancel= my_dict['statoNew'] 
            #    temp.append(  str(statocancel)  )  
            # elif my_dict['tipo_oprazione'] ==  "Cancellazione Messaggio Fascicolo" :
            #    statocancel= my_dict['statoCancellazione']  
            #    temp.append(  str(statocancel) ) 
            # elif my_dict['tipo_oprazione'] ==  "Nuovo Scoring del Fascicolo" :
            #    statocancel= my_dict['scoreNew']  
            #    temp.append(  str(statocancel) )     
             
            # elif my_dict['tipo_oprazione'] ==  "Visualizzazione Documento nel Fascicolo" :
            #    statocancel= "visualizzato" 
            #    temp.append(  str(statocancel))      
            # elif my_dict['tipo_oprazione'] ==  "Conferma Lettura Messagio nel Fascicolo" :
            #    statocancel=  my_dict['statoLettura']
            #    temp.append(  str(statocancel) )      
            # elif my_dict['tipo_oprazione'] ==  "Spegnimento Alert del Fascicolo" :
            #    statocancel=  my_dict['statoLettura']
            #    temp.append(  str(statocancel))    
                
            # elif my_dict['tipo_oprazione'] ==  "Cancellazione Alert Fascicolo" :
            #    statocancel=  "Ripristinato"
            #    temp.append(  str(statocancel)) 
            
            # elif my_dict['tipo_oprazione'] ==  "Cancellazione Documento nel Fascicolo" :
            #    statocancel=  my_dict['statoDocumento'] 
            #    temp.append(  str(statocancel))   

            # elif my_dict['tipo_oprazione'] ==  "Caricamento Nuovo Documento nel Fascicolo" :
            #    statocancel=  my_dict['descrizioneTipoDoc']   
            #    temp.append(  str(statocancel) )       
            # else :  
            #     statocancel =" "    
            #     temp.append(  str(statocancel)) 
             
            # temp.append("13sTd6nVoFxLJek1Lg3eC9BUno8fEHqZSX") 

            data.append(temp)

      # Configure style and word wrap
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, s) for cell in row] for row in data]
            
        table = Table(data2,repeatRows=1, colWidths=(None, 67*mm, 57*mm, 47*mm,None))        
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
      
        table.setStyle(ts)
        elems = []
        chart_style = TableStyle([('ALIGN', (0, 0),(-1, -1), 'CENTER'),
                         
                          ('VALIGN', (0, 0), (0, 0), 'CENTER')])
        elems.append(Table([[im2 ]],
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[0 * inch ], style=chart_style))

        elems.append(Table([[im3] ], 
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[1* inch ]  ) )
        elems.append(table)


        doc.build(elems, onFirstPage= addPageNumber, onLaterPages=addPageNumber)  
        
        return send_file(filename, as_attachment=True)



def format_time(nTime):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(nTime)))

def addPageNumber(canvas, doc):
        page_num = canvas.getPageNumber()
        text = "Page #%s" % page_num
        canvas.drawRightString(280*mm, 2*mm, text)    
   