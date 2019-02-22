from bs4 import BeautifulSoup
import urllib.request
from requests_html import HTMLSession

#change the user agent so that we dont get a 403 error
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	
url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=Android&sc.keyword=Android+Developer&locT=C&locId=1128808&jobType="
headers = {'User-Agent':user_agent,} #apply the user agent here

request = urllib.request.Request(url,None,headers)
response = urllib.request.urlopen(request)
data = response.read() #this is the raw html in case it's needed
soup = BeautifulSoup(data, "lxml")
soup.prettify()
for foo in soup.findAll('a', href=True):
	print (foo['href'])