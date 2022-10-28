from datetime import date
from flask import render_template

def get_html(block, mc, datetime, txs, previous_url):
    html = render_template('block_detail.html', 
        block = block, mc = mc, datetime = datetime, txs = txs, previous_url = previous_url)

    return html