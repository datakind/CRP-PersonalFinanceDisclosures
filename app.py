import os
from flask import Flask, render_template
from algoliasearch import algoliasearch
from dotenv import load_dotenv, find_dotenv


app = Flask(__name__)
load_dotenv(find_dotenv())

algolia_api_key = os.environ.get('ALGOLIA_API_KEY')
algolia_app_key = os.environ.get('ALGOLIA_APP_ID')

client = algoliasearch.Client(algolia_app_key, algolia_api_key)
index = client.init_index('master_disclosure')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')