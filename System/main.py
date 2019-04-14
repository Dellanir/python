import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template
import configparser
from xlsUtils import *
from dbUtils import *

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/probka/<int:id>')
def probka(id):
    sample = getSample(id)
    samples = [sample]
    convertNulls(samples)
    return render_template('probka.html', samples=sample)

@app.route('/probki')
def probki():
    samples = getAllSamples()
    convertNulls(samples)
    return render_template('probka.html', samples=samples)

@app.route('/config')
def config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['PROBKI']
    return render_template('config.html', config=config)

if __name__ == '__main__':
   config = configparser.ConfigParser()
   config.read('config.ini')
   app.run( debug = config['SERVER']['debug'],
            port = config['SERVER']['port'],
            host = config['SERVER']['host']
               )


