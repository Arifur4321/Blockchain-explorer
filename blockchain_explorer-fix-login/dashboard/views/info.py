from flask import render_template

def get_html(general_information, blockchain_parameters, previous_url):
    html = render_template('info.html',
    general_information = general_information,
    blockchain_parameters = blockchain_parameters,
    previous_url = previous_url)

    return html