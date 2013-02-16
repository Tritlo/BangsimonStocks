import webbrowser
import urllib2 as urll
from datetime import date
import csv
from stockUtil import *

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
        self.infoList = []
        self.infoDict = {}

        baseurl = "http://ichart.yahoo.com/table.csv?s="
        url = baseurl + ticker +"&a="+str((fromMonth -1))+"&b="+str(fromDay)+"&c="+str(fromYear)+"&d="+str(toMonth-1)+"&e="+str(toDay)+"&f="+str(toYear)+"&g="+str(interval)+"&ignore=.csv"
        try:
            csvfile = urll.urlopen(url)
        except urll.HTTPError:
            raise ValueError("Ticker not found")
            return None
        csvList = csv.reader(csvfile)
        #Throw away the start of the list, it only contains the names of the variables
        csvList.next()
        for d in csvList:
            d[0] = stringToDate(d[0])
            for i in range(1,7):
                d[i] = float(d[i])
            self.infoDict[d[0]] = {'Open':d[1], 'High':d[2], 'Low':d[3], 'Close':d[4], 'Volume':d[5], 'Adj Close':d[6]}
            self.infoList.append(d)
        
        #Reverse the list, so it is in order by date.
        self.toDate = self.infoList[0][0]
        self.infoList.reverse()
        self.fromDate = self.infoList[0][0]



    def validDate(self, date):
        """ 
        #Use: b = s.validDate(date)
        #Pre: date is a datetime object, s is a stockinfo object
        #Post: b is true if the date is within the objects timeframe, false otherwise
        """
        if (compareDates(self.fromDate,date) <= 0) and (compareDates(date,self.toDate) <= 0):
            return True
        return False
    

    def listFromTo(self, fromDate, toDate):
       """
       #Use: l = self.listFromTo(fd,td)
       #Pre: fromDate, toDate are datetime.date objects, s is a stockinfo object
       #Post: A list containing the lists containing information about the dates in the given interval, empty if there are no such dates.
       """
       firstDateIndex = 1
       lastDateIndex = 0
       
       #Find first and last index of list we want.
       h = list(enumerate(self.infoList))
       for i, d in h:
           if compareDates(d[0],fromDate) >=0:
               firstDateIndex = i
               break
           
       for i, d in reversed(h):
           if compareDates(d[0],toDate) <=0:
               lastDateIndex = i
               break
               
       return self.infoList[firstDateIndex:lastDateIndex+1]

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
    
    def getCurrentProperty(self,propert):
        """ 
        #Use: h = s.getCurrentProperty(p)
        #Pre:  s is a stockinfo object, p is a string describing a property
        #Post: h is the current value of the property p of the stock s. 
        """
        return self.getCurrent()[propert]

    def getCurrent(self):
        """ 
        #Use: h = s.getCurrent()
        #Pre:  s is a stockinfo object
        #Post: h is a dictionary containing current information about the given stock.
        """
        baseurl = "http://download.finance.yahoo.com/d/quotes.csv?s="

        url = baseurl + self.ticker +"&f=l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7n0" +"&e=.csv"
        try:
            csvfile = urll.urlopen(url)
        except urll.HTTPError:
            raise ValueError("Ticker not found")
            return None
        csvList = csv.reader(csvfile)
        values = csvList.next()
        for i in range(len(values)):
            try:
                values[i] = float(values[i])
            except ValueError:
                pass

        data = {
                'price': values[0],
                'change': values[1],
                'volume': values[2],
                'avg_daily_volume': values[3],
                'stock_exchange': values[4],
                'market_cap': values[5],
                'book_value': values[6],
                'ebitda': values[7],
                'dividend_per_share': values[8],
                'dividend_yield': values[9],
                'earnings_per_share': values[10],
                '52_week_high': values[11],
                '52_week_low': values[12],
                '50day_moving_avg': values[13],
                '200day_moving_avg': values[14],
                'price_earnings_ratio': values[15],
                'price_earnings_growth_ratio': values[16],
                'price_sales_ratio': values[17],
                'price_book_ratio': values[18],
                'short_ratio': values[19],
                'name': values[20]
        }
        return data

    def getRSS(self):
        """ 
        #Use: h = s.getRSS()
        #Pre:  s is a stockinfo object
        #Post: h is a list of pairs with headlines and links
        """
        baseurl = "http://feeds.finance.yahoo.com/rss/2.0/headline?s="

        url = baseurl + self.ticker + "&region=US"+"&lang=en-US"
        
        try:
            news = urll.urlopen(url)
        except urll.HTTPError:
            raise ValueError("Ticker not found")
            return None
        #Get news
    
        data = news.read()
        news.close()
        #Get data from news

        string = data.split("title>")
        #Split data

        out = []
        for i in range(4,len(string)):
            if ">" not in string[i]:
                title = string[i].rstrip("/<")
                title=title.replace("&apos;","'")
                link = string[i+1].split("link>")[1].rstrip("</")
                pair = title,link
                out.append(pair)
        return out
        #Sorts out and cuts headlines

    def openURL(self):
        """
        #Use: h = s.openURL()
        #Pre: s is a stockinfo object
        #Post: h is a link to the company's information's website
        """
        profile = webbrowser.open('http://finance.yahoo.com/q/pr?s='+self.ticker+'+Profile')
        keystat = webbrowser.open('http://finance.yahoo.com/q/ks?s='+self.ticker+'+Key+Statistics')
        comp = webbrowser.open('http://finance.yahoo.com/q/co?s='+self.ticker+'+Competitors')
                                  

    def __str__(self):
        """
        #Use: y = s.__st__
        #Pre: s is a stockInfo object
        #Post:y is a string representation of the object
        """
        return "Stock information about %s, from %s to %s" % (self.ticker, dateToString(self.fromDate),dateToString(self.toDate))

            
if __name__ == "__main__":
    Google = stockInfo("GOOG",date(2000,1,1),date(2013,1,1))
    Msft = stockInfo("MSFT") 
    print Msft.fromDate
    print Msft.toDate
