from xlsUtils import *
import sqlite3
import os
import datetime
import shutil
import glob

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
    query = 'INSERT INTO results '
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
    query += 'NaBr = {0} '.format(sample['NaBr'].replace(',', '.'))
    query += 'WHERE id={0}'.format(id)
    query = query.replace(' = ,', ' = NULL,')
    query = query.replace(' =  WHERE', ' = NULL WHERE')
    executeQuery(query)

def addSample(sample):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = 'select * from results where id=(select MAX(id) from results)'
    for row in cursor.execute(query):
        r = row
    sample = dict_factory(cursor, r)
    conn.close()
    return sample

def getChemistryData(sample_number):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = 'select * from samples where kod_probki = "{0}"'.format(sample_number)
    for row in c.execute(query):
        r = row
    chemistryData = dict_factory(c, r)
    conn.close()
    return chemistryData

def getAllChemistryData(year = ''):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = 'select * from results left join samples on results.nr_probki = samples.kod_probki'
    if year != "":
        query += ' WHERE results.data_pobrania like "{0}%"'.format(year)
    samples = []
    for row in c.execute(query):
        r = row
        chemistryData = dict_factory(c, r)
        samples.append(chemistryData)
    conn.close()
    return samples

def convertNulls(sampleList, character='--'):
    for index, sample in enumerate(sampleList):
        for key, value in sample.items():
            if value==None:
                sampleList[index][key]=character

def exportBackup():
    today = str(datetime.datetime.today()).split('.')[0]
    backupName = today.replace(' ','_').replace(':','-') + '.db'
    shutil.copy('data.db', 'db_backup\\{0}'.format(backupName))
    return backupName

def importBackup(backupName):
    shutil.copy('db_backup\\{0}'.format(backupName), 'data.db')

def getBackupList():
    backupList = [ file.split('\\')[-1] for file in glob.glob('db_backup\\*.db') ]
    return backupList
