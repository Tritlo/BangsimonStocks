from stockInfo import stockInfo
from stockPlot import stockPlot

def Bhelp():
    helpstring = "The following commands are available:\n\
            help: prints this message\n\
            plot: plots information about the stocks\
            "
    print helpstring


def Bplot():
    print "Enter number of attribute to plot:"
    print "Available attributes are: (1) Open, (2) High, (3) Low, (4) Close, (5) Volume, (6) Adj Close, (7) Avg. Price"
    ind = raw_input(">> ") 
    selection = { "1": "Open", "2": "High", "3": "Low", "4": "Close", "5": "Volume", "6": "Adj Close", "7": "Avg. Price"}
    stockPlot(stockObj,selection[ind])

def Bquit():
    print "Goodbye!"
    quit()





print "Welcome to the Bangsimon stock program!"
print "Please enter the ticker of the company/index you wish to check."
ticker = raw_input("Ticker: ")
stockObj = stockInfo(ticker)

c = 'help'
commands = {'plot': Bplot, 'help':Bhelp, 'quit':Bquit}
Bhelp()
while c != "quit":
    c = raw_input(">> ")
    if c not in commands:
        print "invalid command"
        continue
    commands[c]()

