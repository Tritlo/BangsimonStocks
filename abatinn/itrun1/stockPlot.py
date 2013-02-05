from stockInfo import stockInfo
import matplotlib.pyplot as plt
from datetime import date

# The Price function computes the average of a given day's opening and closing prices
Price = lambda x: (x[1] + x[4]) / 2

def stockPlot(s,k,fromDate=None,toDate=None):
    # Use: stockPlot(s,k,fromDate,toDate)
    # Pre: s is a stockinfo object, k is a string which describes an attribute of s
    # fromDate and toDate are optional date objects
	# Post: We have a plot of the attribute k of s vs time,
    # where the possible attributes are, in order:
    # Open, High, Low, Close, Volume, Adj Close, and Avg. Price
    if fromDate==None: 
        fromDate=s.fromDate
    if toDate==None:
        toDate=s.toDate
    dates=[]
    yvalues=[]
    ylabels={'Date':0, 'Open':1, 'High':2, 'Low':3, 'Close':4, 'Volume':5, 'Adj Close':6, 'Avg. Price':7}
    infoList=s.listFromTo(fromDate,toDate)
    n=len(infoList)
    for i in range(0,n-1): 
        data=infoList[i]
        dates.append(data[0])
        if ylabels[k]==7: yvalues.append(Price(data))
        else: yvalues.append(data[ylabels[k]])  
    if ylabels[k]==5: plt.bar(dates, yvalues, align="center")
    else: plt.plot(dates, yvalues)   
    
    plt.ylabel(k)
    plt.xlabel('Date')
    # Find out how to add a title?
    plt.show()
