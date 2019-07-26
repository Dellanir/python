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
def sample(id):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['SAMPLE']
    sample = getSample(id)
    samples = [sample]
    convertNulls(samples)
    return render_template('sample.html', samples=samples, config=config)

@app.route('/samples')
def samples():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['SAMPLE']
    samples = getAllSamples()
    convertNulls(samples)
    return render_template('sample.html', samples=samples, config=config)

@app.route('/isotopes')
def isotopes():
    isotopes = getAllIsotopes()
    convertNulls(isotopes)
    return render_template('isotope.html', isotopes=isotopes)

@app.route('/editIsotope/<int:id>', methods = ['GET', 'POST'])
def editIsotope(id):
    edited = False
    if request.method == 'POST':
        edited = True
        updateIsotope(id, request.form)
    isotope = getIsotope(id)
    isotopes = [isotope]
    convertNulls(isotopes, character='')
    return render_template('editIsotope.html', isotope=isotopes[0], edited=edited)

@app.route('/addIsotope', methods = ['GET', 'POST'])
def addNewIsotopeView():
    if request.method == 'POST':
        addIsotope(request.form)
        return '<html>Dodano nowe dane izotopowe! Za 5 sekund zostaniesz przekierowany.<script>window.setTimeout(function(){window.location.href = "/isotopes";}, 5000);</script></html>'
    return render_template('addIsotope.html')

@app.route('/deleteIsotope/<int:id>', methods = ['GET', 'POST'])
def deleteIsotopeView(id):
    if request.method == 'POST':
        deleteIsotope(id)
        return '<html>Usunieto dane izotopowe! Za 5 sekund zostaniesz przekierowany.<script>window.setTimeout(function(){window.location.href = "/isotopes";}, 5000);</script></html>'
    isotope = getIsotope(id)
    isotopes = [isotope]
    convertNulls(isotopes)
    return render_template('deleteIsotope.html', isotope=isotopes[0], id=id)

@app.route('/level/<int:level>')
def samplesByLevel(level):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['SAMPLE']
    samples = getSamplesByLevel(level)
    convertNulls(samples)
    return render_template('sample.html', samples=samples, config=config)

@app.route('/event/<int:event>')
def samplesByEvent(event):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['SAMPLE']
    samples = getSamplesByEvent(event)
    convertNulls(samples)
    return render_template('sample.html', samples=samples, config=config)

@app.route('/event-and-level/<int:event>/<int:level>')
def samplesByEventAndLevel(event, level):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['SAMPLE']
    samples = getSamplesByEventAndLevel(event, level)
    convertNulls(samples)
    return render_template('sample.html', samples=samples, config=config)

@app.route('/editConfig', methods=['GET', 'POST'])
def editConfig():
    config = configparser.SafeConfigParser()
    config.read('config.ini')
    edited = True if request.method == 'POST' else False
    if edited:
        fields = [i for i in request.form]
        for key in config['SAMPLE']:
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
    if request.method == 'POST':
        addSample(request.form)
        return '<html>Dodano nowy pomiar! Za 5 sekund zostaniesz przekierowany.<script>window.setTimeout(function(){window.location.href = "/samples";}, 5000);</script></html>'
    else:
         return render_template('addSample.html')

@app.route('/deleteSample/<int:id>', methods = ['GET', 'POST'])
def deleteSampleView(id):
    if request.method == 'POST':
        deleteSample(id)
        return '<html>Usunieto dane pomiarowe! Za 5 sekund zostaniesz przekierowany.<script>window.setTimeout(function(){window.location.href = "/samples";}, 5000);</script></html>'
    sample = getSample(id)
    samples = [sample]
    convertNulls(samples, character='')
    return render_template('deleteSample.html', sample=samples[0], id=id)

@app.route('/help')
def helpPage():
    return render_template('help.html')

@app.route('/charts', methods=['GET', 'POST'])
def charts():
    if request.method == "GET":
        return render_template('chart.html')
    event = request.form['event']
    level = request.form['level']
    if event != "" and level != "":
        samples = getSamplesByEventAndLevel(event, level)
    if event == "" and level == "":
        samples = getAllSamples()
    if event != "" and level == "":
        samples = getSamplesByEvent(event)
    if event == "" and level != "":
        samples = getSamplesByLevel(level)
    if len(samples)==0:
        return render_template('chart.html', event=event, level=level)
    results = {}
    for key in samples[0]:
        results[key] = [ x[key] for x in samples ]
        if None in results[key]:
            results.pop(key)
    return render_template('chart.html', results=results, samples=samples, event=event, level=level)

@app.route('/charts-chemistry', methods=['GET', 'POST'])
def chartsChemistry():
    if request.method == "GET":
        return render_template('chart.html')
    year = request.form['year']
    chemData = getAllSamples() if year == '' else getAllSamples()
    result = {}
    result['y_axis'] = [ float(x['stezenie_ca_mg_w_h2o_z_soli'].encode('ascii', 'ignore')) for x in chemData if x['stezenie_ca_mg_w_h2o_z_soli'] is not None ]
    result['x_axis'] = [ float(x['steznie_na_k_w_h2o_z_soli'].encode('ascii', 'ignore')) for x in chemData if x['steznie_na_k_w_h2o_z_soli'] is not None ]
    data = []
    for i,x in enumerate(chemData):
        if x['stezenie_ca_mg_w_h2o_z_soli'] is not None:
            point = {}
            point['y'] = float(x['stezenie_ca_mg_w_h2o_z_soli'].encode('ascii', 'ignore'))
            point['x'] = float(x['steznie_na_k_w_h2o_z_soli'].encode('ascii', 'ignore'))
            data.append(point)
    print data
    return render_template('chart-chem.html', chemData=chemData, result=result, data=data)

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

@app.route('/backup', methods=['GET'])
def backup():
    backupList = getBackupList()
    return render_template('backup.html', backupList=backupList)

@app.route('/backupSave', methods=['POST'])
def backupSave():
    backupSavedName = exportBackup()
    backupList = getBackupList()
    return render_template('backup.html', backupList=backupList, backupSavedName=backupSavedName)

@app.route('/backupLoad', methods=['POST'])
def backupLoad():
    backupLoadedName = request.form['name']
    backupSavedName = exportBackup()
    importBackup(backupLoadedName)
    backupList = getBackupList()
    return render_template('backup.html', backupList=backupList, backupSavedName=backupSavedName,
                           backupLoadedName=backupLoadedName)

if __name__ == '__main__':
   config = configparser.ConfigParser()
   config.read('config.ini')
   app.run( debug = config['SERVER']['debug'],
            port = config['SERVER']['port'],
            host = config['SERVER']['host']
               )


