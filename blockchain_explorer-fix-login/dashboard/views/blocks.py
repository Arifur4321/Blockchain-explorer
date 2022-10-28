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

def get_html(listBlocksArray, datetime, previous_url):
    html = render_template('blocks.html', 
        listBlocksArray = listBlocksArray,
        datetime = datetime,
        previous_url = previous_url)

    return html