from audioop import add, mul
import imp
import json
from lib2to3.pgen2 import token
from pickle import TRUE
import re

import string

from this import d

from flask import Flask, render_template, redirect, Response, request, jsonify, make_response, session
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


multichain = blochchain_interface.Multichain(mode='dev')

app = Flask(__name__)

def get_datails_from_username(username, list_assets):
    #detail = {'value': 0, 'userName': 'Damiano--19/09/2022 10:24:20', 'idFascicolo': 'kjgsdfkjsafd', 'statoOld': '27', 'statoNew': '98', 'tipo_oprazione': 'Cambio Stato Fascicolo', 'descrizione': 'testin putpose'}
    return [asset['details'] for asset in list_assets if asset['details']['userName'].split('--')[0] == username ]

class CheckDetails:
    def checkIfDetailRouteExists(detail):
        existingDetails = ["Cambio Stato Fascicolo", "Cancellazione Messaggio Fascicolo", "Cancellazione Alert Fascicolo", "Caricamento Nuovo Documento nel Fascicolo", "Modifica Documento nel Fascicolo", "Visualizzazione Documento nel Fascicolo", "Cancellazione Documento nel Fascicolo", "Conferma Lettura Messagio nel Fascicolo", "Spegnimento Alert del Fascicolo", "Nuovo Messaggio nel Fascicolo", "Nuovo Alert nel Fascicolo", "Modifica Messaggio nel Fascicolo", "Modifica Alert nel Fascicolo", "Nuovo Scoring del Fascicolo"]
        
        return detail in existingDetails

    def checkIfBlockDetailRouteExists(blockid):
        return multichain.client.listblocks(blockid) != []

class BlocksLoader:

    def loadBlocksForHtml(c, q):

        info = multichain.client.getinfo().as_dict()    

        counter = 0

        i = int(c)
        
        listBlocksArray = []

        while(i < info['blocks'] + 1 and counter < q):
            
            listBlocksArray.append(multichain.client.listblocks(i))

            i = i + 1
            counter = counter + 1

        return listBlocksArray

def start_session (token):
    from helpers import check_token
    return check_token.checkToken(token = token )

def has_session():
    if session['logged'] == True:
        return True
    else:
        return False
    
