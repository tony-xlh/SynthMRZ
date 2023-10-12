from flask import Flask, request, send_file, Response
from flask_cors import CORS, cross_origin
import base64
import os
import time
import json
import sys
script_folder_path = os.path.dirname((os.path.realpath(__file__)))
sys.path.append(script_folder_path)
import gen

app = Flask(__name__, static_url_path='/', static_folder='./')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET','POST'])
@cross_origin()
def generate_MRZ():
    doc_type = request.args.get('doc_type')
    code = str(gen.random_generate(doc_type=doc_type))
    response = {}
    response["MRZ"] = code
    resp = Response(json.dumps(response))
    resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == '__main__':
   app.run(host = "0.0.0.0", port = 8888) #, ssl_context='adhoc'