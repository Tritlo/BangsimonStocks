#CLI for the stockInfo program

from stockInfo import stockInfo
from stockPlot import stockPlot

def Bhelp():
    """
    #Use: Bhelp()
    #Post: A help string for the CLI has been printed out.
    """
    helpstring = "The following commands are available:\n\
            help: prints this message\n\
            plot: plots information about the stocks\
            "
    print helpstring


def Bplot():
    """
    #Use: Bplot()
    #Post: A graph has been displayed
    """
    print "Enter number of attribute to plot:"
    print "Available attributes are: (1) Open, (2) High, (3) Low, (4) Close, (5) Volume, (6) Adj Close, (7) Avg. Price"
    ind = raw_input(">> ") 
    print "Enter interval to plot in yyyy-mm-dd format, leave blank for minimum and maximum available date respectively" 
    fromDate = raw_input("From: ")
    if len(fromDate) != 0:
        fromDate = stockObj.stringToDate(fromDate)
    else:
        fromDate = None
    toDate = raw_input("To: ")
    if len(toDate) != 0:
        toDate = stockObj.stringToDate(toDate)
    else:
        toDate = None
    selection = { "1": "Open", "2": "High", "3": "Low", "4": "Close", "5": "Volume", "6": "Adj Close", "7": "Avg. Price"}
    stockPlot(stockObj,selection[ind],fromDate,toDate)

def Bquit():
    """
    #Use: Bquit()
    #Post: A goodbye string has been posted, and the application exited.
    """
    print "Goodbye!"
    quit()





print "Welcome to the Bangsimon stock program!"
print "Please enter the ticker of the company/index you wish to check."
ticker = raw_input("Ticker: ")
stockObj = stockInfo(ticker)

c = 'help'
commands = {'plot': Bplot, 'help':Bhelp, 'quit':Bquit} #: Dictionary of functions
Bhelp()
while c != "quit":
    c = raw_input(">> ")
    if c not in commands:
        print "invalid command"
        continue
    commands[c]()

