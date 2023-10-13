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
from io import BytesIO

app = Flask(__name__, static_url_path='/', static_folder='./')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/code', methods=['GET','POST'])
@cross_origin()
def generate_MRZ():
    doc_type = request.args.get('doc_type')
    code = str(gen.random_generate(doc_type=doc_type))
    response = {}
    response["MRZ"] = code
    resp = Response(json.dumps(response))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/image', methods=['GET','POST'])
@cross_origin()
def generate_MRZ_image():
    doc_type = "TD3"
    nationality = gen.random_nationality()
    code = str(gen.random_generate(doc_type=doc_type,nationality=nationality))
    img = gen.mrz_filled(code,nationality)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    print(img_str)
    response = {}
    response["base64"] = img_str.decode()
    response["MRZ"] = str(code)
    resp = Response(json.dumps(response))
    resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == '__main__':
   app.run(host = "0.0.0.0", port = 8888) #, ssl_context='adhoc'