import xlrd
import configparser
from collections import OrderedDict


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
        return value

    for key in xls:
        values[key] = getValueByCellIndex(xls[key])
    return values