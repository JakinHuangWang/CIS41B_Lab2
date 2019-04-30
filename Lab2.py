from college import College
import numpy as np
import matplotlib
matplotlib.use('TkAgg')               	        # tell matplotlib to work with Tkinter
import tkinter as tk                      	# normal import of tkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt	                # normal import of pyplot to plot


def tuitionTrend(c):
    npArr = c.getArr()
    size = len(npArr)
    colorLabelDict = {'.-g':'Private 4-year', '.-b':'Public 4-year', '.-r':'Public 2-year'}
    plt.plot(np.arange(c.getStart_year(), c.getEnd_year() + 1), npArr[:size//2, 0], '.-g', label = 'Private 4-year')
    plt.plot(np.arange(c.getStart_year(), c.getEnd_year() + 1), npArr[:size//2, 2], '.-b', label = 'Public 4-year')
    plt.plot(np.arange(c.getStart_year(), c.getEnd_year() + 1), npArr[:size//2, 4], '.-r', label = 'Public 2-year')
    plt.xticks(np.arange(c.getStart_year(), c.getEnd_year() + 1), rotation = 90, fontsize = 8)
    plt.title('Tuition Trend')
    plt.xlabel('Years')
    plt.ylabel('Tuition')
    plt.legend(loc='best')
    plt.show()
    
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
    plt.show()
    
##Function retVal(someFunc) is a decorator for the function popDensity()
#def retVal(someFunc):
    #def printResult(*args, **kwargs):
        #print("\n" + "*" * 12)
        #result = print(someFunc(*args, **kwargs))
        #print("*" * 12)        
        #return result
    #return printResult    

#@retVal
def fourYearPaths(c, yrNum):
    npArr = c.getArr()
    grad_Yr = yrNum - 1970
    private4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr, 0])
    public4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr, 2])
    ccprivate4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr-2, 4]+npArr[grad_Yr-2:grad_Yr, 0])
    ccpublic4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr-2, 4]+npArr[grad_Yr-2:grad_Yr, 2])
    plt.bar(tuple(range(1, 5)), (private4yr_Cost, public4yr_Cost, ccprivate4yr_Cost, ccpublic4yr_Cost))
    label = ['Private 4-Yr\n' + str(private4yr_Cost), 
             'Public 4-Yr\n' + str(public4yr_Cost), 
             'CC to Private 4-yr\n' + str(ccprivate4yr_Cost), 
             'CC to Public 2-yr\n' + str(ccpublic4yr_Cost)]
    plt.title('4 Pathways Trend(Graduation Year: ' + str(grad_Yr + 1970) + ')' )
    plt.xlabel('Years')
    plt.ylabel('4 Pathways')
    plt.xticks(np.arange(1, 5), label, fontsize = 8)
    plt.show()
    return private4yr_Cost, public4yr_Cost, ccprivate4yr_Cost, ccpublic4yr_Cost  

# Additional code for running GUI application on Mac

# these modules and the code below will be covered in module 4
import sys
import os

def gui2fg():
    """Brings tkinter GUI to foreground on Mac
       Call gui2fg() after creating main window and before mainloop() start
    """
    if sys.platform == 'darwin':  
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))

def main():
    c = College()
    tuitionTrend(c)
    roomAndBoardTrend(c)
    fourYearPaths(c)
#main()   
win = tk.Tk()
def FourYearThing():
    topWin = tk.Toplevel(win)
    userEntry = tk.StringVar()
    tk.Label(topWin, text="Enter year of graduation or click and press Enter for latest year: ").grid(row=0,column=0)
    userEntry = tk.Entry(topWin, textvariable=userEntry)
    userEntry.grid(row=0, column=1)
    userEntry.bind('<Return>', lambda event:innerFourYrThing(topWin, userEntry.get()))
    topWin.mainloop()
    
def innerFourYrThing(topWin, userEntry):
    atopWin = tk.Toplevel(topWin)
    if len(userEntry) == 0:
        userEntry = str(College().getEnd_year())
    print(fourYearPaths(College(), int(userEntry)))
    #s = tk.StringVar()
    #s.set(userEntry)
    #tk.Label(atopWin, textvariable=s).grid()
    atopWin.mainloop()
    
win.title('College Pricing')
win.configure(bg='blue')
win.geometry("500x100")
TuitionB = tk.Button(text='Tuition Trend', width=10, command=lambda:tuitionTrend(College()))
TuitionB.grid(row=0, column=0, padx=10, pady=10)
RoomBoardB = tk.Button(text='Room And Board', width=20, command = lambda:roomAndBoardTrend(College()))
RoomBoardB.grid(row=0, column=1, padx=10, pady=10)
FourYrB = tk.Button(text='4 Year Trend', width=10, command = FourYearThing)
FourYrB.grid(row = 0, column=2, padx=10, pady=10)
win.mainloop()