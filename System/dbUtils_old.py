from xlsUtils import *
import sqlite3
import glob

def prepareInsert(sample):
    cmd = 'insert into samples (kod_probki, gestosc_roztworu, k, ca, mg, br, cl, na, so4, kbr, caso4, mgso4, kcl, nacl, cacl2, mgcl2, kbr_, c, a, c1, a1, m1, m2, m3, m4, m5, m6, m7, e, f, i1, i2, i3, i4, i5, i6, i7, ts, ds, cj, ck, cl_, z1, z2, z3, z4, z5, z6, z7, n1, n2, n3, n4, n5, n6, n7, j1, j2, j3, j4, j5, j6, j7, ta, da, gestosc_roztworu_, stezenie_roztworu_z_soli, stezenie_roztworu_z_jonow, stezenie_roztworu_w_h2o_z_soli, stezenie_roztoworu_w_h2o_z_jonow, stezenie_ca_mg_w_h2o_z_soli, steznie_na_k_w_h2o_z_soli, steznie_na_k_ca_mg_w_h2o_z_soli, poprawka_na_tlen_z_soli, poprawka_na_tlen_z_jonow, poprawka_na_deuter_z_soli, poprawka_na_deuter_z_jonow, stezenie_dane_ca, stezenie_dane_mg, stezenie_dane_k, stezenie_dane_na, stezenie_dane_cl, stezenie_dane_so4, stezenie_dane_br, stezenie_obliczone_ca, stezenie_obliczone_mg, stezenie_obliczone_k, stezenie_obliczone_na, stezenie_obliczone_cl, stezenie_obliczone_so4, stezenie_obliczone_br, sole_ca, sole_mg, sole_k, sole_na, sole_cl, sole_so4, sole_br, stezenie_ca, stezenie_mg, stezenie_k, stezenie_na, stezenie_cl, stezenie_so4, stezenie_br, unkown_e04, unkown_e05, unkown_e06, unkown_e07, unkown_e08, unkown_e09, unkown_e10, unkown_e11) values ('
    strValues = []
    for key, value in sample.items():
       strValues.append('"{0}"'.format(value))
    values = ', '.join(strValues)
    cmd += values + ');'
    return cmd

def executeInsert(query):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()

def getSample(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = 'select * from samples where id = {0}'.format(id)
    for row in c.execute(query):
        r = row
    conn.close()
    config = configparser.ConfigParser()
    config.read('config.ini')
    xls = config['XLS_PROBA']
    values = OrderedDict()
    for index, key in enumerate(xls):
        values[key] = r[index]
    return values

def getAllSamples():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = 'select * from samples'
    config = configparser.ConfigParser()
    config.read('config.ini')
    xls = config['XLS_PROBA']
    samples = []
    for row in c.execute(query):
        values = OrderedDict()
        for index, key in enumerate(xls):
            values[key] = row[index]
        samples.append(values)
    conn.close()
    return samples








#for xls in glob.glob(r'D:\Emma\xls\*.xls'):
#    sample = getValueDictFromXls(xls)
#    print(prepareInsert(sample))
