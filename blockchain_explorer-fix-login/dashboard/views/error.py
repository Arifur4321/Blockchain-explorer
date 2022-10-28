from flask import render_template

def get_html(previous_url):
    html = render_template('error.html', previous_url = previous_url)

    return html