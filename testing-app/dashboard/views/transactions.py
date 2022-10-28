from flask import render_template

def get_html(listTransactions, datetime):
    html = render_template('transactions.html', 
        listTransactions = listTransactions,
        datetime = datetime)

    return html