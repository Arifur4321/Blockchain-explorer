from dataclasses import dataclass
from re import sub
from turtle import color
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
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String
from reportlab.platypus import SimpleDocTemplate, Paragraph
from flask import Flask, send_file
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import HorizontalBarChart, VerticalBarChart
from reportlab.lib.pagesizes import A4


def pdf_generator_dashboard(info, analytics, app_instance_path):
        
        
        def add_legend(draw_obj, chart, data):
            legend = Legend()
            legend.alignment = 'right'
            legend.x = 480
            legend.y = 420
            legend.columnMaximum = 14
            legend.fontName = 'Helvetica'
            legend.colorNamePairs = Auto(obj=chart)
            draw_obj.add(legend)
#pie chart
        def pie_chart_with_legend():

            pie = Pie()

            sliceColors = ['#3182BD', '#6BAED6', '#9ECAE1', '#C6DBEF', '#E6550D', '#FD8D3C', '#FDAE6B', '#FDD0A2', '#31A354', '#74C476', '#A1D99B', '#C7E9C0', '#756BB1', '#9E9AC8']
            
            counter = 0

            data = []

            labels = []

            for subject in analytics:
                for k, v in subject['dataForPieChart'].items():

                    labels.append(k) 

                    pie.slices[counter].fillColor = colors.toColor(sliceColors[counter])

                    data.append(v)

                    counter += 1
                    
            
            drawing = Drawing(width=500, height=400)
            pie.sideLabels = 0
            pie.slices.fontSize = 0
            pie.x = 90
            pie.y = 75
            pie.width = 350
            pie.height = 350
            pie.data = data
            pie.slices.strokeWidth = 0.5
            pie.direction = 'anticlockwise'
            pie.startAngle = 360
            pie.labels = labels
            pie.slices.strokeColor = colors.white
            drawing.add(pie)
            add_legend(drawing, pie, data)
            return drawing
