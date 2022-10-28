from audioop import mul
import imp
import json
import re
import string
#from turtle import width
from flask import Flask, render_template, redirect, Response, request
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.palettes import Spectral6
import blochchain_interface
import pandas as pd
from math import pi
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models.callbacks import CustomJS
from bokeh import events
from datetime import datetime
from helpers import assets_filter, blocks_filter
from views import home

multichain = blochchain_interface.Multichain(mode='dev')

app = Flask(__name__)

# from flask_wkhtmltopdf import Wkhtmltopdf

# wkhtmltopdf = Wkhtmltopdf(app )


def get_datails_from_username(username, list_assets):
    #detail = {'value': 0, 'userName': 'Damiano--19/09/2022 10:24:20', 'idFascicolo': 'kjgsdfkjsafd', 'statoOld': '27', 'statoNew': '98', 'tipo_oprazione': 'Cambio Stato Fascicolo', 'descrizione': 'testin putpose'}
    return [asset['details'] for asset in list_assets if asset['details']['userName'].split('--')[0] == username ]

@app.route('/')
def index(): 
    info = multichain.client.getinfo().as_dict()
  
    listAssets = multichain.client.listassets()
    #print ( listAssets[0].keys())
    '''
        dict_keys(['name', 'issuetxid', 'assetref', 'multiple', 'units', 'open', 'restrict', 'fungible', 
        'canopen', 'canclose', 'totallimit', 'issuelimit', 'details', 'issuecount', 'issueqty', 'issueraw', 
        'subscribed', 'synchronized', 'transactions', 'confirmed'])
    '''

    #print ( listAssets[0]['details'])
    detail = {'value': 0, 'userName': 'Damiano--19/09/2022 10:24:20', 'idFascicolo': 'kjgsdfkjsafd', 'statoOld': '27', 'statoNew': '98', 'tipo_oprazione': 'Cambio Stato Fascicolo', 'descrizione': 'testin putpose'}
    #for asset in listAssets:
    #    print(asset['details']['tipo_oprazione'] )
    #print(f"Quantità di Operazioni fatte da Damiano:  {len(get_datails_from_username('Damiano', list_assets=listAssets))}")
    #print(f"Quantità di Operazioni fatte da Arifur:  {len(get_datails_from_username('Arifur', list_assets=listAssets))}")
    #print(f"Quantità di Operazioni fatte da SiteAdminUAT:  {len(get_datails_from_username('SiteAdminUAT', list_assets=listAssets))}")
   
    
    values = f"{info['blocks']},{info['transactions']},{info['assets']}"
    
    cambioStatoFascicolo = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Cambio Stato Fascicolo' ])
    cancellazioneMessaggio = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Cancellazione Messaggio Fascicolo' ])
    cancellazioneAlert = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Cancellazione Alert Fascicolo' ])
    cancellazioneDocumento = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Cancellazione Documento nel Fascicolo' ])
    caricamentoNuovoDocumento = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Caricamento Nuovo Documento nel Fascicolo' ])
    modificaDocumento = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Modifica Documento nel Fascicolo' ])
    visualizzazioneDocumento = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Visualizzazione Documento nel Fascicolo' ])
    nuovoMessaggio = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Nuovo Messaggio nel Fascicolo' ])
    nuovoAlert = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Nuovo Alert nel Fascicolo' ])
    modificaMessaggio = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Modifica Messaggio nel Fascicolo' ])
    modificaAlert = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Modifica Alert nel Fascicolo' ])
    nuovoScoringFascicolo = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Nuovo Scoring del Fascicolo' ])
    spegnimentoAlert = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Spegnimento Alert del Fascicolo' ])
    confermaLetturaMessaggio = len ([asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == 'Conferma Lettura Messagio nel Fascicolo' ])


    analytics = [
                    {"title": "Documenti", "data": {"Nuovi Documenti":caricamentoNuovoDocumento,
                        "Documenti Vizualizzati":visualizzazioneDocumento,
                        "Documenti Modificati":modificaDocumento,
                        "Messaggi Cancellati":cancellazioneDocumento}},

                    {"title": "Fascicoli", "data": {"Cambio Stato Fascicolo": cambioStatoFascicolo,
                        "Fascicoli Nuovo Scoring": nuovoScoringFascicolo}},

                    {"title": "Messaggi", "data": {"Nuovi Messaggi":nuovoMessaggio,
                        "Messagi Eliminati": cancellazioneMessaggio,
                        "Messaggi Letti":confermaLetturaMessaggio,
                        "Messaggi Modificati":modificaMessaggio}},
                        
                    {"title": "Alert", "data": {"Nuovi Alert":nuovoAlert,
                        "Alert Eliminati":cancellazioneAlert,
                        "Alert Modificati":modificaAlert,
                        "Alert Spenti":spegnimentoAlert}},
                ]

    print(listAssets)


    return home.get_html(values=values, info = info, analytics = analytics)

