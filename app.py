from flask import request, Flask

app = Flask(__name__)

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    return f'Authorization code: {auth_code}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)