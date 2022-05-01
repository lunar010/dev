from flask import Flask, request, Response
app = Flask(__name__)

server_domain = 'cloudlayer.kro.kr'

@app.route('/')
def home():
    return 'hi'