#bar chart
        def make_drawing():

            drawing = Drawing(450, 230)


            data = [
                (info['blocks'], 
                info['transactions'],
                info['assets'])
                ]

            bc = VerticalBarChart()
    
            bc.height = 230
            bc.width = 400
            bc.valueAxis.valueMax = info['transactions'] * 1.05
            bc.bars.strokeWidth = 0.1
            bc.barWidth = 5.5
            bc.data = data
            bc.x = 188
            bc.y = -10
            bc.strokeColor = colors.toColor('#E5E5E5')
            bc.bars[0].fillColor = colors.toColor("#00008B")
            bc.valueAxis.valueMin = 0
            bc.valueAxis.labels.fontName = 'Helvetica'
            bc.categoryAxis.labelAxisMode = 'low'
            bc.categoryAxis.labels.boxAnchor = 'n'
            bc.categoryAxis.labels.textAnchor = 'middle'
            bc.categoryAxis.labels.dx = -15
            bc.categoryAxis.labels.fontName = 'Helvetica'
            bc.categoryAxis.categoryNames = ['          Blocchi', '          Transazioni', '          Dettagli Transazioni']


            drawing.add(bc)
            return drawing

     
        filename ="report.pdf"

        import os

        header_path=os.path.join(app_instance_path, os.path.normpath('static/img/headerupdated3.png'))
        whitespace_path = os.path.join(app_instance_path, os.path.normpath('static/img/whitespace.JPG'))
        dashboard_sections_headers = os.path.join(app_instance_path, os.path.normpath('static/img/dashboardssectionsheaders.png'))
        dashboard_barchart_header = os.path.join(app_instance_path, os.path.normpath('static/img/barchartheader.png'))
        dashboard_analytics_header = os.path.join(app_instance_path, os.path.normpath('static/img/analyticsheader.png'))
        dashboard_piechart_header =os.path.join(app_instance_path, os.path.normpath('static/img/dashboardpiechartheader.png'))
        dashboard_header =os.path.join(app_instance_path, os.path.normpath('static/img/dashboardpdfheader.png'))

        doc = SimpleDocTemplate( filename, pagesize=A3, rightMargin=20,leftMargin=20, topMargin=20,bottomMargin=30 )
        
        im1 = Image(dashboard_header, 14.5*inch, 0.45*inch)
        im2 = Image(header_path, 14.1*inch, 0.7*inch )
        im3 = Image(whitespace_path, 0.5*inch, 0.5*inch )
        im4 = Image(dashboard_sections_headers, 14.1*inch, 0.35*inch)
        im5 = Image(dashboard_piechart_header, 14.1*inch, 0.45*inch)
        im6 = Image(dashboard_barchart_header, 2.9*inch, 0.41*inch)
        im7 = Image(dashboard_analytics_header, 1.7*inch, 0.4*inch)

       
        data = [
        ["Stato", "Nome Nodo", "Blocchi", "Transazioni", "Dettaglio Transazioni", "Data", "Indrizzi"]
        ]
        temp = []
           
            
        temp.append("Connected")
        temp.append(str(info['chainname']))
        temp.append(str(info['blocks'] + 1)) 
        temp.append(str(info['transactions']))
        temp.append(str(info['assets']))
        temp.append(str(info['streams']))
        temp.append(str(info['addresses'])) 
       
        data.append(temp)

      # Configure style and word wrap
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, s) for cell in row] for row in data]
            
        table = Table(data2,repeatRows=1, colWidths=(None, None, None, None,None, None,None))        
        style = TableStyle([
                            ('BACKGROUND', (0,0), (6,0),  '#dedede' ),
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

        dataAnalytics = []

        analyticsHeaders = []

        counter = 0

        for index, subject in enumerate(analytics):
            if index == 0: 
                analyticsHeaders.append('  ' + subject['title'])
            else:
                analyticsHeaders.append('       ' + subject['title'])

            if len(subject['data']) >= len(analytics[counter]['data']):
                counter = index

        dataAnalytics.append(analyticsHeaders)

        analyticsRow1 = ['   Nuovi Documenti: ' + str(analytics[0]['data']['Nuovi Documenti']), '         Cambio Stato Fascicolo: ' +  str(analytics[1]['data']['Cambio Stato Fascicolo']), '         Nuovi Messaggi: ' +  str(analytics[2]['data']['Nuovi Messaggi']), '         Nuovi Alert: ' +  str(analytics[3]['data']['Nuovi Alert'])]
        analyticsRow2 = ['   Documenti Visualizzati: ' + str(analytics[0]['data']['Documenti Visualizzati']), '         Fascicoli Nuovo Scoring: ' +  str(analytics[1]['data']['Fascicoli Nuovo Scoring']), '         Messaggi Eliminati: ' +  str(analytics[2]['data']['Messaggi Eliminati']), '         Alert Eliminati: ' +  str(analytics[3]['data']['Alert Eliminati'])]
        analyticsRow3 = ['   Documenti Modificati: ' + str(analytics[0]['data']['Documenti Modificati']), '', '         Messaggi Letti: ' +  str(analytics[2]['data']['Messaggi Letti']), '         Alert Modificati: ' +  str(analytics[3]['data']['Alert Modificati'])]
        analyticsRow4 = ['   Documenti Cancellati: ' + str(analytics[0]['data']['Documenti Cancellati']), '', '         Messaggi Modificati: ' +  str(analytics[2]['data']['Messaggi Modificati']), '         Alert Spenti: ' +  str(analytics[3]['data']['Alert Spenti'])]
        emptyRow = [' ', ' ', ' ', ' ']

        dataAnalytics.append(analyticsRow1)
        dataAnalytics.append(analyticsRow2)
        dataAnalytics.append(analyticsRow3)
        dataAnalytics.append(analyticsRow4)
        dataAnalytics.append(emptyRow)

        analyticsStyle = TableStyle([
                    ('BACKGROUND', (0,0), (4,5),  '#f9f9f9' ),
                    ('TEXTCOLOR', (0,0), (4,0),  '#00008B' ),
                    ('FONTSIZE', (0,0), (4,0), 12),
                    ('INNERGRID', (0, 0), (5, 0), 35, colors.white),
                    ('INNERGRID', (0, 1), (5, 1), 35, colors.white),
                    ('INNERGRID', (0, 2), (5, 2), 35, colors.white),
                    ('INNERGRID', (0, 3), (5, 3), 35, colors.white),
                    ('INNERGRID', (0, 4), (5, 4), 35, colors.white),
                    ('INNERGRID', (0, 5), (5, 5), 35, colors.white)                                        
                    ])

        analyticsTable = Table(dataAnalytics, repeatRows=1, colWidths=(2.3*inch, 2.6*inch, 2.6*inch, 2.3*inch))

        analyticsTable.setStyle(analyticsStyle)

        # 3) Add borders
        ts = TableStyle([])
      
        table.setStyle(ts)
        elems = []
        chart_style = TableStyle([('ALIGN', (0, 0),(-1, -1), 'CENTER'),
                         
                          ('VALIGN', (0, 0), (0, 0), 'CENTER')])
        elems.append(Table([[im2]],
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[0 * inch ], style=chart_style))



        elems.append(Table([[im1]],
            colWidths=[9.2* inch, 8.9*inch, 8*inch],
            rowHeights=[1* inch ], style=chart_style))

        elems.append(table)

        elems.append(Table([[im7]], 
                     colWidths=[2.2* inch, 11.9*inch, 8*inch],
                     rowHeights=[0.8* inch ]))

        elems.append(Table([[im3]], 
                     colWidths=[9.2* inch, 8.9*inch, 8*inch],
                     rowHeights=[0.1* inch ]  ) )

        elems.append(analyticsTable)


        elems.append(Table([[im6]],
                colWidths=[0* inch, 8.9*inch, 8*inch],
                rowHeights=[0.9* inch ], style=chart_style))
        
        barcharts=make_drawing()
        elems.append(barcharts)

        elems.append(Table([[im5]],
            colWidths=[9.2* inch, 8.9*inch, 8*inch],
            rowHeights=[2* inch ], style=chart_style))

        charts=pie_chart_with_legend()
        elems.append(charts)

        doc.build(elems, onFirstPage= addPageNumber, onLaterPages=addPageNumber)  
        
        return send_file(filename, as_attachment=True)

def addPageNumber(canvas, doc):
        page_num = canvas.getPageNumber()
        text = "Page %s" % page_num
        canvas.drawRightString(280*mm, 2*mm, text)    


 