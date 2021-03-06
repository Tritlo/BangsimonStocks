from datetime import timedelta
from datetime import date
from numpy import *
from stockInfo import stockInfo
from stockUtil import *

def movingAverage(stockInfo, N=20, fromDate=None, toDate=None):
    """
    #U: l = movingAverage(s,fd,td,N)
    #Pre: s is a stockInfo object, fd, td are optional date objects, N is an optional integer >=1, the default value of N is 20.
    #Post: l is a list containing the moving averages from fd to td, if data exists for that interval, otherwise raises exception
    """
    if fromDate==None: 
        fromDate=stockInfo.fromDate
    if toDate==None:
        toDate=stockInfo.toDate
    if not (stockInfo.validDate(fromDate) and stockInfo.validDate(toDate)):
        raise ValueError("Invalid dates")
    
    result = []
    Ndays = timedelta(4*N) #: Have it 4*N, so that it definitely gives us enough days of data (the stock market is not continiously open)

    price = lambda d: d[1]
    
    dataList = stockInfo.listFromTo(fromDate-Ndays,toDate)
    dataList = map( (lambda l: [l[0],l[6]]), dataList)
    dateList = map((lambda l: l[0]), dataList)
    priceList = map((lambda l: l[1]), dataList)

    fromDateIndex = 0
    for i, d in list(enumerate(dateList)):
        if compareDates(d,fromDate) >=0:
            fromDateIndex = i
            break

        
    if fromDateIndex >= N:
        for i in range(fromDateIndex-N,fromDateIndex):
            result.append(sum(priceList[i:i+N])/N)
    else:
        pl = priceList[0:fromDateIndex+N]
        for p in range(fromDateIndex+1,fromDateIndex+N+1):
            result.append(sum(pl[0:p])/p)

    for i in range(N,len(priceList)-fromDateIndex):
        result.append(result[i-1] + (priceList[i+fromDateIndex] -priceList[i-N+fromDateIndex])/N)
        
    return result[:len(stockInfo.listFromTo(fromDate,toDate))]

def BuyOrSell(s,date=None):
    """
    # U: b=BuyOrSell(s,d)
    # Pre: s is a stockInfo object, d is an optional date object, the default value of d is the most recent date we have data for.
    # Post: b is equal to 1 if buying is recommended (the 50 day moving average is above the 200 day moving average) and -1 if 
    # selling is recommended (the 50 day moving average is below the 200 day moving average) on date d.
    """       
    if date==None:
        date=s.toDate
    if not (s.validDate(date)):
        raise ValueError("Invalid date")
    shortma=movingAverage(s,50,date,date)
    longma=movingAverage(s,200,date,date)
    if shortma>longma:
        return 1
    if shortma<longma:
        return -1
    t=timedelta(days=1)
    while shortma==longma:
        date=date-t
    return -BuyOrSell(s,date)
        # if the moving averages are equal we check which one is crossing above the other
        # and recommend buying if the 50-day is crossing over the 200-day, and selling if the opposite is true

def Beta(s, fromDate=None, toDate=None):
    """
    # U: b=Beta(s,fd,td)
    # Pre: s is stockInfo object, fd, td are optional date objects
    # Post: b is a number describing our stock's Beta value for the time period from fromDate to toDate if data exists for those dates,
    # otherwise raises exception
    """
    if fromDate==None: 
        fromDate=s.fromDate
    if toDate==None:
        toDate=s.toDate
    if not (s.validDate(fromDate) and s.validDate(toDate)):
        raise ValueError("Invalid dates")
    
    price = lambda d: d[6]
    def log_returns(l):
        """
        # U: l_r=log_returns(l)
        # Pre: l is a list of numbers, the length of which is n
        # Post: l_r is a list the length of which is one shorter than the length of l, where
        # l_r[k]=log(l[k]/l[k-1]) for k=1,...,n-1
        """
        l_r=[]           
        for i in range(1,len(l)):
            r=math.log(l[i]/l[i-1])
            l_r.append(r)
        return l_r
        
    datelist=s.listFromTo(fromDate,toDate)
    pricelist=map(price, datelist)
    SP=stockInfo("^GSPC",fromDate,toDate)
    SPlist=SP.listFromTo(fromDate,toDate)
    SPprices=map(price,SPlist)
    r_a=log_returns(pricelist)
    r_b=log_returns(SPprices)
    cov_ab=cov(array(r_a),array(r_b))[0][1] # We extract the covariance between r_a and r_b from the covariance matrix   
    return round(cov_ab,6)/round(var(array(r_b)),6) #: some error in cov or var, we must round to get correct value

if __name__ == "__main__":
    SP = stockInfo("^GSPC")
    print Beta(SP)
    #Google = stockInfo("GOOG",date(2000,1,1),date.today())
    #virkar ekki, getum ekki importad i hring.
    #smaPlot(Google,fromDate = date(2010,1,2), toDate = date(2011,1,2)).show()
