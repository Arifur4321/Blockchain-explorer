from pickle import TRUE
from tkinter.tix import Tree
import requests

def checkToken(token):
    check_token_url = "http://192.168.99.21:8189/InplaceAPI/InplaceAPI_ValidazioneToken/EseguiValidazioneToken?valoreToken=" + str(token)
    r = requests.get(check_token_url)
    respond= r.json()
    if bool(respond['ValidazioneOK']):
        return True  
    return False