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

def pdf_generator_streams (streamsdata, restrictions, app_instance_path):
      
        filename ="report.pdf"

        import os
        
        header_path=os.path.join(app_instance_path, os.path.normpath('static/img/headerupdated3.png'))
        whitespace_path = os.path.join(app_instance_path, os.path.normpath('static/img/whitespace.JPG'))
        doc = SimpleDocTemplate( filename, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
        
        header = Image(header_path, 14.1*inch, 0.7*inch )
        whitespace = Image(whitespace_path, 0.5*inch, 0.5*inch )
       
        data = [
        ["Nome", "Oggetti PDF", "Chiavi", "Editore", "Restrizioni", "Dettagli Creatore", "Transazione di Creazione"]
        ]

        for index,stream in enumerate(streamsdata):
            temp = []
            dict = json.dumps(stream)
            restrict_dict = json.dumps(restrictions[index])

            stream_dict_loaded = json.loads(dict)
            restrict_dict_loaded = json.loads(restrict_dict)

            temp.append(str(stream_dict_loaded['name']))
            temp.append(str(stream_dict_loaded['items']))
            temp.append(str(stream_dict_loaded['keys']))
            temp.append(str(stream_dict_loaded['publishers']))
            temp.append(str(restrict_dict_loaded))
            temp.append('13sTd6nVoFxLJek1Lg3eC9BUno8fEHqZSX')
            temp.append(str(stream_dict_loaded['createtxid']))
            
            data.append(temp)

      # Configure style and word wrap
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, s) for cell in row] for row in data]
            
        table = Table(data2,repeatRows=1, colWidths=(None, None, None, None, None, None, None ))        
        style = TableStyle([
                            ('BACKGROUND', (0,0), (7,0),  '#dedede' ),
                            ('ALIGN',(0, 0), (0, 0),'CENTER'),
                            ('VALIGN',(0, 0), (0, 0),'CENTER'),
                            ('VALIGN',(0, 0), (0, 0),'CENTER'),
                            ('ALIGN',(0, 0), (0, 0),'CENTER'),
                            ('VALIGN',(0, 0), (0, 0),'CENTER')
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
        
        ts = TableStyle(
            [
            ]
        )
      
        table.setStyle(ts)
        elems = []
        chart_style = TableStyle([('ALIGN', (0, 0),(-1, -1), 'CENTER'),
                         
                          ('VALIGN', (0, 0), (0, 0), 'CENTER')])
        elems.append(Table([[header]],
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[0 * inch ], style=chart_style))

        elems.append(Table([[whitespace] ], 
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[1* inch ]  ) )
        elems.append(table)


        doc.build(elems, onFirstPage= addPageNumber, onLaterPages=addPageNumber)  
        
        return send_file(filename, as_attachment=True)



def addPageNumber(canvas, doc):
        page_num = canvas.getPageNumber()
        text = "Page %s" % page_num
        canvas.drawRightString(280*mm, 2*mm, text)    


def format_time(nTime):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(nTime)))