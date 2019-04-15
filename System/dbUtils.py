from xlsUtils import *
import sqlite3

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
    sample = dict_factory(cursor, row)
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

def updateSample(id, sample):
    query = 'UPDATE results SET '
    query += 'nr_zjawiska = {0}, '.format(sample['nr_zjawiska'].replace(',', '.'))
    query += 'poziom = {0}, '.format(sample['poziom'].replace(',', '.'))
    query += 'nr_probki = {0}, '.format(sample['nr_probki'].replace(',', '.'))
    query += 'data_pobrania = "{0}", '.format(sample['data_pobrania'].replace(',', '.'))
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

def convertNulls(sampleList, character='--'):
    for index, sample in enumerate(sampleList):
        for key, value in sample.items():
            if value==None:
                sampleList[index][key]=character