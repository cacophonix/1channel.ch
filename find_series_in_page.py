from bs4 import BeautifulSoup
import opener
import re


def i_have_gotten_page_number(url):
	
	data=opener.fetch(url)['data']
	soup=BeautifulSoup(data)
	
	l=soup.find_all('a')
	
	reg=re.compile(r'.*/watch.*')
	
	for i in l:
		
		if not i.has_key('href'):
			continue;
			
		link =i.get('href')
		
		m=reg.match(link)
		if m:
			print m.group(0)


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
	
	for i in range(1,page_count+1):
		new_url=url+"&page="+str(i)
		print new_url
		
	


def tester(url):
	pass
	
	
	
	

if __name__=='__main__':
	
	i_have_gotten_page_number('http://www.1channel.ch/?letter=123&page=1')
	
	
