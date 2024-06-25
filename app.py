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
    token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    auth = HTTPBasicAuth(client_id, client_secret)
    headers = {"Accept": "application/json"}
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(token_url, auth=auth, headers=headers, data=data)
    tokens = response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    
    return f'Access Token: {access_token}, Refresh Token: {refresh_token}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
