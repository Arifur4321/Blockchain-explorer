from flask import render_template

def get_html(asset, mc,assetid, previous_url):
    html = render_template('asset_detail.html', 
        asset = asset,
        mc = mc,
        assetid=assetid,
        previous_url = previous_url)

    return html