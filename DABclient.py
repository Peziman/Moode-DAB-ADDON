import sys
import time
import os
from mpdclass import MPDConnect
import requests

mode_dab = False
client = MPDConnect()
client.connect()


while True:
	if mode_dab == False:
		#dab_server()
		mode_dab = True
	else:
	#get DAB+ channel
		infolist = client.fetch_playlist()
		info = infolist[0]
		title = info['title']
		if "DAB+" in title:
			cur_ch = title.split("-")[-1]
			r = requests.get('http://localhost:7979/channel')
			if cur_ch in r.text:
				print cur_ch
			else:
				client.stop()
				p = requests.post('http://localhost:7979/channel', data = cur_ch)
				time.sleep(2)
				ra = requests.get('http://localhost:7979/channel')
				while cur_ch in ra.text == False:
					time.sleep(1)
					print "Aktueller Sender:", ra.text
					print "Voreingestelleter Sender:", cur_ch
				client.play()
		else:
			pass
		time.sleep(0.5)
