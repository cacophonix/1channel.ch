from bs4 import BeautifulSoup
import opener
import re



def get_page_count_and_go_deeper(url):
	data=opener.fetch(url)['data']
	soup=BeautifulSoup(data)
	l=soup.select('.pagination > a ')
	ref = l[len(l)-1]['href']
	reg=re.compile(r'.*?page=(\d+).*?')
	page_count=1
	m=reg.match(ref)
	if m:
		page_count=int(m.group(1))



def tester(url):
	
	
	
	
	

if __name__=='__main__':
	
	#~ tester('http://www.1channel.ch/?letter=a&tv')
	tester('tv.html')
	
