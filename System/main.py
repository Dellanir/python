import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template, request, flash, request, redirect, url_for
import configparser
from charts import *
from dbUtils import *
try:
    import git
except:
    pass
import datetime
from flask_basicauth import BasicAuth
from werkzeug.utils import secure_filename
from xlsUtils import *
import os

app = Flask(__name__)
basic_auth = BasicAuth(app)
ALLOWED_EXTENSIONS = {'xls'}

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

@app.route('/isotopesLevel/<int:level>')
def isotopesLevel(level):
    isotopes = getIsotopesByLevel(level)
    convertNulls(isotopes)
    return render_template('isotope.html', isotopes=isotopes)

@app.route('/isotopesEvent/<int:event>')
def isotopesEvent(event):
    isotopes = getIsotopesByEvent(event)
    convertNulls(isotopes)
    return render_template('isotope.html', isotopes=isotopes)

@app.route('/isotopesEventAndLevel/<int:event>/<int:level>')
def isotopesEventAndLevel(event, level):
    isotopes = getIsotopesByLevelAndEvent(level, event)
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
    fromDate = request.form['fromDate']
    toDate = request.form['toDate']
    event = request.form['event']
    level = request.form['level']
    if event != '' and level != '':
        isotopes = getIsotopesByLevelAndEvent(level, event)
        chemData = getSamplesByEventAndLevel(event, level)
    if event == '' and level != '':
        isotopes = getIsotopesByLevel(level)
        chemData = getSamplesByLevel(level)
    if event != '' and level == '':
        isotopes = getIsotopesByEvent(event)
        chemData = getSamplesByEvent(event)
    if event == '' and level == '':
        chemData = getAllSamples()
        isotopes = getAllIsotopes()
    if fromDate != '':
        chemData = [x for x in chemData if getDate(x['data_pobrania']) > getDate(fromDate)]
        isotopes = [x for x in isotopes if getDate(x['data_poboru']) > getDate(fromDate)]
    if toDate != '':
        chemData = [x for x in chemData if getDate(x['data_pobrania']) < getDate(toDate)]
        isotopes = [x for x in isotopes if getDate(x['data_poboru']) < getDate(toDate)]
    data = []
    delta = []
    for i,sample in enumerate(chemData):
        if sample['stezenie_ca_mg_w_h2o_z_soli'] is not None:
            point = {}
            point['y'] = round(float(sample['stezenie_ca_mg_w_h2o_z_soli'].encode('ascii', 'ignore')),2)
            point['x'] = round(float(sample['steznie_na_k_w_h2o_z_soli'].encode('ascii', 'ignore')),2)
            point['nr_probki'] = sample['nr_probki']
            point['nr_zjawiska'] = sample['nr_zjawiska']
            point['poziom'] = sample['poziom']
            data.append(point)
    for i, isotope in enumerate(isotopes):
        if isotope['d18o'] != '' and isotope['dd'] != '':
            point = {}
            point['y'] = getAvgValue(isotope, "dd")
            point['x'] = getAvgValue(isotope, "d18o")
            point['nr_probki'] = isotope['nr_probki']
            point['nr_zjawiska'] = sample['nr_zjawiska']
            point['poziom'] = sample['poziom']
            delta.append(point)
    return render_template('chart.html', data=data, delta=delta, fromDate=fromDate, toDate=toDate, event=event,
                           level=level, constChemDataPoints=constChemDataPoints, jezor=jezor, jezor2=jezor2, wmwl=wmwl,
                           smow=smow, gorneParowanie=gorneParowanie, dolneParowanie=dolneParowanie,
                           koncoweParowanie=koncoweParowanie)

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
    name = request.form['nazwa']
    backupSavedName = exportBackup(name)
    backupList = getBackupList()
    return render_template('backup.html', backupList=backupList, backupSavedName=backupSavedName)

@app.route('/backupLoad', methods=['POST'])
def backupLoad():
    backupLoadedName = request.form['name']
    #backupSavedName = exportBackup()
    importBackup(backupLoadedName)
    backupList = getBackupList()
    return render_template('backup.html', backupList=backupList, backupLoadedName=backupLoadedName)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/import', methods=['POST', 'GET'])
def importXls():
    if request.method=='GET':
        return render_template('import.html')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            sample = getValueDictFromXls(filename)
            os.remove(filename)
            return render_template('addImportedSample.html', sample=sample)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    app.config['BASIC_AUTH_USERNAME'] = config['SERVER']['username']
    app.config['BASIC_AUTH_PASSWORD'] = config['SERVER']['password']
    app.config['UPLOAD_FOLDER'] = ''
    if config['SERVER']['require_authentication'] == 'True':
        app.config['BASIC_AUTH_FORCE'] = True
    app.run( debug = config['SERVER']['debug'],
            port = config['SERVER']['port'],
            host = config['SERVER']['host']
               )


