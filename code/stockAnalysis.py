from datetime import timedelta

class stockAnalysis:
    """
    Class which contains methods for analysis of stocks.
    """
    def movingAverage(self, stockInfo, fromDate, toDate,N):
        """
        #U: l = s.movingAverage(fd,td,N)
        #Pre: s is a stockAnalysis object, fd, td are dates, N is an integer >=0
        #Post: l is a list containing the moving averages from fd to td, if data exists for that interval, an empty list otherwise
        """
        result = []
        if not (stockInfo.validDate(fromDate) and stockInfo.validDate(toDate)):
            return []
        Ndays = timedelta(2*N) #: Have it 2*N, so that it definitely gives us enough days of data (the stock market is not continiously open)
        price = lambda d: (d[1] + d[4])/2
        for d in stockInfo.listFromTo(fromDate,toDate):
            Nprevdays = stockInfo.listFromTo(d[0]-Ndays,d[0])
            Nprevdays = map(price, Nprevdays)
            Nprevdays = Nprevdays[-20:]
            result.append(sum(Nprevdays)/len(Nprevdays))

        return result
