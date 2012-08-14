from bs4 import BeautifulSoup
f=open('proxy.html')
soup=BeautifulSoup(f.read())
l=soup.find_all('td')
for i in l:
	print i.string
