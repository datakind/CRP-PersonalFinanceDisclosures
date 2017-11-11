import os
from flask import Flask, render_template
from algoliasearch import algoliasearch
from dotenv import load_dotenv

app = Flask(__name__)
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

algolia_api_key = os.getenv('ALGOLIA_API_KEY')
algolia_app_key = os.getenv('ALGOLIA_APP_ID')
client = algoliasearch.Client(algolia_app_key, algolia_api_key)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')