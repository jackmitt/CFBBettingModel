import pandas as pd
import numpy as np
import scipy.stats

class Database:
    def __init__(self, keys = []):
        self.df = pd.DataFrame()
        self.dict = {}
        for key in keys:
            self.dict[key] = []
        self.tempRow = []

    def getKeys(self):
        return (list(self.dict.keys()))

    def getCol(self, colName):
        return (self.dict[colName])

    def getLength(self):
        return (len(list(self.dict.keys())[0]))

    def getDict(self):
        return (self.dict)

    def getDataFrame(self):
        self.df = pd.DataFrame.from_dict(self.dict)
        return(self.df)

    def getCell(self, col, index):
        return (self.dict[col][index])

    def initDictFromCsv(self, path):
        self.dict = pd.read_csv(path, encoding = "ISO-8859-1").to_dict(orient="list")

    def addColumn(self, colName):
        self.dict[colName] = []

    def addCellToRow(self, datum):
        if (len(self.tempRow) + 1 > len(self.dict)):
            raise ValueError("The row is already full")
        else:
            self.tempRow.append(datum)

    def appendRow(self):
        if (len(self.tempRow) != len(self.dict)):
            raise ValueError("The row is not fully populated")
        else:
            for i in range(len(self.dict.keys())):
                self.dict[list(self.dict.keys())[i]].append(self.tempRow[i])
            self.tempRow = []

    def trashRow(self):
        self.tempRow = []

    def dictToCsv(self, pathName):
        self.df = pd.DataFrame.from_dict(self.dict)
        self.df = self.df.drop_duplicates()
        self.df.to_csv(pathName, index = False)

    def printRow(self):
        print(self.tempRow)

    def printDict(self):
        print(self.dict)

    def reset(self):
        self.tempRow = []
        self.dict = {}
        for key in list(self.dict.keys()):
            self.dict[key] = []

    def merge(self, B):
        for key in B.getKeys():
            if (key not in list(self.dict.keys())):
                self.dict[key] = B.getCol(key)
