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
    colorLabelLst = [('.-g', 'Private 4-year'), ('.-b', 'Public 4-year'), ('.-r','Public 2-year')]
    for i in range(len(colorLabelLst)):
        plt.plot(np.arange(c.getStart_year(), c.getEnd_year() + 1), npArr[:size//2, i*2], colorLabelLst[i][0], 
                 label=colorLabelLst[i][1])
    plt.xticks(np.arange(c.getStart_year(), c.getEnd_year() + 1), rotation = 90, fontsize = 8)
    plt.title('Tuition Trend')
    plt.xlabel('Years')
    plt.ylabel('Tuition')
    plt.legend(loc='best')
    
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
    grad_Yr = yrNum - c.getStart_year() + 1
    private4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr, 0])
    public4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr, 2])
    ccprivate4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr-2, 4]+npArr[grad_Yr-2:grad_Yr, 0])
    ccpublic4yr_Cost = np.sum(npArr[grad_Yr-4:grad_Yr-2, 4]+npArr[grad_Yr-2:grad_Yr, 2])
    plt.bar((1,2,3,4), (private4yr_Cost, public4yr_Cost, ccprivate4yr_Cost, ccpublic4yr_Cost), align="center")
    label = ['Private 4-Yr\n' + str(private4yr_Cost), 
             'Public 4-Yr\n' + str(public4yr_Cost), 
             'CC to Private 4-yr\n' + str(ccprivate4yr_Cost), 
             'CC to Public 2-yr\n' + str(ccpublic4yr_Cost)]
    plt.title('4 Pathways Trend(Graduation Year: ' + str(grad_Yr + 1970) + ')' )
    plt.xlabel('Years')
    plt.ylabel('4 Pathways')
    plt.xticks((1,2,3,4), label, fontsize = 10)
    return private4yr_Cost, public4yr_Cost, ccprivate4yr_Cost, ccpublic4yr_Cost  

def main():
    c = College()
    tuitionTrend(c)
    roomAndBoardTrend(c)
    fourYearPaths(c)
#main()   
def FourYearThing(c):
    userEntry = tk.StringVar()
    tk.Label(topWin, text="Enter year of graduation or click and press Enter for latest year: ").grid(row=0,column=0)
    userEntry = tk.Entry(topWin, textvariable=userEntry)
    userEntry.grid(row=0, column=1)
    userEntry.bind('<Return>', lambda event:innerFourYrThing(topWin, userEntry))
    
#def innerFourYrThing(topWin, userEntry):
    #entryText = userEntry.get()
    #userEntry.delete(0, tk.END)
    #if not entryText.isdigit():
        #atopWin = tk.Toplevel(topWin)
        #tk.Label(atopWin, text = "You didn't input a number!! Please input again").grid()
        #atopWin.mainloop()      
    #elif len(entryText) == 0:
        #entryText = str(College().getEnd_year())
    #elif int(entryText) < College().getStart_year() or int(entryText) > College().getEnd_year():
        #atopWin = tk.Toplevel(topWin)
        #tk.Label(atopWin, text = "Year not within range!! Please input again").grid()
        #atopWin.mainloop()      
    #else:
        #print(fourYearPaths(College(), int(entryText)))
    #s = tk.StringVar()
    #s.set(userEntry)
    #tk.Label(atopWin, textvariable=s).grid()

class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('College Pricing')
        tk.Button(self, text='Tuition Trend', width=10, command=lambda:plotWindow(self).graph(tuitionTrend)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self, text='Room And Board', width=20, command=lambda:plotWindow(self).graph(roomAndBoardTrend)).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text='4 Year Trend', width=10, command=lambda:dialogueWindow(self)).grid(row = 0, column=2, padx=10, pady=10)
class plotWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.grab_set()
        self.focus_set()
        self.transient(master)
        self.title("Plotting Window")
    def graph(self, someFunc):
        fig = plt.figure()
        someFunc(College())
        canvas = FigureCanvasTkAgg(fig, master=self)      
        canvas.get_tk_widget().grid()	               	
        canvas.draw()
    def anotherGraph(self, someFunc, yr):
        fig = plt.figure()
        someFunc(College(), yr)
        canvas = FigureCanvasTkAgg(fig, master=self)      
        canvas.get_tk_widget().grid()	               	
        canvas.draw()       
class dialogueWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.userInput = 0
        self.grab_set()
        self.focus_set()        
        self.transient(master)
        self.entryText = tk.StringVar()
        self.title("Dialogue Window")
        tk.Label(self, text="Enter year of graduation or click and press Enter for latest year: ").grid(row=0,column=0)
        self.userEntry = tk.Entry(self, textvariable=self.entryText)
        self.userEntry.grid(row=0, column=1)
        self.userEntry.bind("<Return>", self.getEntry)
    def getEntry(self, event):
        self.userInput = self.userEntry.get()
        self.userEntry.delete(0, tk.END)
        if not self.userInput.isdigit() or int(self.userInput) < 1971 or int(self.userInput) > 2018:
            self.badInput()
        else:
            plotWindow(self).anotherGraph(fourYearPaths, int(self.userInput))
    def retVal(self):
        return self.userInput
    def badInput(self):
        eWin = errorWindow(self)
    #def retYr(self):
        #return self.userInput
class errorWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.grab_set()
        self.focus_set()        
        tk.Label(self, text = "Year must be 4 digit between 1971 and 2018").grid()             
mainWindow().mainloop()