from google.appengine.api import urlfetch
import urllib
_GROUPME_URL = 'http://groupme.com/api/'
class Bot:
	"""docstring for GroupMe"""
	def __init__(self, token, phone_number):
		self.token = token
		#best to take this directly from what groupme sends in
		self.phone_number = phone_number

	#data is a dictionary
	def send_message(self, text):
		url = _GROUPME_URL + self.phone_number + '?token=' + self.token
		return urlfetch.fetch(url = url, method = urlfetch.POST, payload = urllib.urlencode( {'text':text} ), deadline = 10)