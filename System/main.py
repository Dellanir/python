import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template
import configparser

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
   return render_template('index.html')

if __name__ == '__main__':
   config = configparser.ConfigParser()
   config.read('config.ini')
   app.run( debug = config['SERVER']['debug'],
            port = config['SERVER']['port'],
            host = config['SERVER']['host']
               )

