import csv
import pandas

class CSVProcessor:

    def readColValue(self, filename, colname):
        csvFile = pandas.read_csv(filename)
        #print(csvFile)
        colval_list = csvFile[colname].tolist()
        return colval_list

    def readMultiColValue(self, filename, colName_list):
        multiColVal_list = []
        for colname in colName_list:
            colval_list = self.readColValue(filename, colname)
            multiColVal_list.append(colval_list)
        return multiColVal_list