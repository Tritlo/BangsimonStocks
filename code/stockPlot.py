from stockInfo import stockInfo
import matplotlib.pyplot as plt
from datetime import date
from stockAnalysis import movingAverage

# The Price function computes the average of a given day's opening and closing prices
Price = lambda x: (x[1] + x[4]) / 2

def stockPlot(s,k,fromDate=None,toDate=None, MovingAvg = False, N = 20):
    """
    # Use: stockPlot(s,k,fromDate,toDate)
    # Pre: s is a stockinfo object, k is a string which describes an attribute of s
    # fromDate and toDate are optional date objects, MovingAvg is boolean
    # N is an Integer >= 0.
    # Post: We have a plot of the attribute k of s vs time,
    # where the possible attributes are, in order:
    # Open, High, Low, Close, Volume, Adj Close, and Avg. Price
    # Moving Average with over the period of last N days is plotted if Moving Avg is true,
    # though not if k is "Volume"
    """
    if fromDate==None: 
        fromDate=s.fromDate
    if toDate==None:
        toDate=s.toDate
        
    attrs={'Date':0, 'Open':1, 'High':2, 'Low':3, 'Close':4, 'Volume':5, 'Adj Close':6, 'Avg. Price':7}
    
    infoList=s.listFromTo(fromDate,toDate)

    date=lambda d: d[0]
    dateList=map(date,infoList)

    a = attrs[k]
    if a == 7:
        getData =lambda d: (d[1] + d[4])/2
    else:
        getData =lambda d: d[a]

    dataList=map(getData,infoList)
    if MovingAvg:
        l=movingAverage(s, N, fromDate, toDate)
        if a==5:
            plt.bar(dateList, dataList, align="center")
            plt.ylabel(k)
        else:
            plt.plot(dateList,l,'r--',dateList,dataList,'b')
            plt.ylabel(k + " (blue) and Moving average over " + str(N) + " days (red)")
    else:
        if a==5:
            plt.bar(dateList, dataList, align="center")
        else:
            plt.plot(dateList, dataList)   
    
        plt.ylabel(k)

    plt.xlabel("Dates")
    #plt.show()
    return plt.gcf()

def smaPlot(s,N=20,fromDate=None,toDate=None):
    return stockPlot(s,"Adj Close",fromDate,toDate,True,N)
    
if __name__ == "__main__":
    Google = stockInfo("GOOG",date(2000,1,1),date.today())
    smaPlot(Google)
