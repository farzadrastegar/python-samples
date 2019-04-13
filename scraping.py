from lxml import html
import requests
import socket
from itertools import chain

#Set the URL that contains websites' ranks
url = "http://www.alexa.com/topsites/countries;PAGE/IR"
#Note: this url is not available now. See how it looked liked from goole cached websites here:
#https://webcache.googleusercontent.com/search?q=cache:lH2VVNOLs2IJ:https://www.alexa.com/topsites/countries/IR+&cd=3&hl=en&ct=clnk&gl=ua

#Extract all the websites in the first 20 pages (ordered descendingly) from the URL
webranks = []
for page in range(20):
	pageURL = url.replace("PAGE", str(page))
	page = requests.get(pageURL)
	tree = html.fromstring(page.content)
	pagelist = tree.xpath('//p[@class="desc-paragraph"]/a/text()')
	webranks.append(pagelist)

#Set ranks for the extracted websites
ranks = range(1, len(webranks)+1)

#Extract the IP of those websites if available
webranksIP = []
for w in webranks:
	try:
		webranksIP.append(socket.gethostbyname(w))
	except:
		webranksIP.append("")

#Print rank, website, website's IP
print(["%s\t%s\t%s" % t for t in list(zip(ranks, webranks, webranksIP))])


