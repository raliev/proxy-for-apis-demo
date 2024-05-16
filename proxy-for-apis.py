from flask import Flask, request, Response
import requests
from flask_cors import CORS
import json 
#create certificates to support https
#openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

#the URL to which all incoming requests will be redirected to
#CHANGE IT
#TO YOURS TARGET URL

TARGET_URL = '<TARGET_URL>'

def modify_target_path(path):
    # change path if needed
    return path;

def modify_query_string(query_string, args):
    return query_string;    

def modify_headers(headers):
    # change headers if needed
    return headers;    

def modify_json_payload(json_payload):
    return json_payload;    

def modify_response_body(response_body):
    return response_body;

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
    url = TARGET_URL + "/" + modify_target_path(path)
    query_string = modify_query_string(request.query_string.decode('utf-8'), request.args)
    if query_string:
        url = f"{url}{query_string}"

    print("NEW URL:" + url)

    headers = modify_headers({key: value for key, value in request.headers if key != 'Host'})

    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        return Response(headers={'Access-Control-Allow-Origin': '*',
                                 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
                                 'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-anonymous-consents'})

    json_str = request.get_data().decode('utf-8')
    json_obj = {}
    if json_str:
        try:
            json_obj = modify_json_payload(json.loads(json_str))
        except json.JSONDecodeError:
            pass

    bodypayload = json.dumps(json_obj)

    if request.method == 'GET':
        resp = requests.get(url, headers=headers)
    elif request.method == 'POST':
        resp = requests.post(url, headers=headers, data=body)
    elif request.method == 'PUT':
        resp = requests.put(url, headers=headers, data=body)
    elif request.method == 'DELETE':
        resp = requests.delete(url, headers=headers, data=body)
    elif request.method == 'PATCH':
        resp = requests.patch(url, headers=headers, data=body)

    response = Response(modify_response_body(resp.content), status=resp.status_code, headers=dict(resp.headers))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, x-anonymous-consents'

    return response 

if __name__ == '__main__':
    #openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    app.run(port=443, ssl_context=('cert.pem', 'key.pem'))  