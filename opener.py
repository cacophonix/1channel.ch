import urllib2,gzip,urlparse
from StringIO import StringIO
import sys,time, random
USER_AGENT='Google-Chrome'
FETCH_TOTAL_TRY = 5

AGENTS = [
'Googlebot/2.1 (+http://www.google.com/bot.html)',
'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
'Mediapartners-Google/2.1',
'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
'DoCoMo/1.0/P502i/c10 (Google CHTML Proxy/1.0)',
'Googlebot-Image/1.0 ( http://www.googlebot.com/bot.html)'
]

t1=time.time()

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):    
	def http_error_301(self, req, fp, code, msg, headers):  
		result = urllib2.HTTPRedirectHandler.http_error_301(
			self, req, fp, code, msg, headers)              
		result.status = code                                
		return result                                       

	def http_error_302(self, req, fp, code, msg, headers):  
		result = urllib2.HTTPRedirectHandler.http_error_302(
			self, req, fp, code, msg, headers)              
		result.status = code                                
		return result                                       

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):   
	def http_error_default(self, req, fp, code, msg, headers):
		result = urllib2.HTTPError(                           
			req.get_full_url(), code, msg, headers, fp)       
		result.status = code                                  
		return result                                         


def open_anything(url,etag=None,last_modified=None,agent=USER_AGENT):

	if hasattr(url,'read'):
		return url

	if url=='-':
		return sys.stdin
	if urlparse.urlparse(url)[0]=='http':
		request=urllib2.Request(url)
		request.add_header('Accept-encoding','gzip')
		request.add_header('User-Agent',agent)

		if etag:
			request.add_header('If-None-Match',etag)

		if last_modified:
			request.add_header('If-Modified-Since',last_modified)

		opener=urllib2.build_opener(SmartRedirectHandler(), DefaultErrorHandler())

		return opener.open(request)



	try:
		return open(url)
	except (IOError,OSError):
		pass

	return StringIO(str(url))


def fetch(source, etag=None, last_modified=None, agent=USER_AGENT,fetch_try=FETCH_TOTAL_TRY):
	result = {}
	result['data']='nothing'
	try:
		f = open_anything(source, etag, last_modified, agent)
		result['data'] = f.read()
		if hasattr(f, 'headers'):
			# save ETag, if the server sent one
			result['etag'] = f.headers.get('ETag')
			# save Last-Modified header, if the server sent one
			result['lastmodified'] = f.headers.get('Last-Modified')
			if f.headers.get('content-encoding', '') == 'gzip':
				# data came back gzip-compressed, decompress it
				try:
					result['data'] = gzip.GzipFile(fileobj=StringIO(result['data'])).read()
				except:
					print '###gzip error found at %s ###' % source

		if hasattr(f, 'url'):
			result['url'] = f.url
			result['status'] = 200
		if hasattr(f, 'status'):
			result['status'] = f.status
		f.close()
	except:
		print 'open_anything failed, retry: %s' %fetch_try
		fetch_try -=1 
		if fetch_try > 0:
			result = fetch(source, None, None, random.choice(AGENTS), fetch_try)

		#~ Checking if Robot 
	if 'robot_check_container' in result['data']:
		print '@@@@@@@@@@ DUMPED with agent %s !!!!!!!! HIDE n SLEEP' %s			
		result = fetch(source,None, None, random.choice(AGENTS))
	return result 



