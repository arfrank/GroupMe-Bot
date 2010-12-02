#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
import groupme
import logging
from urllib import urlencode
try:
	import json
except:
	from django.utils import simplejson as json

class MainHandler(webapp.RequestHandler):
	def post(self):
		#text, name, group
		text = self.request.get('text','').lower()
		text = text.split(' ')
		msg = None
		logging.info(text)
		if text[0] == 'weather':
			msg = self.get_weather(text[1])
		bot = groupme.Bot('','')
		if msg is not None:
			bot.send_message(msg)
		
	def get(self):
		self.redirect('http://www.groupme.com')

	def get_weather(self,zip_code):
		#http://www.worldweatheronline.com/register.aspx
		weather_api_key = ''
		response = urlfetch.fetch(url = 'http://www.worldweatheronline.com/feed/weather.ashx?q='+str(zip_code)+'&format=json&num_of_days=5&key='+weather_api_key)
		logging.info(response.content)
		obj = json.loads(response.content)
		now_temp = obj['data']['current_condition'][0]['temp_F']
		now_desc = obj['data']['current_condition'][0]['weatherDesc'][0]['value']
		msg = 'N:'+now_temp+'F '+now_desc+' '
		w_list = []
		weather = obj['data']['weather']
		old_msg = msg
		for day in weather:
			if len(msg) < 160:
				old_msg = msg
				msg+= day['date'].split('-')[1]+'/'+day['date'].split('-')[2]+': +'+day['tempMaxF']+'F _'+day['tempMinF']+'F '+day['weatherDesc'][0]['value']+' '
			else:
				msg = old_msg
				break
		logging.info(msg)
		return msg
		
class Cron(webapp.RequestHandler):
	def get(self):
		if self.request.get('key') == 'TUPLE':
			bot = groupme.Bot('','')
			self.response.out.write(bot.send_message('').content)

def main():
	application = webapp.WSGIApplication([
											('/', MainHandler)
											,('/cron', Cron)
										],
										 debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
