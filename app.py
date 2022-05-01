import requests
from flask import Flask, request, Response, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
web = Flask(__name__)

limiter = Limiter(
    web,
    key_func=get_remote_address,
    default_limits=["500 per day"]
)

server_domain = 'cloudlayer.kro.kr'

@web.errorhandler(429)
def ratelimit_handler(e):
  return render_template('rate.html')

@web.route('/', defaults={'path': ''})
@web.route('/<path:path>')
@limiter.limit("20 per minute")
@limiter.limit("1 per second")
def main(path):
    try:
        ip = request.remote_addr
        if not server_domain in request.url:
            return render_template('directaccess.html')
        else:
            with open(f'./dat/{ip}', 'r') as wip:
                if not ip in wip:
                    return render_template('whitelisted.html')
            resps = requests.get(f'http://ip-api.com/line/{ip}').text
            if resps.split('\n')[2] == 'KR':
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
            else:
                return render_template('ip.html')
    except Exception as e:
        return e

if __name__ == '__main__':
    web.run(host="0.0.0.0",port=3333)
