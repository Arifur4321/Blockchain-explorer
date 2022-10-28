from flask import render_template

def get_html(listAddresses, previous_url):
    html = render_template('addresses.html', 
        listAddresses = listAddresses,
        previous_url = previous_url)

    return html