@app.route('/', methods = ['GET', 'POST'])
def index():

    # if ('logged' not in session.keys() or session['logged'] == False) and request.method == 'GET':
    #     session['logged'] = start_session(request.args.get('classifaitoken'))
    #     print("**************************\n\n\n", session['logged'])

    #     print("************************** ", type(session['logged']))

    

    # if 'logged' not in session.keys() or session['logged'] == False:
    #     return render_template('forbidden.html')
    


    info = multichain.client.getinfo().as_dict()
    listAssets = multichain.client.listassets()
    filtered_assets = []

    logged = 0
    
    if request.method == 'POST':
        if request.form.get('dataInizio1') != '':
            data_inizio = request.form.get('dataInizio1')
        else:
            data_inizio = '1970-01-01'

        if request.form.get('dataFine1') != '':
            data_fine = request.form.get('dataFine1')
        else:
            data_fine = str(datetime.today().strftime('%Y-%m-%d'))

        utente = request.form.get('nomeUtente')

        listAssets = multichain.client.listassets()
        i = 0
        listBlocks = multichain.client.listblocks(0)
        listBlocksArray = []
        listBlocksArray.append(listBlocks)

        while(multichain.client.listblocks(i + 1) != []):
            i = i + 1
            listBlocksArray.append(multichain.client.listblocks(i))
        from views import home_filtered

        filtered_assets = home_filtered.get_values(listAssets, listBlocksArray, utente, data_inizio, data_fine)
        print(json.dumps(filtered_assets)) 
        '''
        [{"value": 0, "userName": "Damiano--19/09/2022 10:24:20", "idFascicolo": "kjgsdfkjsafd", "statoOld": "27", "statoNew": "98", "tipo_oprazione": "Cambio Stato Fascicolo", "descrizione": "testin putpose"}]
        [{"value": 0, "userName": "Damiano--19/09/2022 10:24:20", "idFascicolo": "kjgsdfkjsafd", "statoOld": "27", "statoNew": "98", "tipo_oprazione": "Cambio Stato Fascicolo", "descrizione": "testin putpose"}]
        '''



    if 'logged' in session.keys() and session['logged'] == True:
        from views import home
        detail = {'value': 0, 'userName': 'Damiano--19/09/2022 10:24:20', 'idFascicolo': 'kjgsdfkjsafd', 'statoOld': '27', 'statoNew': '98', 'tipo_oprazione': 'Cambio Stato Fascicolo', 'descrizione': 'testin putpose'}    
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
                            "Documenti Visualizzati":visualizzazioneDocumento,
                            "Documenti Modificati":modificaDocumento,
                            "Documenti Cancellati":cancellazioneDocumento},
                            "dataForPieChart": {"Caricamento_Nuovo_Documento_nel_Fascicolo":caricamentoNuovoDocumento,
                            "Visualizzazione_Documento_nel_Fascicolo":visualizzazioneDocumento,
                            "Modifica_Documento_nel_Fascicolo":modificaDocumento,
                            "Cancellazione_Documento_nel_Fascicolo":cancellazioneDocumento}},

                        {"title": "Fascicoli", "data": {"Cambio Stato Fascicolo": cambioStatoFascicolo,
                            "Fascicoli Nuovo Scoring": nuovoScoringFascicolo},
                            "dataForPieChart": {"Cambio_Stato_Fascicolo": cambioStatoFascicolo,
                            "Nuovo_Scoring_del_Fascicolo": nuovoScoringFascicolo}},

                        {"title": "Messaggi", "data": {"Nuovi Messaggi":nuovoMessaggio,
                            "Messaggi Eliminati": cancellazioneMessaggio,
                            "Messaggi Letti":confermaLetturaMessaggio,
                            "Messaggi Modificati":modificaMessaggio},
                            "dataForPieChart":{"Nuovo_Messaggio_nel_Fascicolo":nuovoMessaggio,
                            "Cancellazione_Messaggio_Fascicolo": cancellazioneMessaggio,
                            "Conferma_Lettura_Messagio_nel_Fascicolo":confermaLetturaMessaggio,
                            "Modifica_Messaggio_nel_Fascicolo":modificaMessaggio}},
                            
                        {"title": "Alert", "data": {"Nuovi Alert":nuovoAlert,
                            "Alert Eliminati":cancellazioneAlert,
                            "Alert Modificati":modificaAlert,
                            "Alert Spenti":spegnimentoAlert},
                            "dataForPieChart": {"Nuovo_Alert_nel_Fascicolo":nuovoAlert,
                            "Cancellazione_Alert_Fascicolo":cancellazioneAlert,
                            "Modifica_Alert_nel_Fascicolo":modificaAlert,
                            "Spegnimento_Alert_del_Fascicolo":spegnimentoAlert}},
                    ]
        return home.get_html(values=values, info = info, analytics = analytics, app_instance_path= app.root_path, filtered_assets=filtered_assets, logged = logged, previous_url = request.referrer)

    return render_template('forbidden.html')
@app.route('/logout')
def logout():
    session['logged'] = False


@app.route('/assets-filtrati/<details>')
def assets_filtered(details):
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

    for detail in details:
        print(detail)
        
    return 'Teste'
    #return render_template(,details)


@app.route('/pdf_generator')
def pdf_generator():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

    from views import pdf_generator
    listAssets = multichain.client.listassets()
    return pdf_generator.pdf_generator_asset(listAssets = listAssets, app_instance_path= app.root_path)


    
     #return  redirect('/assets')

@app.route('/pdf_generatorblocks')
def pdf_generatorblocks():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

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
    return pdf_generatorblocks.pdf_generator_blocks(listBlocksArray = listBlocksArray, app_instance_path = app.root_path)


@app.route('/assets')
def assets():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

    from views import assets
    info = multichain.client.getinfo().as_dict()

    listAssets = multichain.client.listassets()

    values = f"{info['blocks']},{info['transactions']},{info['assets']}"
    
    return assets.get_html(listAssets = listAssets, operazione="", previous_url = request.referrer)

@app.route('/streams')
def streams():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    from views import streams
    streamsdata = multichain.client.liststreams()
    #streamsdata2 = multichain.client.listaddresses()
    #print("arifur stream data :",streamsdata2)
    
    restrictions = []

    for stream in streamsdata:
        stream_restrictions = ""
        for k,v in stream['restrict'].items():
            if v:
                stream_restrictions += str(k)
                stream_restrictions += ": "
                stream_restrictions += str(v)
                stream_restrictions += " "
        if stream_restrictions == "":
            restrictions.append("None")
        else:
            restrictions.append(stream_restrictions)

    return streams.get_html( streamsdata = streamsdata, restrictions = restrictions, previous_url = request.referrer)

@app.route("/download")
def route_download():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

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
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

    from views import blocks
    
    return blocks.get_html(listBlocksArray=[], datetime = datetime, previous_url = request.referrer)


@app.route('/addresses')
def addresses():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    from views import addresses

    addressesList = multichain.client.explorerlistaddresses()

    return addresses.get_html(listAddresses=addressesList, previous_url = request.referrer)

