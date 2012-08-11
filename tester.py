from bs4 import BeautifulSoup
import opener
import re
from urlparse import urlparse
from base64 import standard_b64decode
import MySQLdb as mdb
import sys
from datetime import datetime

con=con=mdb.connect('localhost','root','s','vidsearch')

def get_series_id_in_database(name,link,d):
	
	cur=con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT * FROM `vs_series` WHERE `series_name`=%s",name)
	res=cur.fetchone()
	if res:
		return res['series_id']
	else :
		cur.execute('INSERT INTO `vs_series`(`series_name`, `imdb_link`, `series_release_date`) VALUES (%s,%s,%s)',(name,link,d))
		return get_series_id_in_database(name,link,d)



def i_have_got_series_episode_url(name,url,season,episode):
	
	data=opener.fetch(url)['data']
	soup=BeautifulSoup(data)
	imdb_link=None
	try:
		imdb_link=soup.select('.mlink_imdb')[0].find_all('a')
		imdb_link=imdb_link[0].get('href')
	except:
		pass
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
			final_url=standard_b64decode(m.group(1))
		except:
			pass
	



def i_have_got_series_name(url,name):
	
	data=opener.fetch(url)['data']
	soup=BeautifulSoup(data)
	
	released_date=datetime.today()
	
	try:
		l=soup.select('.movie_info > table ')
		l=(l[0].find_all('tr'))
		l=l[1].find_all('td')[1].text
		released_date=datetime.strptime(l,'%B %d, %Y')
	except:
		pass
	
	
	series_id_in_database=get_series_id_in_database(name)
	
	
	
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
			episode_link="http://www.1channel.ch"+m.group(0)
			season=m.group(1)
			episode=m.group(2)
			i_have_got_series_episode_url(series_id_in_database,episode_link,season,episode)
	




def i_have_got_page_number(url):
	
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
			i_have_got_series_name(series_link,series_name)


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
		i_have_gotten_page_number(url)
	

def generate_all_the_main_page_name():
	l=[]
	l.append('http://www.1channel.ch/?letter=123&tv')
	for i in range(ord('a'),ord('z')+1):
		l.append('http://www.1channel.ch/?letter='+str(chr(i))+'&tv')
	return l




if __name__=='__main__':
	
	#~ print generate_all_the_main_page_name()
	
	i_have_got_series_name("http://www.1channel.ch/watch-9460-2020","hello")
	#~ i_have_got_page_number('http://www.1channel.ch/?letter=123&tv&page=1')
	#~ get_page_count_and_go_deeper('http://www.1channel.ch/?letter=123&tv')
	
	
