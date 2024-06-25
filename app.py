import os
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, redirect
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('QUICKBOOKS_CLIENT_ID')
client_secret = os.getenv('QUICKBOOKS_CLIENT_SECRET')
redirect_uri = 'https://notion2books-f57fa00a266c.herokuapp.com/callback'  

app = Flask(__name__)

@app.route('/')
def home():
    auth_url = f"https://appcenter.intuit.com/connect/oauth2?client_id={client_id}&response_type=code&scope=com.intuit.quickbooks.accounting&redirect_uri={redirect_uri}&state=1234"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    return f'Authorization code: {auth_code}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
