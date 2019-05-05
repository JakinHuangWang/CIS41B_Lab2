"""
LAB 2
Author: Jakin Wang
OS: Mac OSX
IDE: Wings IDE
Date: 05/04/2019
"""
import numpy as np
import csv

#class College includes: default filename, start_year, end_year, a numpy Array and all the accessor methods
class College:
    filename = 'tuition.csv'
    start_year = 1971
    end_year = 2018
    def __init__(self):
        try:
            with open(self.filename, 'r') as infile:
                self.npArr = np.array([[float(x) for x in lst] for lst in csv.reader(infile)])
        except IOError:
            print('Error Opening File!!')
            raise SystemExit
    def getStart_year(self):
        return self.start_year
    def getEnd_year(self):
        return self.end_year
    def getArr(self):
        return self.npArr
