import os
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, jsonify, request, redirect
from dotenv import load_dotenv
import logging

load_dotenv()

client_id = os.getenv('QUICKBOOKS_CLIENT_ID')
client_secret = os.getenv('QUICKBOOKS_CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI') 
company_id = os.getenv('QUICKBOOKS_COMPANY_ID')
notion_api_key = os.getenv('NOTION_API_KEY')
notion_database_id = os.getenv('NOTION_DATABASE_ID')

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def home():
    auth_url = f"https://appcenter.intuit.com/connect/oauth2?client_id={client_id}&response_type=code&scope=com.intuit.quickbooks.accounting&redirect_uri={redirect_uri}&state=1234"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    try:
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

        # Ensure tokens are correctly parsed
        if 'access_token' in tokens and 'refresh_token' in tokens:
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            return f'Access Token: {access_token}, Refresh Token: {refresh_token}'
        else:
            logging.error(f"Token error: {tokens}")
            return jsonify({"error": tokens}), 500

    except Exception as e:
        logging.exception("An error occurred during the callback processing")
        return jsonify({"error": str(e)}), 500
      

# TODO: function to retrive access and refresh tokens with input: auth code
# TODO: function to refresh tokens once they expire (handle 401 status code error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
