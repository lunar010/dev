import requests
from flask import Flask, request, Response
web = Flask(__name__)

server_domain = 'cloudlayer.kro.kr'

@web.route('/', defaults={'path': ''})
@web.route('/<path:path>')
def main(path):
    url_splited = request.url.split("/")[2]
    if url_splited == server_domain:
        subdomains = ''
    else:
        subdomains = request.url.split("/")[2].replace(server_domain, '')
        resp = requests.request(
            method=request.method,
            url='https://' + subdomains + 'xates.dev/'+path,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                 if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
