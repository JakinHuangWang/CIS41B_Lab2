"""
LAB 2
Author: Jakin Wang
OS: Mac OSX
IDE: Wings IDE
Date: 05/04/2019
"""
from college import College
import numpy as np
import matplotlib
matplotlib.use('TkAgg')               	        # tell matplotlib to work with Tkinter
import tkinter as tk                      	# normal import of tkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt	                # normal import of pyplot to plot

#Function tuitionTrend(c) produces the graph for tuition Trend of Private 4-year, Public 4-year,
#and Public 2-year over the years
def tuitionTrend(c):
    npArr = c.getArr()
    size = len(npArr)
    colorLabelLst = [('.-g', 'Private 4-year'), ('.-b', 'Public 4-year'), ('.-r','Public 2-year')]
    for i in range(len(colorLabelLst)):
        plt.plot(np.arange(c.getStart_year(), c.getEnd_year() + 1), npArr[:size//2, i*2], colorLabelLst[i][0],
                 label=colorLabelLst[i][1])
    plt.xticks(np.arange(c.getStart_year(), c.getEnd_year() + 1), rotation = 90, fontsize = 8)
    plt.title('Tuition Trend')
    plt.xlabel('Years')
    plt.ylabel('Tuition')
    plt.legend(loc='best')
    
#Function tuitionTrend(c) produces the graph for Room and Board Trend of Private 4-year and Public 4-year over the years
def roomAndBoardTrend(c):
    npArr = c.getArr()
    size = len(npArr)
    plt.plot(np.arange(c.getStart_year(), c.getEnd_year() + 1), npArr[:size//2, 6], '.-b', label = 'Private 4-year Room + Board')
    plt.plot(np.arange(c.getStart_year(), c.getEnd_year() + 1), npArr[:size//2, 8], '.-g', label = 'Public 4-year Room + Board')
    plt.xticks(np.arange(c.getStart_year(), c.getEnd_year() + 1), rotation = 90, fontsize = 8)
    plt.title('Room + Board Trend')
    plt.xlabel('Years')
    plt.ylabel('Room + Board')
    plt.legend(loc='best')

#Function retVal(someFunc) is a decorator to print out the different costs of 4 options
def retVal(someFunc):
    def printResult(*args, **kwargs):
        fourOptionLst = ['Private 4-Yr', 'Public 4-Yr', 'CC to Private 4-Yr', 'CC to Public 2-Yr']
        print("\n" + "*" * 12)
        print("Year: ", args[1])
        result = print(*zip(fourOptionLst, someFunc(*args, **kwargs)))
        print("*" * 12)
        return result
    return printResult

#Function FourYearPaths(c, yrNum) takes in a year number and the college to calculate and graph the 4 options.
@retVal
def fourYearPaths(c, yrNum):
    npArr = c.getArr()
    grad_Yr = yrNum - c.getStart_year() + 1
    private4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr, 0])
    public4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr, 2])
    ccprivate4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr-2, 4]+npArr[grad_Yr-2:grad_Yr, 0])
    ccpublic4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr-2, 4]+npArr[grad_Yr-2:grad_Yr, 2])
    plt.bar((1,2,3,4), (private4yr_Cost, public4yr_Cost, ccprivate4yr_Cost, ccpublic4yr_Cost), align="center")
    label = ['Private 4-Yr\n' + str(private4yr_Cost),
             'Public 4-Yr\n' + str(public4yr_Cost),
             'CC to Private 4-Yr\n' + str(ccprivate4yr_Cost),
             'CC to Public 2-Yr\n' + str(ccpublic4yr_Cost)]
    plt.title('4 Pathways Trend(Graduation Year: ' + str(grad_Yr + 1970) + ')' )
    plt.xlabel('Years')
    plt.ylabel('4 Pathways')
    plt.xticks((1,2,3,4), label, fontsize = 10)
    return private4yr_Cost, public4yr_Cost, ccprivate4yr_Cost, ccpublic4yr_Cost

