from bs4 import BeautifulSoup
import opener
import re
from urlparse import urlparse
from base64 import standard_b64decode



def i_have_gotten_series_episode_url(url):
	
	data=opener.fetch(url)['data']
	soup=BeautifulSoup(data)
	l=soup.find_all('a')
	reg=re.compile(r'.*?url=(.+?)&domain.*')
	reg2=re.compile(r'.*external.php.*')
	for i in l:
		if not i.has_key('href'):
			continue
		ref=i['href']
		parsed=urlparse(ref)
		try:
			t1=parsed[2]
			if not reg2.match(t1):
				continue
			m=reg.match(parsed[4])
			print standard_b64decode(m.group(1))
		except:
			pass
	



def i_have_gotten_series_name(url,name):
	
	data=opener.fetch(url)['data']
	soup=BeautifulSoup(data)
	l=soup.find_all('a')
	
	t1=url;
	t1=t1.replace('http://www.1channel.ch/watch','tv')
	t1='/'+t1+"/season-(\d+)-episode-(\d+).*"
	reg=re.compile(t1)
	
	for i in l:
		if not i.has_key('href'):
			continue
		m=reg.match(i.get('href'))
		if m:
			print m.group(0),m.group(1),m.group(2)
	




def i_have_gotten_page_number(url):
	
	data=opener.fetch(url)['data']
	soup=BeautifulSoup(data)
	l=soup.find_all('a')
	reg=re.compile(r'.*/watch-\d+-(.*)')
	for i in l:
		if not i.has_key('href'):
			continue;
		if not i.has_key('title'):
			continue;
		link =i.get('href')
		m=reg.match(link)
		if m:
			series_name=i.get('title')
			series_link="http://www.1channel.ch"+m.group(0)
			print series_name,series_link
			#~ got series name and series link


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
		#~ i have got the new url and now i have to go through all the urls
		print new_url
	


def tester(url):
	pass
	
	
	
	

if __name__=='__main__':
	
	i_have_gotten_series_name("http://www.1channel.ch/watch-9460-2020","hello")
	#~ i_have_gotten_page_number('http://www.1channel.ch/?letter=123&tv&page=1')
	#~ get_page_count_and_go_deeper('http://www.1channel.ch/?letter=123&tv')
	
	
