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

def pdf_generator_blockdetails (blockToPass, txs, app_instance_path):

        from datetime import datetime
        import os
    
        import tempfile
         
        filename ="report.pdf"
        
            
        header_path=os.path.join(app_instance_path, os.path.normpath('static/img/headerupdated3.png'))
        whitespace_path = os.path.join(app_instance_path, os.path.normpath('static/img/whitespace.JPG'))
        doc = SimpleDocTemplate( filename, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
         

        im2 = Image(header_path, 14.1*inch, 0.7*inch )

        im3 = Image(whitespace_path, 0.5*inch, 0.5*inch )
       
        data = [
        ["Hash",
         "Blocco Precedente",
         "Blocco Successivo", 
         "ID Blocco", 
         "Miner", 
         "Version", 
         "Transaction Merkle Root", 
         "Data",
         "Nonce",
         "Transazioni",
         ]  
        ]

        data1 = [
        ["ID Transazione",
         "Tipologia",
  
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
        asset = blockToPass
        temp = []     
            
        temp.append(str(asset['hash'] ))
        nothing=" "    
        temp.append(str(nothing))
        temp.append(str(asset['nextblockhash']))
        temp.append(str(asset['height']))
        temp.append(str(asset['miner']))
        temp.append(str(asset['version']))
        temp.append(str(asset['merkleroot']))
        temp.append(format_time(asset['time']))
        temp.append(str(asset['nonce']))
        temp.append(str(len(asset['tx'])) )
 
        data.append(temp)     

        temp = []
        temp.append(str(asset['tx'][0]) )
        temp.append("Coinbase")
         
        nothing = "N/A"

        data1.append(temp)    

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

         
            
        table = Table(data2,repeatRows=1, colWidths=(27*mm, 27*mm, 27*mm,27*mm,27*mm, 27*mm,27*mm,27*mm,27*mm,27*mm))    
        table1 = Table(data3,repeatRows=1, colWidths=(None,None)) 
         
        style = TableStyle([
                            ('BACKGROUND', (0,0), (10,0),  '#dedede' ),
                            ('ALIGN',(0, 0), (0, 0),'CENTER'),
                            ('VALIGN',(0, 0), (0, 0),'CENTER'),
                            ('VALIGN',(0, 0), (0, 0),'CENTER'),
                            ('ALIGN',(0, 0), (0, 0),'CENTER'),
                            ('VALIGN',(0, 0), (0, 0),'CENTER'),
                            ])
        table.setStyle(style)
        table1.setStyle(style)
  

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
        
        
        # 3) Add borders
        ts = TableStyle(
            [
            ]
        )
      

        #adding the row color style 
        table.setStyle(ts)
        table1.setStyle(ts)
 
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.alignment = 1
        title = Paragraph("Dettaglio Transazione", title_style)

        elems = []
        
        chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                          ('VALIGN', (0, 0), (-1, -1), 'CENTER')])

        elems.append(Table([[im2]],

                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[0 * inch ], style=chart_style))

        elems.append(Table([[im3]], 
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[1* inch ]  ) )    

        elems.append(table)

        elems.append(Table([[im3]],
                     colWidths=[19.2* inch, 18.9*inch, 18*inch],
                     rowHeights=[1.1 * inch], style=chart_style))

        elems.append(table1)

        elems.append(Table([[im3]], 
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[1* inch ]  ) )
        

        doc.build(elems, onFirstPage= addPageNumber, onLaterPages=addPageNumber)  
        
       
        return send_file(filename, as_attachment=True)

def format_time(nTime):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(nTime)))
def addPageNumber(canvas, doc):
        page_num = canvas.getPageNumber()
        text = "Page #%s" % page_num
        canvas.drawRightString(200*mm, 20*mm, text)    
 