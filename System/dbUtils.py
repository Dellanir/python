from xlsUtils import *
import sqlite3
import glob

def executeInsert(query):
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

def convertNulls(sampleList, character='--'):
    for index, sample in enumerate(sampleList):
        for key, value in sample.items():
            if value==None:
                sampleList[index][key]=character