#class mainWindow() includes three buttons which will evoke 3 graphs
class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('College Pricing')
        textFctLst = [('Tuition Trend', self.plotTuit),
                      ('Room And Board', self.plotRB),
                      ('4 Year Trend', self.plot4Yrs)]
        try:
            for i in range(len(textFctLst)):
                tk.Button(self, text=textFctLst[i][0], width=12, command=textFctLst[i][1]).grid(row=0, column=i, padx=10, pady=10)
        except TypeError as TE:
            errWin = errorWindow(self, "Different Type Entered in the Field: " + str(TE))
            self.wait_window(errWin)
            self.destroy()
            raise SystemExit
    def plotTuit(self):
        plotWindow(self).graphTrend(tuitionTrend)
    def plotRB(self):
        plotWindow(self).graphTrend(roomAndBoardTrend)
    def plot4Yrs(self):
        dWin = dialogueWindow(self)
        self.wait_window(dWin)
        if dWin.retVal().isdigit(): plotWindow(self).graph4Yrs(fourYearPaths, int(dWin.retVal()))

#class plotWindow plots the functions on the canvas with mainWindow being its Master
class plotWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.transient(master)
        self.title("Plotting Window")
        self.fig = plt.figure(figsize=(7, 7))
    def graphTrend(self, someFunc):
        someFunc(College())
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()
    def graph4Yrs(self, someFunc, Yr):
        someFunc(College(), Yr)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()

#class dialogueWindow presents a window which allows the user to 
#enter the years and return that value to the mainWindow
class dialogueWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.c = College()
        self.userInput = "No Entry"   #Defualt Value when there is no entry
        #cannot access other windows while dialogueWindow is opened
        self.grab_set()
        self.focus_set()
        self.title("Dialogue Window")
        tk.Label(self, text="Enter year of graduation or click and press Enter for latest year: ").grid(row=0,column=0)
        self.userEntry = tk.Entry(self, textvariable=tk.StringVar())
        self.userEntry.grid(row=0, column=1)
        self.userEntry.bind("<Return>", self.getEntry)
    def getEntry(self, event):
        self.userInput = self.userEntry.get().strip()
        self.userEntry.delete(0, tk.END)
        if len(self.userInput) == 0:  self.userInput = str(self.c.getEnd_year())
        if not self.userInput.isdigit() or int(self.userInput) < self.c.getStart_year() + 3 or int(self.userInput) > self.c.getEnd_year():
            self.badInput()
        else:
            self.userInput
            self.destroy()
    def retVal(self):
        return self.userInput
    def badInput(self):
        eWin = errorWindow(self, "Year must be 4 digit between 1974 and 2018")
        self.wait_window(eWin)
        
#class errorWindow presents the error Message whenever an error occurs
class errorWindow(tk.Toplevel):
    def __init__(self, master, errMsg):
        super().__init__(master)
        self.title("Error Window") 
        #cannot access other windows while errorWindow is opened
        self.grab_set()
        self.focus_set()
        self.transient(master)
        tk.Label(self, text = errMsg).grid()
 
#instantiate the main window and run the mainloop       
mWin = mainWindow()
mWin.mainloop()


"""
Dear Customer, after carefully using a python data analysis program, 
I can hereby conclude that the most cost-effective way to earn a 4-year degree is through the
Community College to Public 4-year university Program.
For Reference, I chose the most current data of 5 years, which was the data of 2018, 2017, 2016, 2015, and 2014.
The Result:

************
Year:  2018
('Private 4-Yr', 140780.0) ('Public 4-Yr', 40590.0) ('CC to Private 4-Yr', 78760.0) ('CC to Public 2-Yr', 27710.0)
************

************
Year:  2017
('Private 4-Yr', 138040.0) ('Public 4-Yr', 40040.0) ('CC to Private 4-Yr', 77920.0) ('CC to Public 2-Yr', 27520.0)
************

************
Year:  2016
('Private 4-Yr', 134820.0) ('Public 4-Yr', 39360.0) ('CC to Private 4-Yr', 76260.0) ('CC to Public 2-Yr', 27120.0)
************

************
Year:  2015
('Private 4-Yr', 131630.0) ('Public 4-Yr', 38740.0) ('CC to Private 4-Yr', 74200.0) ('CC to Public 2-Yr', 26600.0)
************

************
Year:  2014
('Private 4-Yr', 128580.0) ('Public 4-Yr', 38020.0) ('CC to Private 4-Yr', 72360.0) ('CC to Public 2-Yr', 26040.0)
************

As you can see the cost ranges from Private 4-Yr: 13 - 14,000, CC to Private 4-Yr: 72 - 78,000, 
Public 4-Yr: 38 - 40,000, to CC to Public 2-Yr: 26 - 27,000.

I chose the most recent 5 years since this data may be the most revelant to your children's educational plan.
"""