import urllib2 as urll
import csv

class stockInfo:
    """
    Hlutur sem inniheldur gogn um hlutabref, sott fra yahoo finance
    """
    
    infoDict = {} #: Dictionary sem inniheldur upplysingar um fyrirtaekdi, hvers lyklar eru dagsetningar.
    infoList = [] #: Listi a forminu ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    interval = "" #: Inniheldur hver nakvaemnin er, vikur, dagar eda manudir
    fromDate = (1,1,1970) #: Dagsetning sem gognin byrja
    toDate = (1,1,1970) #: Dagsetning sem gognin na til
    
    def __init__(self, ticker, fromDate,toDate,interval):
        """ 
        #N: s = stockInfo(t,fd,td,i)
        #F: t er ticker fyrirtaekis, fd = d,m,y er dagsetning a heiltalnaformi dagur, manudur, ar og td = d,m,y er thad einnig, i er "w", "d", eda "m" 
        #E: s er hlutur sem inniheldur upplysingar um fyrirtaekid t, fra fd,fm,fy til td,tm,ty og med nakvaemninni vikur ef i er "w", dogum ef i er "d" og manudum ef i er "m".
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
        #N: h = s.formatDate(d,m,y)
        #F: d er heiltala sem taknar dag, m er heiltala sem taknar manud og y er heiltala sem taknar ar, s er stockInfo hlutur
        #E: h er dagsetning a yahoo api. formi
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
        """ #N: b = s.validDate(d,m,y)
            #F: d,m,y er a dagsetningar formi, dagur, manudur ,ar
            #E: b er true ef dagsetningin er innan timarammans, false annars
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
        #N: h = s.getDate(d,m,y)
        #F: d er heiltala sem taknar dag, m er heiltala sem taknar manud og y er heiltala sem taknar ar.
        #E: h er dict sem inniheldur upplysingar um gefin dag, ef upplysingar eru til um hann, en None annars
        """
        date = self.formatDate(date)
        if date in self.infoDict:
            return self.infoDict[date]
        else:
           #return {'Volume': 'NA', 'Adj Close': 'NA', 'High': 'NA', 'Low': 'NA', 'Close': 'NA', 'Open': 'NA'}
           return None
            
if __name__ == "__main__":
    Google = stockInfo("GOOG",1,1,2000,1,1,2012,"d")
    print Google.getDate(1,2,2009)
