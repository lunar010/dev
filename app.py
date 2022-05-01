import requests
from flask import Flask, request, Response
web = Flask(__name__)

server_domain = 'cloudlayer.kro.kr'

@web.route('/')
def home():
    return 'hi'
