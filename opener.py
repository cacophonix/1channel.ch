import urllib2,gzip,urlparse
from StringIO import StringIO
import sys,time
USER_AGENT='GOOGLE-CHROME'

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
	
	
def fetch(source, etag=None, last_modified=None, agent=USER_AGENT):
	result = {}
	f = open_anything(source, etag, last_modified, agent)
	result['data'] = f.read()
	if hasattr(f, 'headers'):
		# save ETag, if the server sent one
		result['etag'] = f.headers.get('ETag')
		# save Last-Modified header, if the server sent one
		result['lastmodified'] = f.headers.get('Last-Modified')
		if f.headers.get('content-encoding', '') == 'gzip':
			# data came back gzip-compressed, decompress it
			result['data'] = gzip.GzipFile(fileobj=StringIO(result['data'])).read()
	if hasattr(f, 'url'):
		result['url'] = f.url
		result['status'] = 200
	if hasattr(f, 'status'):
		result['status'] = f.status
	f.close()
	return result 












