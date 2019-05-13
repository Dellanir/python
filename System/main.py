import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template, request
import configparser
from xlsUtils import *
from dbUtils import *
import git
import datetime

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/sample/<int:id>')
def probka(id):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['SAMPLE']
    sample = getSample(id)
    samples = [sample]
    convertNulls(samples)
    chemistryData = getChemistryData(sample['nr_probki'])
    return render_template('sample.html', samples=samples, config=config, chemistryData=chemistryData)

@app.route('/samples')
def probki():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['SAMPLE']
    samples = getAllSamples()
    convertNulls(samples)
    return render_template('sample.html', samples=samples, config=config)

@app.route('/editConfig', methods=['GET', 'POST'])
def editConfig():
    config = configparser.SafeConfigParser()
    config.read('config.ini')
    edited = True if request.method == 'POST' else False
    if edited:
        fields = [i for i in request.form]
        for     key in config['SAMPLE']:
            config.set('SAMPLE', key, 'False')
        for key in fields:
            config.set('SAMPLE', key, 'True')
        with open('config.ini', 'wb') as configfile:
            config.write(configfile)
    return render_template('config.html', config = config['SAMPLE'], edited=edited)

@app.route('/editSample/<int:id>', methods=['GET', 'POST'])
def editSample(id):
    edited = True if request.method == 'POST' else False
    if edited:
        updateSample(id, request.form)
    sample = getSample(id)
    samples = [sample]
    convertNulls(samples, character='')
    return render_template('editSample.html', sample=samples[0], edited=edited, mode="edit")

@app.route('/addSample', methods=['GET', 'POST'])
def addNewSample():
    added = True if request.method == 'POST' else False
    mode = "add"
    if added:
        mode = "edit"
        pass
    sample = addSample('')
    samples = [sample]
    convertNulls(samples, character='')
    return render_template('editSample.html', sample=samples[0], added=added, mode=mode)

@app.route('/help')
def helpPage():
    return render_template('help.html')

@app.route('/charts')
def charts():
    return "TODO" #render_template('help.html')

@app.route('/info')
def infoPage():
    try:
        repo = git.Repo('..')
        commit = repo.head.commit
        author = str(commit.author)
        date = str(datetime.datetime.fromtimestamp(commit.committed_date))
        message = str(commit.message)
        revision = str(commit)
    except:
        author = date = message = revision = " -- "
    return render_template('info.html', author=author, date=date, message=message, revision=revision)


if __name__ == '__main__':
   config = configparser.ConfigParser()
   config.read('config.ini')
   app.run( debug = config['SERVER']['debug'],
            port = config['SERVER']['port'],
            host = config['SERVER']['host']
               )


