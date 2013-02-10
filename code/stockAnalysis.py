from datetime import timedelta
from datetime import date
from numpy import *
from stockInfo import stockInfo

def movingAverage(stockInfo, fromDate, toDate,N):
    """
    #U: l = movingAverage(s,fd,td,N)
    #Pre: s is a stockInfo object, fd, td are dates, N is an integer >=0
    #Post: l is a list containing the moving averages from fd to td, if data exists for that interval, an empty list otherwise
    """
    result = []
    if not (stockInfo.validDate(fromDate) and stockInfo.validDate(toDate)):
        return []
    Ndays = timedelta(2*N) #: Have it 2*N, so that it definitely gives us enough days of data (the stock market is not continiously open)
    price = lambda d: d[6]
    for d in stockInfo.listFromTo(fromDate,toDate):
        Nprevdays = stockInfo.listFromTo(d[0]-Ndays,d[0])
        Nprevdays = map(price, Nprevdays)
        Nprevdays = Nprevdays[-20:]
        result.append(sum(Nprevdays)/len(Nprevdays)) 
        # Note that len(Nprevdays) cannot be equal to zero because if fromDate and toDate are not valid dates for the ticker
        # movingAverage would have returned an empty list above, and if fromDate didn't occur before toDate 
        # listFromto(fromDate,toDate) would be emoty so the for loop would never loop. 
            
    return result

def Beta(s, fromDate, toDate):
    """
    # U: b=Beta(s,fd,td)
    # Pre: s is stockInfo object, fd, td are dates
    # Post: b is a number describing our stock's Beta value for the time period from fromDate to toDate
    """
    
    if not (s.validDate(fromDate) and s.validDate(toDate)):
        return 0
    
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
    cov_ab=cov(array(r_a),array(r_b))[0][1]   
    
    return cov_ab/var(array(r_b))

if __name__ == "__main__":
    Google = stockInfo("GOOG",date(2000,1,1),date(2013,1,1))
    
    print Beta(Google, date(2012,6,7),date(2012,12,31))
