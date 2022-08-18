import xlrd
import requests
from bs4 import BeautifulSoup
import threading

class ErrorSite:
    """
    class for store information from site
    stored url and satus code (Code or description)
    example:
    url = https://www.google.ru
    status = "402"
    """
    def __init__(self, url, status) :
        self.url = url
        self.status = status
        
    def getUrl(self):
        return self.url

    def getStatus(self):
        return self.status

#open excel file with site list
sitelist = xlrd.open_workbook("sites.xls")

#Open sheet
sitesheet = sitelist.sheet_by_index(0)

#Result dict with ErrorSite object
result = []

def getHttpStatusCode(url):
    """return http status code ex 200,302,301 or zero if we can't to connect to site

    Args:
        url (String): url exmp: https://www.google.com

    Returns:
        int: htp status code
    """
    try:
        statusCode = requests.head(url)
        return statusCode.status_code
    except requests.ConnectionError:
        return 0

def checkTitle(url, title):
    """
    :param url: This is url addresss which we are checks
    :param title: Title we are using for check that site is alive, and we aren't get dummy page from our provider
    :return: if title matches return True, otherwise return false
    """
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for titleInSite in soup.find_all('title'):
        if titleInSite.getText() == title:
            return True
    return False

def checkSiteStatus(url, title):
    """this function checks url if alive and title matches the specified 

    Args:
        url (String): url exmp: https://www.google.com
        title (String): Specified value, this value we are checks in html tag <title> </title>
    """
    statusCode = getHttpStatusCode(url)
    if statusCode != 200:
        if statusCode == 0:
           statusCode = "Connection error"
           
        errorSite = ErrorSite(url, statusCode)
        result.append(errorSite)
        
    else:
        if not checkTitle(url, title):
            errorSite = ErrorSite(url, "Title doesn't match")
            result.append(errorSite)

threads = [] #thread array for store all threads
for i in range(0, sitesheet.nrows):
    url = sitesheet.cell_value(i, 0)
    title = sitesheet.cell_value(i,1)    
    threads.append(threading.Thread(target=checkSiteStatus, args=(url,title)))

#start all threads
for thread in threads:
    thread.start()
#wait all threads
for thread in threads:
    thread.join()
    
#print result dict
if not result:
    print("Good day! Nothing is bad")
for errorSite in result:
    print("Site: ", errorSite.getUrl(), "Status: ", errorSite.getStatus())