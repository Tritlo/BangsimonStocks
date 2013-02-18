from stockInfo import stockInfo
import matplotlib.pyplot as plt
from datetime import date
from stockAnalysis import movingAverage
import matplotlib

def stockPlot(s,k,fromDate=None,toDate=None, MovingAvg = False, N = 20, Volume=False):
    """
    # Use: stockPlot(s,k,fromDate,toDate)
    # Pre: s is a stockinfo object, k is a string which describes an attribute of s
    # fromDate and toDate are optional date objects, MovingAvg and Volume are boolean
    # N is an Integer >= 0.
    # Post: We have a plot of the attribute k of s vs time,
    # where the possible attributes are, in order:
    # Open, High, Low, Close, Adj Close, and Avg. Price
    # Moving Average with over the period of last N days is plotted if Moving Avg is true,
    # If Volume is true: Below the plot we have a bar graph of the volume of s over time, 
    # where the bar is green if the volume is 'positive' (the day's closing price was higher than the opening price),
    # and red if the volume is 'negative' (opening price higher than closing)
    """
    if fromDate==None: 
        fromDate=s.fromDate
    if toDate==None:
        toDate=s.toDate
        
    attrs={'Date':0, 'Open':1, 'High':2, 'Low':3, 'Close':4, 'Adj Close':5, 'Avg. Price':6}
    
    infoList=s.listFromTo(fromDate,toDate)

    date=lambda d: d[0]
    dateList=map(date,infoList)

    fig = plt.gcf()
    ax = fig.add_subplot(1,1,1)

    a = attrs[k]
    if a == 6:
        getData =lambda d: (d[1] + d[4])/2
    else: 
        if a==5:
            getData =lambda d: d[6]
        else:
            getData=lambda d:d[a]

    dataList=map(getData,infoList)

    if MovingAvg:
        l=movingAverage(s, N, fromDate, toDate)
        ax.plot(dateList,l,'r--',dateList,dataList,'b')
        ax.set_ylabel(k + " (blue) and Moving average over " + str(N) + " days (red)")
    else:
        ax.plot(dateList, dataList)   
    
        ax.set_ylabel(k)

    ax.set_xlabel("Dates")
    if Volume:
        # shift y-limits of the plot so that there is space at the bottom for the volume bar chart
        pad = 0.25
        yl = ax.get_ylim()
        ax.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])

        vol=lambda d: d[5]

        # create the second axis for the volume bar chart
        ax2 = ax.twinx()

        # set the position of ax2 so that it is short (y2=0.32) but otherwise the same size as ax
        ax2.set_position(matplotlib.transforms.Bbox([[0.125,0.1],[0.9,0.32]]))

        # make bar charts and color differently depending on up/down for the day
        posList=[]
        negList=[]
        for i in infoList:
            if i[1]-i[4]<0:
                posList.append(i)
            else: negList.append(i)
        ax2.bar(map(date,posList),map(vol,posList),color='green',width=1,align='center')
        ax2.bar(map(date,negList),map(vol,negList),color='red',width=1,align='center')

        ax2.yaxis.set_label_position("right")
        ax2.set_ylabel('Volume')
    return fig


def smaPlot(s,N=20,fromDate=None,toDate=None):
    return stockPlot(s,"Adj Close",fromDate,toDate,True,N)
    
if __name__ == "__main__":
    Google = stockInfo("GOOG",date(2012,1,1),date.today())
    s = stockPlot(Google,'Adj Close')