@app.route('/assets-filtrati/<details>')
def assets_filtered(details):
    for detail in details:
        print(detail)
        
    return 'Teste'
    #return render_template(,details)


@app.route('/pdf_generator')
def pdf_generator():
    from views import pdf_generator
    listAssets = multichain.client.listassets()
    return pdf_generator.pdf_generator_asset(listAssets = listAssets )

    
     #return  redirect('/assets')

@app.route('/pdf_generatorblocks')
def pdf_generatorblocks():
    from views import pdf_generatorblocks
    listAssets = multichain.client.listassets()
    from views import blocks
    info = multichain.client.getinfo().as_dict()    
    i = 0
    listBlocks = multichain.client.listblocks(0)
    listBlocksArray = []
    listBlocksArray.append(listBlocks)

    while(multichain.client.listblocks(i + 1) != []):
        i = i + 1
        listBlocksArray.append(multichain.client.listblocks(i))
    
    #print("arifur listBlocksArray :", listBlocksArray)
    return pdf_generatorblocks.pdf_generator_blocks(listBlocksArray = listBlocksArray )


@app.route('/assets')
def assets():
    items = [1, 1, 2, 4, 4]
    from views import assets
    info = multichain.client.getinfo().as_dict()
    
    listAssets = multichain.client.listassets()
    
    values = f"{info['blocks']},{info['transactions']},{info['assets']}"
    
    return assets.get_html(items=items, listAssets = listAssets)

@app.route('/streams')
def streams():
     from views import streams
     streamsdata = multichain.client.liststreams()
     #streamsdata2 = multichain.client.listaddresses()
     #print("arifur stream data :",streamsdata2)
    
    
     return streams.get_html( streamsdata = streamsdata)
    



@app.route("/download")
def route_download():
    import pdfkit
    # Get the HTML output
    out = render_template("export.html")
    
    # PDF options
    options = {
        "orientation": "landscape",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }
    
    # Build PDF from HTML 
    pdf = pdfkit.from_string(out, options=options)
    
    # Download the PDF
    return Response(pdf, mimetype="application/pdf")

@app.route('/blocks')
def blocks():
    from views import blocks
    info = multichain.client.getinfo().as_dict()    
    i = 0
    listBlocks = multichain.client.listblocks(0)
    listBlocksArray = []
    listBlocksArray.append(listBlocks)

    while(multichain.client.listblocks(i + 1) != []):
        i = i + 1
        listBlocksArray.append(multichain.client.listblocks(i))
    
    return blocks.get_html(listBlocksArray=listBlocksArray, datetime = datetime)


@app.route('/addresses')
def addresses():
    return 'addresses'



@app.route('/transactions')
def transactions():
    #transactions = multichain.client.listaccounts(str(0))
    #trans = multichain.client.listassettransactions(str(0))
    #print(trans)
    #html = render_template('blocks.html', 
    #    listBlocksArray = trans)
    #return html

    from views import transactions

    info = multichain.client.getinfo().as_dict()

    addressesList = multichain.client.explorerlisttransactions(True, info['transactions'], 0)
    

    return transactions.get_html(addressesList, datetime)

@app.route('/pdf_generator_transactions')
def pdf_generator_transactions():
     
    from views import pdf_generator_transactions

    listAssets = multichain.client.listassets()
    info = multichain.client.getinfo().as_dict()

    addressesList = multichain.client.explorerlisttransactions(True, info['transactions'], 0)
    return pdf_generator_transactions.pdf_generator_transactionlist (addressesList = addressesList, app_instance_path= app.root_path )

@app.route('/chain')
def chain():
    from views import info

    generalInfo = multichain.client.getchaintotals()

    listParams = multichain.client.getblockchainparams()

    return info.get_html(general_information=generalInfo, blockchain_parameters=listParams)

@app.route('/assets/<string:Operazione>')
def detail():
    from views import error, assets
    
    operazione: request.base_url.replace("_", " ")

    listAssets = multichain.client.listassets()

    listAssetsFiltered = [asset['details']['tipo_oprazione'] for asset in listAssets if asset['details']['tipo_oprazione'] == operazione ]



@app.route('/test_filtri')
def test_filtri():
    
    listAssets = multichain.client.listassets()
    i = 0
    listBlocks = multichain.client.listblocks(0)
    listBlocksArray = []
    listBlocksArray.append(listBlocks)

    while(multichain.client.listblocks(i + 1) != []):
        i = i + 1
        listBlocksArray.append(multichain.client.listblocks(i))

    #print('-----------------------------------------', assets_filter.AssetsFilter(list_assets=listAssets).get_detail_from_filters_with_username('dam', datetime.fromtimestamp(1662602640), datetime.now()))
    
    #print('-----------------------------------------', blocks_filter.BlocksFilter(list_blocks=listBlocksArray).get_block_from_filters_with_height('15', datetime.fromtimestamp(1662602640), datetime.now()))

    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)