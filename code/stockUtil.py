from datetime import date

def dateToString(date):
    """
    #Use: h = dateToString(date)        
    #Pre: date = (d,m,y) where d,m,y are integers which specify a valid  day, month, year
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
   
def stringToDate(string):
    """
    #Use: d = stringToDate(h)
    #Pre: h is a valid date string of yahoo api format
    #Post: d is a datetime.date object of the specified date. 
    """
    string = string.split("-")
    return date(int(string[0]),int(string[1]),int(string[2]))

def compareDates(d1,d2):
    """
    #Use: i = compareDates(d1,d2)
    #Pre: d1, d2 are datetime.date objects
    #Post: returns -1, 0 or 1 if d1 is less than equal or greater than d2
    """
    if d1 < d2:
        return -1
    if d1 == d2:
        return 0
    return 1

def dateSearch(d,l,i,j):
    """
    # Use: di=dateSearch(d,l)
    # Pre: d is a datetime.date object, l is an ordered list of datetime.date objects,
    # l=[d1,d2,...,dn]
    # Post: di is the first date in l which is greater than or equal to d, d[0,...,i-1]<d<=d[0,...,j]
    """
    m = i+ (j-i)/2
    if i>=j):
        return i
    if compareDates(l[m],d) < 0:
        return dateSearch(d,l,m+1,j)
    else:
        return dateSearch(d,l,i,m)



