
from flask import Flask, request, make_response, render_template
from datetime import datetime
import os.path, re, time, json

app = Flask(__name__)



@app.route('/')
def indexpage():


    return "test"
    #return render_template('index.html', name='Jerry')



if __name__ == "__main__":
    #app.run(debug=True)
    pass

