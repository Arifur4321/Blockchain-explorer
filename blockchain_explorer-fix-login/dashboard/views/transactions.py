from flask import render_template

def get_html(listTransactions, datetime, previous_url):
    html = render_template('transactions.html', 
        listTransactions = listTransactions,
        datetime = datetime,
        previous_url = previous_url)

    return html