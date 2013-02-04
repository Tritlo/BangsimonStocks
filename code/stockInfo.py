import urllib2 as urll
from datetime import date
import csv

class stockInfo:
    """
    An Object which contains basic information about stocks, via yahoo finance
    """
    
    ticker = "" #: The ticker of the given company
    infoDict = {} #: Dictionary containing information about the given company, for ease of checking certain dates
    infoList = [] #: A List of the form ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], containing information about the given company, for ease of creating graphs
    interval = "d"
    fromDate = date.min #: The date from which the data start
    toDate = date.today() #: The date to which the data is.
    
    def __init__(self, ticker, fromDate = date.min ,toDate = date.today(), interval = "d"):
        """ 
        #Use: s = stockInfo(t,fd = date.min, td =date.today())
        #Pre: t is the companies ticker, fd and td are date objects. All but t are optional arguments
       #Post: s is an object which contains information about the company, specified with the ticker t, from fd to td. If fd and td are not specified, it is taken to be from as long as possible to today.
        """
        fromDay, fromMonth, fromYear = fromDate.day, fromDate.month, fromDate.year
        toDay, toMonth, toYear = toDate.day, toDate.month, toDate.year
        self.ticker = ticker
        self.interval = interval

        baseurl = "http://ichart.yahoo.com/table.csv?s="
        url = baseurl + ticker +"&a="+str((fromMonth -1))+"&b="+str(fromDay)+"&c="+str(fromYear)+"&d="+str(toMonth-1)+"&e="+str(toDay)+"&f="+str(toYear)+"&g="+str(interval)+"&ignore=.csv"
        try:
            csvfile = urll.urlopen(url)
        except urll.HTTPError:
            raise ValueError("Company not found")
            return None
        csvList = csv.reader(csvfile)
        #Throw away the start of the list, it only contains the names of the variables
        csvList.next()
        for d in csvList:
            d[0] = self.stringToDate(d[0])
            for i in range(1,7):
                d[i] = float(d[i])
            self.infoDict[d[0]] = {'Open':d[1], 'High':d[2], 'Low':d[3], 'Close':d[4], 'Volume':d[5], 'Adj Close':d[6]}
            self.infoList.append(d)
        
        #Reverse the list, so it is in order by date.
        self.toDate = self.infoList[0][0]
        self.infoList.reverse()
        self.fromDate = self.infoList[0][0]


    def dateToString(self,date):
        """
        #Use: h = s.dateToString(date)
        #Pre: date = (d,m,y) where d,m,y are integers which specify a valid  day, month, year, s is a stockinfo object
        #Post: h is a date string of yahoo api format
        """
        day, month, year = date.day, date.month, date.year
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
   
    def stringToDate(self,string):
        """
        #Use: h = s.dateToString(date)
        #Pre: h is a valid date string of yahoo api format, s is a stockinfo object
        #Post: date is a datetime.date object of the specified date. 
        """
        string = string.split("-")
        return date(int(string[0]),int(string[1]),int(string[2]))

    def compareDates(self, d1,d2):
        """
        #Use: i = s.compareDates(d1,d2)
        #Pre: d1, d2 are datetime.date objects, s is a stockinfo object
        #Post: returns -1, 0 or 1 if d1 is less than equal or greater than d2
        """
        if d1 < d2:
            return -1
        if d1 == d2:
            return 0
        return 1

    def validDate(self, date):
        """ 
        #Use: b = s.validDate(date)
        #Pre: date is a datetime object, s is a stockinfo object
        #Post: b is true if the date is within the objects timeframe, false otherwise
        """
        if (self.compareDates(self.fromDate,date) <= 0) and (self.compareDates(date,self.toDate) <= 0):
            return True
        return False
    

    def listFromTo(self, fromDate, toDate):
       """
       #Use: l = self.listFromTo(fd,td)
       #Pre: fromDate, toDate are datetime.date objects, s is a stockinfo object
       #Post: A list containing the lists containing information about the dates in the given interval, empty if there are no such dates.
       """
       return [ l for l in self.infoList if (self.compareDates(l[0], fromDate) >= 0) and  (self.compareDates(l[0],toDate) <= 0)]

    def getDate(self,date):
        """ 
        #Use: h = s.getDate(date)
        #Pre: date is a datetime object, s is a stockinfo object
        #Post: h is a dictionary containing information about the given date, if it exists, None otherwise.
        """
        if date in self.infoDict:
            return self.infoDict[date]
        else:
           return None

    def __str__(self):
        return "Stock information about %s, from %s to %s" % (self.ticker, self.dateToString(self.fromDate),self.dateToString(self.toDate))

            
if __name__ == "__main__":
    Google = stockInfo("GOOG",date(2000,1,1),date(2013,1,1))
    l = Google.listFromTo(date(2004,10,12),date(2005,1,1))
    for k in l:
        print k