@app.route('/pdf_generator_addresseslist')
def pdf_generator_addresseslist():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

    from views import pdf_generator_addresses

    addressesList = multichain.client.explorerlistaddresses()
    return pdf_generator_addresses.pdf_generator_addresseslist(addressesList = addressesList,  app_instance_path = app.root_path)


@app.route('/transactions')
def transactions():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    #transactions = multichain.client.listaccounts(str(0))
    #trans = multichain.client.listassettransactions(str(0))
    #print(trans)
    #html = render_template('blocks.html', 
    #    listBlocksArray = trans)
    #return html

    from views import transactions

    info = multichain.client.getinfo().as_dict()

    addressesList = multichain.client.explorerlisttransactions(True, info['transactions'], 0)
    

    return transactions.get_html(addressesList, datetime, previous_url = request.referrer)

@app.route('/pdf_generator_transactions')
def pdf_generator_transactions():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    from views import pdf_generator_transactions

    listAssets = multichain.client.listassets()
    info = multichain.client.getinfo().as_dict()

    addressesList = multichain.client.explorerlisttransactions(True, info['transactions'], 0)
    return pdf_generator_transactions.pdf_generator_transactionlist (addressesList = addressesList, app_instance_path= app.root_path )

@app.route('/pdf_generator_streams')
def pdf_generator_streams():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    from views import pdf_generator_streams

    listAssets = multichain.client.listassets()
    info = multichain.client.getinfo().as_dict()

    streamsdata = multichain.client.liststreams()

    restrictions = []

    for stream in streamsdata:
        stream_restrictions = ""
        for k,v in stream['restrict'].items():
            if v:
                stream_restrictions += str(k)
                stream_restrictions += ": "
                stream_restrictions += str(v)
                stream_restrictions += " "
        if stream_restrictions == "":
            restrictions.append("None")
        else:
            restrictions.append(stream_restrictions)

    return pdf_generator_streams.pdf_generator_streams(streamsdata = streamsdata, restrictions = restrictions, app_instance_path= app.root_path )

@app.route('/pdf_generator_blockdetails/<blockid>')
def pdf_generator_blockdetails(blockid):

    from views import pdf_generator_blockdetails
    blockToPass=multichain.client.getblock(blockid)
    txsToPass = []
    info = multichain.client.getinfo().as_dict()
    transactionsList = multichain.client.explorerlisttransactions(True, info['transactions'], 0)

    for blockTx in blockToPass['tx']:

            for tx in transactionsList:
                if tx['txid'] == blockTx:
                    txsToPass.append(tx)
 
    return pdf_generator_blockdetails.pdf_generator_blockdetails(blockToPass = blockToPass,txs = txsToPass, app_instance_path = app.root_path)
 

@app.route('/chain')
def chain():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    from views import info

    generalInfo = multichain.client.getchaintotals()

    listParams = multichain.client.getblockchainparams()

    return info.get_html(general_information=generalInfo, blockchain_parameters=listParams, previous_url = request.referrer)

@app.route('/details/<operazione>')
def details(operazione):
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

    from views import assets, error

    operazioneUrl = request.base_url.split("/")[4].replace("_", " ")

    if CheckDetails.checkIfDetailRouteExists(operazioneUrl):   

        listAssets = multichain.client.listassets()
        listAssetsFiltered = [asset for asset in listAssets if asset['details']['tipo_oprazione'] == operazioneUrl ]
        
        return assets.get_html(listAssets = listAssetsFiltered, operazione = operazioneUrl, previous_url = request.referrer)

    else:       

        return error.get_html(previous_url = request.referrer)

@app.route('/block-detail/<blockid>')
def blockDetails(blockid):
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    from views import blockDetail, error

    searchedBlockId = request.base_url.split("/")[4]

    if searchedBlockId.isnumeric() and CheckDetails.checkIfBlockDetailRouteExists(searchedBlockId):

        blockToPass = multichain.client.getblock(searchedBlockId)

        info = multichain.client.getinfo().as_dict()

        transactionsList = multichain.client.explorerlisttransactions(True, info['transactions'], 0)

        txsToPass = []


        for blockTx in blockToPass['tx']:

            for tx in transactionsList:
                if tx['txid'] == blockTx:
                    txsToPass.append(tx)

        return blockDetail.get_html(block = blockToPass, mc = multichain.client, datetime = datetime, txs = txsToPass, previous_url = request.referrer)

    else:       

        return error.get_html(previous_url = request.referrer)


