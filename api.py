import io
import os
import pickle

import requests
from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)
from PIL import Image

from model import CLIP
from translation import Translator

app = Flask(__name__)
app.secret_key = os.urandom(24)

clip = CLIP()
translator = Translator()


@app.route('/getToken', methods=['POST'])
def getToken():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            clientId = data['clientId']
            clientSecret = data['clientSecret']
        except:
            return {"code": 2100}  # "Data format is error"
        Url = 'https://cads-api.fpt.vn/oauth2/token'
        r = requests.post(Url, json={
            "client_id": clientId,
            "client_secret": clientSecret,
            "grant_type": "client_credentials",
            "scope": "read"
        })
        return {"code": r.status_code}  # "get token successfully"


@app.route('/add_items', methods=['GET', 'POST'])
def labels_init():

    try:
        data = request.form
        names = data['names'].replace("'", "").split(',')
        language = data['lang']
    except:
        return {"code": 2100}  # "Data format is error"
    if language == 'en':
        clip.encode_labels(names)
    else: 
        tranlated_names = translator.translate(names)
        clip.encode_labels(tranlated_names)
    return {"code": 200}  # "added successfully"


@app.route('/item_check', methods=['GET', 'POST'])
def item_check():

    try:
        data = request.files['image']
        image = Image.open(data)
    except:
        return {"code": 2100}  # "Data format is error"
    names, scores = clip.predict(image)
    return {"names": names[0], "code": 200}  # "check successfully"


@app.route('/identify', methods=['GET', 'POST'])
def identify():

    try:
        data = request.form
        names = data['names'].replace("'", "").split(',')
        language = data['lang']
        data = request.files['image']
        image = Image.open(data)
    except:
        return {"code": 2100}  # "Data format is error"
    
    if language == 'en':
        clip.encode_labels(names)
    else: 
        tranlated_names = translator.translate(names)
        clip.encode_labels(tranlated_names)
    names, scores = clip.predict(image)
    return {"names": names[0], "code": 200}  # "check successfully"



if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=9090)
    app.run(host='0.0.0.0', port=6002,  use_reloader=False)
    #serve(app, host='0.0.0.0', port=9090, url_scheme='https')
    #app.config["SECRET_KEY"] = "camerafpt"
    #http_server = WSGIServer(('0.0.0.0', 6000), app)
    # http_server.serve_forever()
