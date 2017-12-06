# flask app to handle connected brewery
#import os
from flask import Flask, request, redirect, url_for, render_template
#from werkzeug.utils import secure_filename
from models import *
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def main():
    datalist = []
    for d in Tilt.select().where(Tilt.name == "Red").order_by(Tilt.time.asc()):
        datalist.append((d.time,d.temp,d.gravity))
    unzipped = list(zip(*datalist))
    print(unzipped)

    return render_template('index.html', time=unzipped[0],  temp=unzipped[1], gravity=unzipped[2])

    #     datag.append((d.time,d.gravity))
    #     datat.append((d.time,d.temp))
    #
    # return render_template('index.html', datag=datag,  datat=datat)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
