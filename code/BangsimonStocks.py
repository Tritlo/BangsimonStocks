#CLI for the stockInfo program

from stockInfo import stockInfo
from stockPlot import *
from stockAnalysis import *
from stockUtil import *

def Bhelp(args):
    """
    #Use: Bhelp(args)
    #Pre: args is a list of strings
    #Post: A help string for the CLI has been printed out, or about args[1] if provided
    """
    helpstring = "The following commands are available:\n\
            help: prints this message\n\
            help command: dislpays help message about the command\n\
            plot: plots information about the stocks\n\
            change: changes which stocks are being examined\n\
            current: displays current information about the stock\n\
            beta: displays the beta-value of the stock\n\
            quit: exits program\
            "
    helpdict = { 
            'help': 'help: prints this message',
            'plot': 'plots information about the stocks, optional arguments are number of property to plot, date from which to plot and date to which to plot. The dates are on yyyy-mm-dd format. The following properties ar available: Available attributes are: (1) Open, (2) High, (3) Low, (4) Close, (5) Volume, (6) Adj Close, (7) Avg. Price',
            'change': 'changes which stocks are being examined, optional argument is ticker of stock to change to.',
            'current': 'displays current information about the stock, optional argument is property to display. The following properties are available: price,  change, volume,  avg_daily_volume,  stock_exchange,  market_cap,  book_value,  ebitda,  dividend_per_share,  dividend_yield,  earnings_per_share,  52_week_high,  52_week_low,  50day_moving_avg,  200day_moving_avg,  price_earnings_ratio,  price_earnings_growth_ratio,  price_sales_ratio,  price_book_ratio,  short_ratio.',
'beta': 'displays the beta-value of the stock, necessary arguments are the dates from which to calculate and the date to which to calculate',
                'quit': 'exits program'
            }

    if len(args) == 1:
        print helpstring
    else:
        if args[1] in helpdict:
            print helpdict[args[1]]
        else:
            print "Command %s not found" % (args[1])

def Bplot(args):
    """
    #Use: Bplot(args)
    #Pre: args is a list of strings
    #Post: A graph has been displayed, graph of args[1] if provided, from args[2] if provided to args[3] if provided
    """
    selection = { "1": "Open", "2": "High", "3": "Low", "4": "Close", "5": "Volume", "6": "Adj Close", "7": "Avg. Price"}
    try:
        if len(args) == 1:
            print "Enter number of attribute to plot:"
            print "Available attributes are: (1) Open, (2) High, (3) Low, (4) Close, (5) Volume, (6) Adj Close, (7) Avg. Price"
            ind = raw_input(">> ") 
            print "Enter interval to plot in yyyy-mm-dd format, leave blank for minimum and maximum available date respectively" 
            fromDate = raw_input("From: ")
            if len(fromDate) != 0:
                fromDate = stringToDate(fromDate)
            else:
                fromDate = None
            toDate = raw_input("To: ")
            if len(toDate) != 0:
                toDate = stringToDate(toDate)
            else:
                toDate = None
            prop = ind
            
        else:
            if len(args) == 2:
                    prop = args[1]
                    toDate,fromDate = None,None

            else:
                if len(args) == 3:
                    prop = args[1]
                    fromDate = stringToDate(args[2])
                    toDate = None
                else:
                    prop = args[1]
                    fromDate = stringToDate(args[2])
                    toDate = stringToDate(args[3])
        stockPlot(stockObj,selection[prop],fromDate,toDate)
    except KeyError:
        print "Invalid property"
    except IndexError:
        print "Invalid date. It should be a valid date on the yyyy-mm-dd format"
    except ValueError:
        print "Invalid date. It should be a valid date on the yyyy-mm-dd format"

def Bcurrent(args):
    """
    #Use: Bcurrent(args)
    #Pre: args is a list of strings
    #Post: Current information about the stock has been displayed, all if args[1] not provided, else only the current args[1].
    """
    global stockObj
    if len(args) == 1:
        print stockObj.getCurrent()
    else:
        try:
            print stockObj.getCurrentProperty(args[1])
        except KeyError:
            print "Invalid property %s" % (args[1])

def Bbeta(args):
    """
    # Use: Bbeta(args)
    # Pre: 
    # Post: the beta value of the stock for the time period from fromDate to toDate has been displayed if data exists for those dates,
    # if data does not exist for those dates the user has been prompted to try other dates.
    """
    try:
            print "Enter interval to calculate the Beta-value for in yyyy-mm-dd format., leave blank for minimum and maximum available date respectively" 
            fromDate = raw_input("From: ")
            if len(fromDate) != 0:
                fromDate = stringToDate(fromDate)
            else:
                fromDate = None
            toDate = raw_input("To: ")
            if len(toDate) != 0:
                toDate = stringToDate(toDate)
            else:
                toDate = None
            print 'beta: '+str(Beta(stockObj, fromDate, toDate))
              
    except IndexError:
        print "Invalid date. It should be a valid date on the yyyy-mm-dd format."
    except ValueError:
        print "Invalid date. Either the format was not yyyy-mm-dd, or not within the available range."
  

    
            
           

def Bquit(args):
    """
    #Use: Bquit(args)
    #Pre: args is a list of strings
    #Post: A goodbye string has been posted, and the application exited.
    """
    print "Goodbye!"
    quit()

def Bchange(args):
    """
    #Use: Bchange(args)
    #Pre: args is a list of strings, args[1] is a optional string that represents a ticker.
    #Post:The stockObject has been changed, to args[1] if provided and correct.
    """
    global stockObj
    if len(args) == 1:
        print "Please enter the ticker of the company/index you wish to check."
        while True:
            ticker = raw_input("Ticker: ")
            try:
                stockObj = stockInfo(ticker)
                print stockObj
                break
            except ValueError:
                print "Ticker '%s'  not found. Please enter valid ticker" % (ticker)
    else:
        try:
            stockObj = stockInfo(args[1])
            print stockObj
        except ValueError:
            print "Ticker '%s'  not found. Please enter valid ticker" % (args[1])



print "Welcome to Bangsimon Stocks!"
print "Please enter the ticker of the company/index you wish to check."
while True:
    ticker = raw_input("Ticker: ")
    try:
        stockObj = stockInfo(ticker)
        break
    except ValueError:
        print "%s ticker not found. Please enter valid ticker" % (ticker)

c = 'help'
print stockObj
commands = {'plot': Bplot, 'help':Bhelp, 'quit':Bquit, 'change': Bchange, 'current':Bcurrent, 'beta':Bbeta} #: Dictionary of functions
Bhelp(['help'])
while c != "quit":
    c = raw_input(">> ")
    args = c.split()
    if len(args) >= 1:
        if args[0] not in commands:
            print "invalid command"
            continue
        commands[args[0]](args)

