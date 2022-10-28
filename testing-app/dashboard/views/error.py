from flask import render_template

def get_html():
    html = render_template('error.html')

    return html