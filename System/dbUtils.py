from xlsUtils import *
import sqlite3
import os
import datetime
import shutil
import glob

#Helpers
def executeQuery(query):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def dict_factory(cursor, row):
    d = OrderedDict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Sample operations
def getSample(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from results where id = {0}'.format(id)
    for row in cursor.execute(query):
        r = row
    sample = dict_factory(cursor, r)
    conn.close()
    return sample

def getAllSamples():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from results'
    samples = []
    for row in cursor.execute(query):
        sample = dict_factory(cursor, row)
        samples.append(sample)
    conn.close()
    return samples

def getSamplesByLevel(level):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from results where poziom={0}'.format(level)
    samples = []
    for row in cursor.execute(query):
        sample = dict_factory(cursor, row)
        samples.append(sample)
    conn.close()
    return samples

def getSamplesByEvent(event):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from results where nr_zjawiska={0}'.format(event)
    samples = []
    for row in cursor.execute(query):
        sample = dict_factory(cursor, row)
        samples.append(sample)
    conn.close()
    return samples

def getSamplesByEventAndLevel(event, level):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from results where nr_zjawiska={0} and poziom={1}'.format(event, level)
    samples = []
    for row in cursor.execute(query):
        sample = dict_factory(cursor, row)
        samples.append(sample)
    conn.close()
    return samples

def updateSample(id, sample):
    query = 'UPDATE results SET '
    query += 'nr_zjawiska = {0}, '.format(sample['nr_zjawiska'].replace(',', '.'))
    query += 'poziom = {0}, '.format(sample['poziom'].replace(',', '.'))
    query += 'nr_probki = {0}, '.format(sample['nr_probki'].replace(',', '.'))
    query += 'data_pobrania = "{0}", '.format(sample['data_pobrania'].replace('.', '-'))
    query += 'gestosc = {0}, '.format(sample['gestosc'].replace(',', '.'))
    query += 'ph = {0}, '.format(sample['ph'].replace(',', '.'))
    query += 'K = {0}, '.format(sample['K'].replace(',', '.'))
    query += 'Ca = {0}, '.format(sample['Ca'].replace(',', '.'))
    query += 'Mg = {0}, '.format(sample['Mg'].replace(',', '.'))
    query += 'Br = {0}, '.format(sample['Br'].replace(',', '.'))
    query += 'Cl = {0}, '.format(sample['Cl'].replace(',', '.'))
    query += 'CaO = {0}, '.format(sample['CaO'].replace(',', '.'))
    query += 'MgO = {0}, '.format(sample['MgO'].replace(',', '.'))
    query += 'SO3 = {0}, '.format(sample['SO3'].replace(',', '.'))
    query += 'SO4 = {0}, '.format(sample['SO4'].replace(',', '.'))
    query += 'KBr = {0}, '.format(sample['KBr'].replace(',', '.'))
    query += 'CaSO4 = {0}, '.format(sample['CaSO4'].replace(',', '.'))
    query += 'MgSO4 = {0}, '.format(sample['MgSO4'].replace(',', '.'))
    query += 'KCl = {0}, '.format(sample['KCl'].replace(',', '.'))
    query += 'NaCl = {0}, '.format(sample['NaCl'].replace(',', '.'))
    query += 'CaCl2 = {0}, '.format(sample['CaCl2'].replace(',', '.'))
    query += 'MgCl2 = {0}, '.format(sample['MgCl2'].replace(',', '.'))
    query += 'NaBr = {0}, '.format(sample['NaBr'].replace(',', '.'))
    query += 'stezenie_roztworu_z_soli = {0}, '.format(sample['stezenie_roztworu_z_soli'].replace(',', '.'))
    query += 'stezenie_roztworu_z_jonow = {0}, '.format(sample['stezenie_roztworu_z_jonow'].replace(',', '.'))
    query += 'stezenie_roztworu_w_h2o_z_soli = {0}, '.format(sample['stezenie_roztworu_w_h2o_z_soli'].replace(',', '.'))
    query += 'stezenie_roztoworu_w_h2o_z_jonow = {0}, '.format(sample['stezenie_roztoworu_w_h2o_z_jonow'].replace(',', '.'))
    query += 'stezenie_ca_mg_w_h2o_z_soli = {0}, '.format(sample['stezenie_ca_mg_w_h2o_z_soli'].replace(',', '.'))
    query += 'steznie_na_k_w_h2o_z_soli = {0}, '.format(sample['steznie_na_k_w_h2o_z_soli'].replace(',', '.'))
    query += 'steznie_na_k_ca_mg_w_h2o_z_soli = {0}, '.format(sample['steznie_na_k_ca_mg_w_h2o_z_soli'].replace(',', '.'))
    query += 'poprawka_na_tlen_z_soli = {0}, '.format(sample['poprawka_na_tlen_z_soli'].replace(',', '.'))
    query += 'poprawka_na_tlen_z_jonow = {0}, '.format(sample['poprawka_na_tlen_z_jonow'].replace(',', '.'))
    query += 'poprawka_na_deuter_z_soli = {0}, '.format(sample['poprawka_na_deuter_z_soli'].replace(',', '.'))
    query += 'poprawka_na_deuter_z_jonow = {0} '.format(sample ['poprawka_na_deuter_z_jonow'].replace(',', '.'))
    query += 'WHERE id={0}'.format(id)
    query = query.replace(' = ,', ' = NULL,')
    query = query.replace(' =  WHERE', ' = NULL WHERE')
    executeQuery(query)

def addSample(sample):
    query = 'INSERT INTO results(nr_zjawiska, poziom, nr_probki, data_pobrania, gestosc, ph, K, Ca, Mg, Br, Cl, CaO, MgO, SO3, SO4, KBr, CaSO4, MgSO4, KCl, NaCl, CaCl2, MgCl2, NaBr, stezenie_roztworu_z_soli, stezenie_roztworu_z_jonow, stezenie_roztworu_w_h2o_z_soli, stezenie_roztoworu_w_h2o_z_jonow, stezenie_ca_mg_w_h2o_z_soli, steznie_na_k_w_h2o_z_soli, steznie_na_k_ca_mg_w_h2o_z_soli, poprawka_na_tlen_z_soli, poprawka_na_tlen_z_jonow, poprawka_na_deuter_z_soli, poprawka_na_deuter_z_jonow) values ('
    query += '{0}, '.format(sample['nr_zjawiska'].replace(',', '.'))
    query += '{0}, '.format(sample['poziom'].replace(',', '.'))
    query += '{0}, '.format(sample['nr_probki'].replace(',', '.'))
    query += '"{0}", '.format(sample['data_pobrania'].replace('.', '-'))
    query += '{0}, '.format(sample['gestosc'].replace(',', '.'))
    query += '{0}, '.format(sample['ph'].replace(',', '.'))
    query += '{0}, '.format(sample['K'].replace(',', '.'))
    query += '{0}, '.format(sample['Ca'].replace(',', '.'))
    query += '{0}, '.format(sample['Mg'].replace(',', '.'))
    query += '{0}, '.format(sample['Br'].replace(',', '.'))
    query += '{0}, '.format(sample['Cl'].replace(',', '.'))
    query += '{0}, '.format(sample['CaO'].replace(',', '.'))
    query += '{0}, '.format(sample['MgO'].replace(',', '.'))
    query += '{0}, '.format(sample['SO3'].replace(',', '.'))
    query += '{0}, '.format(sample['SO4'].replace(',', '.'))
    query += '{0}, '.format(sample['KBr'].replace(',', '.'))
    query += '{0}, '.format(sample['CaSO4'].replace(',', '.'))
    query += '{0}, '.format(sample['MgSO4'].replace(',', '.'))
    query += '{0}, '.format(sample['KCl'].replace(',', '.'))
    query += '{0}, '.format(sample['NaCl'].replace(',', '.'))
    query += '{0}, '.format(sample['CaCl2'].replace(',', '.'))
    query += '{0}, '.format(sample['MgCl2'].replace(',', '.'))
    query += '{0}, '.format(sample['NaBr'].replace(',', '.'))
    query += '{0}, '.format(sample['stezenie_roztworu_z_soli'].replace(',', '.'))
    query += '{0}, '.format(sample['stezenie_roztworu_z_jonow'].replace(',', '.'))
    query += '{0}, '.format(sample['stezenie_roztworu_w_h2o_z_soli'].replace(',', '.'))
    query += '{0}, '.format(sample['stezenie_roztoworu_w_h2o_z_jonow'].replace(',', '.'))
    query += '{0}, '.format(sample['stezenie_ca_mg_w_h2o_z_soli'].replace(',', '.'))
    query += '{0}, '.format(sample['steznie_na_k_w_h2o_z_soli'].replace(',', '.'))
    query += '{0}, '.format(sample['steznie_na_k_ca_mg_w_h2o_z_soli'].replace(',', '.'))
    query += '{0}, '.format(sample['poprawka_na_tlen_z_soli'].replace(',', '.'))
    query += '{0}, '.format(sample['poprawka_na_tlen_z_jonow'].replace(',', '.'))
    query += '{0}, '.format(sample['poprawka_na_deuter_z_soli'].replace(',', '.'))
    query += '{0})'.format(sample ['poprawka_na_deuter_z_jonow'].replace(',', '.'))
    query = query.replace(' ,', ' NULL,')
    query = query.replace(' )', ' NULL)')
    executeQuery(query)

def deleteSample(id):
    query = "DELETE from results where id={0}".format(id)
    executeQuery(query)

#Isotope operations
def getAllIsotopes():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from izotopy'
    isotopes = []
    for row in cursor.execute(query):
        isotope = dict_factory(cursor, row)
        isotopes.append(isotope)
    conn.close()
    return isotopes

def getIsotopesByLevel(level):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from izotopy where poziom = {0}'.format(level)
    isotopes = []
    for row in cursor.execute(query):
        isotope = dict_factory(cursor, row)
        isotopes.append(isotope)
    conn.close()
    return isotopes

def getIsotopesByEvent(event):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from izotopy where nr_zjawiska = {0}'.format(event)
    isotopes = []
    for row in cursor.execute(query):
        isotope = dict_factory(cursor, row)
        isotopes.append(isotope)
    conn.close()
    return isotopes

def getIsotopesByLevelAndEvent(level, event):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from izotopy where nr_zjawiska = {0} and poziom = {1}'.format(event, level)
    isotopes = []
    for row in cursor.execute(query):
        isotope = dict_factory(cursor, row)
        isotopes.append(isotope)
    conn.close()
    return isotopes

def getIsotope(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from izotopy where id = {0}'.format(id)
    for row in cursor.execute(query):
        r = row
    isotope = dict_factory(cursor, r)
    conn.close()
    return isotope

def updateIsotope(id, isotope):
    query = 'UPDATE izotopy SET '
    query += "nr_probki = '{0}', ".format(isotope['nr_probki'].replace(',', '.'))
    query += "poziom = '{0}', ".format(isotope['poziom'].replace(',', '.'))
    query += "nr_zjawiska = '{0}', ".format(isotope['nr_zjawiska'].replace(',', '.'))
    query += "data_poboru = '{0}', ".format(isotope['data_poboru'].replace(',', '.'))
    query += "camg = '{0}', ".format(isotope['camg'].replace(',', '.'))
    query += "nak = '{0}', ".format(isotope['nak'].replace(',', '.'))
    query += "d18o = '{0}', ".format(isotope['d18o'].replace(',', '.'))
    query += "dd = '{0}' ".format(isotope['dd'].replace(',', '.'))
    query += 'WHERE id={0}'.format(id)
    query = query.replace(' = ,', ' = NULL,')
    query = query.replace(' =  WHERE', ' = NULL WHERE')
    executeQuery(query)

def addIsotope(isotope):
    query = 'INSERT into izotopy(nr_probki, nr_zjawiska, poziom, data_poboru, camg, nak, d18o, dd) values ('
    query += '"{0}", '.format(isotope['nr_probki'])
    query += '"{0}", '.format(isotope['nr_zjawiska'])
    query += '"{0}", '.format(isotope['poziom'])
    query += '"{0}", '.format(isotope['data_poboru'])
    query += '"{0}", '.format(isotope['camg'])
    query += '"{0}", '.format(isotope['nak'])
    query += '"{0}", '.format(isotope['d18o'].replace(',', '.'))
    query += '"{0}")'.format(isotope['dd'].replace(',', '.'))
    query = query.replace(' = ,', ' = NULL,')
    query = query.replace(' =  WHERE', ' = NULL WHERE')
    executeQuery(query)

def deleteIsotope(id):
    query = "DELETE from izotopy where id={0}".format(id)
    executeQuery(query)

def convertNulls(sampleList, character='--'):
    for index, sample in enumerate(sampleList):
        for key, value in sample.items():
            if value==None:
                sampleList[index][key]=character

def exportBackup(name=''):
    today = str(datetime.datetime.today()).split('.')[0]
    backupName = (name + '_' + today).replace(' ','_').replace(':','-') + '.db'
    shutil.copy('data.db', 'db_backup\\{0}'.format(backupName))
    return backupName

def importBackup(backupName):
    shutil.copy('db_backup\\{0}'.format(backupName), 'data.db')

def getBackupList():
    backupList = [ file.split('\\')[-1] for file in glob.glob('db_backup\\*.db') ]
    return backupList

def getSampleYear(sample):
    try:
        year = sample['data_pobrania'][:4]
    except:
        year = ''
    return year

def getIsotopeYear(isotope):
    try:
        year = isotope['data_poboru'][:4]
    except:
        year = ''
    return year

def getAvgValue(isotope, type):
    try:
        elements = map(float, isotope[type].split(' '))
        value = round(sum(elements)/len(elements),2)
    except:
        value = 0
    return value
