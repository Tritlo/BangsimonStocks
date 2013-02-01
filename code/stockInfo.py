import urllib2 as urll
import csv

class stockInfo:
    """
    An Object which contains basic infromation about stocks, via yahoo finance
    """
    
    infoDict = {} #: Dictionary containing information about the given company, for ease of checking certain dates
    infoList = [] #: A List of the form ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], containing information about the given company, for ease of creating graphs
    interval = "" #: Contains the interval which the data are for. 
    fromDate = (1,1,1970) #: The date from which the data start
    toDate = (1,1,1970) #: The date to which the data is.
    
    def __init__(self, ticker, fromDate,toDate,interval):
        """ 
        #Use: s = stockInfo(t,fd,td,i)
        #Pre: t is the companies ticker, fd = (d,m,y) is a triple of integers which specify day, month, year, td = (d,m,y) likewise, i is "w", "d", is "m", specifying the interval for which the data is accurate for.
        #Post: s is an object which contains information about the company, specified with the ticker t, from fd to td, and with accuracy of weeks, days of months depenending on whether i is "w", "d" or "m".
        """
        self.interval = interval #: nakvaemnin
        fromDay, fromMonth, fromYear = fromDate
        toDay, toMonth, toYear = toDate
        self.toDate = toDate
        self.fromDate = fromDate

        baseurl = "http://ichart.yahoo.com/table.csv?s="
        url = baseurl + ticker +"&a="+str((fromMonth -1))+"&b="+str(fromDay)+"&c="+str(fromYear)+"&d="+str(toMonth-1)+"&e="+str(toDay)+"&f="+str(toYear)+"&g="+str(interval)+"&ignore=.csv"

        csvfile = urll.urlopen(url)
        csvList = csv.reader(csvfile)
        #Hendum nofnunum 
        csvList.next()
        for d in csvList:
            self.infoDict[d[0]] = {'Open':d[1], 'High':d[2], 'Low':d[3], 'Close':d[4], 'Volume':d[5], 'Adj Close':d[6]}
            self.infoList.append(d)

    def formatDate(self,date):
        """
        #Use: h = s.formatDate(date)
        #Pre: date = (d,m,y) where d,m,y are integers which specify day, month year, s is a stockInfo object
        #Post: h is a date string of yahoo api format
        """
        day, month, year = date
        year = str(year)
        if month <10:
            month = "0"+str(month)
        else:
            month = str(month)
        if day <10:
            day = "0"+str(day)
        else:
            day = str(day)
        date = year+"-"+month+"-"+day
        return date


    def validDate(self, date):
        """ 
        #Use: b = s.validDate(date)
        #Pre: date = (d,m,y) where d,m,y are integers which specify day, month year, s is a stockInfo object
        #Post: b is true if the date is within the objects timeframe, false otherwise
        """
        if date[2] <= self.toDate[2] and date[2] >= self.fromDate[2]:
            if date[1] <= self.toDate[1] and date[1] >= self.fromDate[1]:
                    if date[0] <= self.toDate[0] and date[0] >= self.fromDate[0]:
                        return True
        return False

    def movingAverage(self, fromDate, toDate):
        pass
   
    def getDate(self,date):
        """ 
        #Use: h = s.getDate(date)
        #Pre: date = (d,m,y) where d,m,y are integers which specify day, month year, s is a stockInfo object
        #Post: h is a dictionary containing information about the given date, if it exists, None otherwise.
        """
        date = self.formatDate(date)
        if date in self.infoDict:
            return self.infoDict[date]
        else:
           #return {'Volume': 'NA', 'Adj Close': 'NA', 'High': 'NA', 'Low': 'NA', 'Close': 'NA', 'Open': 'NA'}
           return None
            
if __name__ == "__main__":
    Google = stockInfo("GOOG",(1,1,2000),(1,1,2012),"d")
    print Google.getDate((1,2,2009))
    help(Google)
