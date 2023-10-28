from flask import Flask,request
from flask_cors import CORS
import requests
from vidsrc import vidsrc

app = Flask(__name__)
CORS(app)

@app.route('/<path:url>', methods=['GET','POST'])
def proxy(url):
    if url.lower().startswith('https'):
        if request.method == 'GET':
            return requests.get(url, params=request.args).content
        elif request.method == 'POST':
            res =  requests.post(url, params=request.args, headers=request.headers, data=request.data.decode('utf8')).content
            print(res)
            return res
    return ""


@app.get('/get-m3u8')
def m3u8():
    tmdb_id = request.args.get('tmdb_id')

    if not tmdb_id:
        return "No tmdb_id provided"

    return vidsrc(tmdb_id)

@app.get('/test')
def test():
    return "success"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)