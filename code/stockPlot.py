from stockInfo import stockInfo
import matplotlib.pyplot as plt

# The Price function computes the average of a given day's highest and lowest prices
Price = lambda x: (x[2]+x[3])/2

def stockPlot(s,k):
    # Use: stockPlot(s,k)
    # Pre: s is a stockinfo object, k is an integer, 1<=k<=7
	# Post: We have a plot of the kth attribute of s vs time,
    # where the possible attributes are, in order:
    # Open, High, Low, Close, Volume, Adj Close, and Avg. Price
    dates=[]
    yvalues=[]
    ylabels={'Date':0, 'Open':1, 'High':2, 'Low':3, 'Close':4, 'Volume':5, 'Adj Close':6, 'Avg. Price':7}
    for i in range(0,len(s.infoList)-1): 
        data=s.infoList[i]
        dates.append(data[0])
        if ylabels[k]==7: yvalues.append(Price(data))
        else: yvalues.append(data[ylabels[k]])    
    plt.plot(dates, yvalues)
    plt.ylabel(k)
    plt.xlabel('Date')
    # Find out how to add a title?
    plt.show()
