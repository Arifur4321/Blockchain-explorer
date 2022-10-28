from hashlib import new
#from turtle import width
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource
import pandas as pd
from math import pi
from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
from bokeh.models.callbacks import CustomJS
from bokeh import events 
from flask import render_template
from bokeh.models import TextInput

def chartInfoTransazioni(width, height, top):
    top = list(top.split(','))
    legend = ['Blocchi', 'Transazioni', 'Dettagli Transazioni']
    y = [float(value) for value in top]
    source = ColumnDataSource(
        data=dict(
            x=legend,
            y = y
        )
    )

    TOOLTIPS = [
        ("Operazione", "@x"),
        ("Quantità", "@y"),
        #("x", "$index"),
        #("(x,y)", "($x, $y)"),     
    ]
    fig = figure(
                title ="Dati Transazioni",
                x_range = legend, 
                plot_width=int(width), 
                tools="hover",
                tooltips = TOOLTIPS,
                plot_height=int(height),
                toolbar_location=None)
    
    fig.vbar(
        x='x',
        top='y',
        width=0.5,
        bottom=0,
        color='navy',
        source = source,

    )
    fig.title.text = "Dati Transazioni"
    fig.title.align = "center"
    fig.title.text_color = "darkblue"
    fig.title.text_font_size = "25px"
    fig.legend.location = "top_center"

    callback = CustomJS(code="""
    // the event that triggered the callback is cb_obj:
    // The event type determines the relevant attributes
    console.log('Tap event occurred at x-position: ' + cb_obj.x)
    """)   
    mouseEnter = CustomJS(code="console.log('Mouse Enter Event')")
    mouseExit = CustomJS(code="console.log('Mouse Exit Event')")
    fig.circle(legend, y, fill_color="white", size=15)
    fig.js_on_event('tap', callback)
    fig.js_on_event(events.MouseEnter, mouseEnter )
    fig.js_on_event(events.MouseLeave, mouseExit )

    script, div = components(fig)
    return script, div


def pieChart(analytics):

    x = {}

    for subject in analytics:
        for key,value in subject['data'].items():
            x[key] = value

    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'operazione'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(x)]

    p = figure(height=600, width=1000, toolbar_location=None,
            tools="hover", tooltips="@operazione: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='operazione', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    script, div = components(p)
    return script, div


def get_html(values, info, analytics):
    scriptbar, divbar = chartInfoTransazioni(width = 620, height= 300, top = values)
    
    script, div = pieChart(analytics)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    

    html = render_template('home.html', 
        info = info,
        script = script, 
        div = div, 
        js_resources = js_resources, 
        css_resources = css_resources,
        scriptbar=scriptbar, 
        divbar= divbar,        
        filter = HomeHtml(),
        analytics = analytics)


    return html

class HomeHtml(): 
    def __init__(self):
        self.js_scripts = []
        self.filter_data_start = ''
        self.filter_data_fine = ''
        self.filter_user = ''
        self.filter_button = ''
        self.divs = {}
        self.divs['form'] = []

        self.get_form()
    
    def get_form(self):
        self.set_utente()
        self.set_dataInizio()
        self.set_dataFine()
        self.set_button()
    
    def set_utente(self):
        self.filter_user =  TextInput(title = "Utente:")
        self.filter_user.css_classes = ['col-sm-2']
        script, div = components(self.filter_user)
        self.js_scripts.append(script)
        self.divs['form'].append(div)

    def set_dataInizio(self):
        from bokeh.models import DatePicker
        from datetime import datetime
        self.filter_data_start =  DatePicker(title='Data Inizio:')
        self.filter_data_start.css_classes = ['col-sm-2']
        script, div = components(self.filter_data_start)
        self.js_scripts.append(script)
        self.divs['form'].append(div)
    
    def set_dataFine(self):
        from bokeh.models import DatePicker
        self.filter_data_fine =  DatePicker(title='Data Fine:')
        self.filter_data_fine.css_classes = ['col-sm-2']
        script, div = components(self.filter_data_fine)
        self.js_scripts.append(script)
        self.divs['form'].append(div)

    def set_button(self):
        from bokeh.models import Button, CustomJS
        self.button = Button(label="Cerca", button_type="success")
        self.button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))
        self.button.css_classes = ['col-sm-2']
        script, div = components(self.button)
        self.js_scripts.append(script)
        self.divs['form'].append(div)
