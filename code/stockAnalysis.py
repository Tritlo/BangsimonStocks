from datetime import timedelta
from datetime import date
from numpy import *
from stockInfo import stockInfo

def movingAverage(stockInfo, N=20, fromDate=None, toDate=None):
    """
    #U: l = movingAverage(s,fd,td,N)
    #Pre: s is a stockInfo object, fd, td are optional date objects, N is an optional integer >=0, the default value of N is 20.
    #Post: l is a list containing the moving averages from fd to td, if data exists for that interval, otherwise raises exception
    """
    if fromDate==None: 
        fromDate=stockInfo.fromDate
    if toDate==None:
        toDate=stockInfo.toDate
    if not (stockInfo.validDate(fromDate) and stockInfo.validDate(toDate)):
        raise ValueError("Invalid dates")
    result = []
    Ndays = timedelta(2*N) #: Have it 2*N, so that it definitely gives us enough days of data (the stock market is not continiously open)
    price = lambda d: d[6]
    for d in stockInfo.listFromTo(fromDate,toDate):
        Nprevdays = stockInfo.listFromTo(d[0]-Ndays,d[0])
        Nprevdays = map(price, Nprevdays)
        Nprevdays = Nprevdays[-N:]
        result.append(sum(Nprevdays)/len(Nprevdays)) 
        # Note that len(Nprevdays) cannot be equal to zero because if fromDate and toDate are not valid dates for the ticker
        # movingAverage would have returned an empty list above, and if fromDate didn't occur before toDate 
        # listFromto(fromDate,toDate) would be empty so the for loop would never loop. 
            
    return result

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
    
    return cov_ab/var(array(r_b))

if __name__ == "__main__":
    Google = stockInfo("GOOG",date(2000,1,1),date.today())
    
    smaPlot(Google)
