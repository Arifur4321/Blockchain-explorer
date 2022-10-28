import json
from helpers import assets_filter, blocks_filter
from datetime import datetime

def get_values(listAssets, listBlocksArray, utente, data_inizio, data_fine):
    print (data_inizio)
    #strptime(cls, date_string, format)
    values = assets_filter.AssetsFilter(list_assets=listAssets).get_detail_from_filters_with_username(utente, datetime.strptime(data_inizio,'%Y-%m-%d'), datetime.strptime(data_fine, '%Y-%m-%d'))
    print(json.dumps(values))
    #blocks_filter.BlocksFilter(list_blocks=listBlocksArray).get_block_from_filters_with_height('10', datetime.fromtimestamp(1662602640), datetime.now())
    return values