@app.route('/asset-detail/<assetid>')
def assetDetail(assetid):
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    from views import assetDetail, error

    listAssets = multichain.client.listassets()

    if len(listAssets) >= int(assetid) and int(assetid) >= 0:

        asset = multichain.client.getassetinfo(listAssets[int(assetid)]['issuetxid'])

        return assetDetail.get_html(asset = asset, mc = multichain.client, assetid=assetid, previous_url = request.referrer)

    else:
        return error.get_html(previous_url = request.referrer)


@app.route('/pdf_generatordetails/<assetid>')
def pdf_generatordetails(assetid):
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')
    from views import pdf_generatordetails
    listAssets = multichain.client.listassets()
    from views import assetDetail, error

    listAssets = multichain.client.listassets()

    assetToPass=multichain.client.getassetinfo(assetid)

    return pdf_generatordetails.pdf_generatordetails(assetToPass = assetToPass, app_instance_path = app.root_path)
 
quantity = 20

@app.route('/load_blocks')
def loadBlocks():
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')


    info = multichain.client.getinfo().as_dict()

    counter = 0

    if request.args:

        counter = int(request.args.get("c"))

        if counter == 0:

            res = make_response(jsonify(BlocksLoader.loadBlocksForHtml(counter, quantity)), 200)
        
        elif counter >= int(info['blocks']) + 1:
            res = make_response(jsonify({}), 200)

        else:
            res = make_response(jsonify(BlocksLoader.loadBlocksForHtml(counter, quantity)), 200)

    return res

@app.route('/forbidden')
def forbidden():
    from views import forbidden

    return forbidden.get_html(previous_url = request.referrer)

@app.route('/test_filtri')
def test_filtri():
    #if 'logged' not in session.keys() or session['logged'] == False:
    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

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

@app.route('/pdf_generatorhome')
def pdf_generatorhome():

    if 'logged' not in session.keys() or session['logged'] == False:
        return render_template('forbidden.html')

    from views import pdf_generator_dashboard
    info = multichain.client.getinfo().as_dict()

    listAssets = multichain.client.listassets()

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
                        "Documenti Visualizzati":visualizzazioneDocumento,
                        "Documenti Modificati":modificaDocumento,
                        "Documenti Cancellati":cancellazioneDocumento},
                        "dataForPieChart": {"Caricamento_Nuovo_Documento_nel_Fascicolo":caricamentoNuovoDocumento,
                        "Visualizzazione_Documento_nel_Fascicolo":visualizzazioneDocumento,
                        "Modifica_Documento_nel_Fascicolo":modificaDocumento,
                        "Cancellazione_Documento_nel_Fascicolo":cancellazioneDocumento}},

                    {"title": "Fascicoli", "data": {"Cambio Stato Fascicolo": cambioStatoFascicolo,
                        "Fascicoli Nuovo Scoring": nuovoScoringFascicolo},
                        "dataForPieChart": {"Cambio_Stato_Fascicolo": cambioStatoFascicolo,
                        "Nuovo_Scoring_del_Fascicolo": nuovoScoringFascicolo}},

                    {"title": "Messaggi", "data": {"Nuovi Messaggi":nuovoMessaggio,
                        "Messaggi Eliminati": cancellazioneMessaggio,
                        "Messaggi Letti":confermaLetturaMessaggio,
                        "Messaggi Modificati":modificaMessaggio},
                        "dataForPieChart":{"Nuovo_Messaggio_nel_Fascicolo":nuovoMessaggio,
                        "Cancellazione_Messaggio_Fascicolo": cancellazioneMessaggio,
                        "Conferma_Lettura_Messagio_nel_Fascicolo":confermaLetturaMessaggio,
                        "Modifica_Messaggio_nel_Fascicolo":modificaMessaggio}},
                        
                    {"title": "Alert", "data": {"Nuovi Alert":nuovoAlert,
                        "Alert Eliminati":cancellazioneAlert,
                        "Alert Modificati":modificaAlert,
                        "Alert Spenti":spegnimentoAlert},
                        "dataForPieChart": {"Nuovo_Alert_nel_Fascicolo":nuovoAlert,
                        "Cancellazione_Alert_Fascicolo":cancellazioneAlert,
                        "Modifica_Alert_nel_Fascicolo":modificaAlert,
                        "Spegnimento_Alert_del_Fascicolo":spegnimentoAlert}},
                ]
    
    return pdf_generator_dashboard.pdf_generator_dashboard(info, analytics, app_instance_path = app.root_path)


DEBUG = False
if __name__ == '__main__':
    if DEBUG:
        app.secret_key = '221fd31a-26e8-411f-86f5-c39e95ec4ea1'
        app.run(debug=True)
        
    else:
        app.secret_key = '221fd31a-26e8-411f-86f5-c39e95ec4ea1'
        app.run(debug=False, port=2751, host="0.0.0.0")
