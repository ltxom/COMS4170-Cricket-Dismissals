from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import itertools
import re
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('homepage.html')  


if __name__ == '__main__':
   app.run(debug = True, port=5001)


