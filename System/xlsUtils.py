import xlrd
import xlwt
from xlutils.copy import copy
import configparser
from collections import OrderedDict
from dbUtils import *

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def convertIndexToCellRow(index):
    row = int(index[1:]) - 1
    return row          # i.e. A1 is (0,0)

def convertIndexToCellColumn(index):
    column = ord(index[0]) - 65
    return column       # i.e. A1 is (0,0)

def getValueDictFromXls(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    config = configparser.ConfigParser()
    config.read('config.ini')
    xls = config['XLS_PROBA']
    values = OrderedDict()

    def getValueByCellIndex(index):
        row = convertIndexToCellRow(index)
        column = convertIndexToCellColumn(index)
        value = sheet.cell(row, column).value
        if isfloat(value):
            value = float(value)
            value = round(value, 2)
        return value

    for key in xls:
        values[key] = getValueByCellIndex(xls[key])
    return values

# def generateXlsReport(id):
#     config = configparser.ConfigParser()
#     config.read('config.ini')
#     sample = getSample(id)
#     w = copy(xlrd.open_workbook('template.xls'))
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['kod_probki']),
#                          convertIndexToCellColumn(config['XLS_PROBA']['kod_probki']), sample['nr_probki'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['gestosc_roztworu']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['gestosc_roztworu']), sample['gestosc'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['k']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['k']), sample['K'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['ca']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['ca']), sample['Ca'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['mg']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['mg']), sample['Mg'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['br']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['br']), sample['Br'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['cl']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['cl']), sample['Cl'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['na']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['na']), 0)
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['so4']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['so4']), sample['SO4'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['kbr']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['kbr']), sample['KBr'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['caso4']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['caso4']), sample['CaSO4'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['mgso4']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['mgso4']), sample['MgSO4'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['kcl']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['kcl']), sample['KCl'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['nacl']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['nacl']), sample['NaCl'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['cacl2']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['cacl2']), sample['CaCl2'])
#     w.get_sheet(0).write(convertIndexToCellRow(config['XLS_PROBA']['mgcl2']),
#                         convertIndexToCellColumn(config['XLS_PROBA']['mgcl2']), sample['MgCl2'])
#     w.save('{0}.xls'.format(sample['nr_probki']))
