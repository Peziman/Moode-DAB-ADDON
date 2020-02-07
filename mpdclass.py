
import sys
import time
import os
from socket import error as socket_error

# MPD Clint
from mpd import MPDClient, MPDError, CommandError, ConnectionError

# MPD Client
class MPDConnect(object):

	def __init__(self, host='localhost', port=6600):
        	self._mpd_client = MPDClient()
        	self._mpd_client.timeout = 10
        	self._mpd_connected = False

        	self._host = host
        	self._port = port

	def connect(self):
		if not self._mpd_connected:
			try:
                		self._mpd_client.ping()
            		except(socket_error, ConnectionError):
                		try:
                    			self._mpd_client.connect(self._host, self._port)
                    			self._mpd_connected = True
                		except(socket_error, ConnectionError, CommandError):
                    			self._mpd_connected = False

    	def disconnect(self):
        	self._mpd_client.close()
        	self._mpd_client.disconnect()

    	def play_pause(self):
        	self._mpd_client.pause()
        	#return False
		
	def stop(self):
		self._mpd_client.stop()
		
	def play(self):
		self._mpd_client.play()

	def next_track(self):
        	self._mpd_client.next()
        	#return False

    	def prev_track(self):
        	self._mpd_client.previous()
        	#return False
		
	def seek_plus(self):
		self._mpd_client.seekcur(+10)
		
	def seek_minus(self):
		self._mpd_client.seekcur(-10)
	
	def mute(self, oldvol = 0):
		volumestaus = self._mpd_client.status()
		oldvol = volumestaus['volume']
		if oldvol == 0:
			pass
		else:
			self._mpd_client.setvol(0)
			return oldvol
		
	def unmute(self, oldvol):
		self._mpd_client.setvol(oldvol)
		
	def repeat(self, command):
		if command == 0:
			self._mpd_client.repeat(1)
		else:
			self._mpd_client.repeat(0)
			
	def random(self, command):
		if command == 0:
			self._mpd_client.random(1)
		else:
			self._mpd_client.random(0)	

	def fetch(self):
        	# MPD current song
        	song_info = self._mpd_client.currentsong()

        	# Artist Name
        	if 'artist' in song_info:
        		artist = song_info['artist']
        	else:
            		artist = 'Unknown Artist'
        	# Song Name
        	if 'title' in song_info:
            		title = song_info['title']
        	else:
            		title = 'Unknown Title'

       	 	# MPD Status
        	song_stats = self._mpd_client.status()
        	# State
        	state = song_stats['state']
		
		#State random
		random_state = song_stats['random']
		
		#State Repeat
		repeat_state = song_stats['repeat']
		

        	# Song time
        	if 'elapsed' in song_stats:
            		elapsed = song_stats['elapsed']
            		m,s = divmod(float(elapsed), 60)
            		h,m = divmod(m, 60)
	            	eltime = "%d:%02d:%02d" % (h, m, s)
        	else:
            		eltime ="0:00:00"

       		 # Audio
        	if 'audio' in song_stats:
            		bit = song_stats['audio'].split(':')[1]
            		frequency = song_stats['audio'].split(':')[0]
            		z, f = divmod( int(frequency), 1000 )
            		if ( f == 0 ):
                		frequency = str(z)
            		else:
                		frequency = str( float(frequency) / 1000 )
            		bitrate = song_stats['bitrate']

           		audio_info =  bit + "bit " + frequency + "kHz " + bitrate + "kbps"
        	else:
            		audio_info = ""

        	# Volume
        	vol = song_stats['volume']

		return({'state':state, 'random_state':random_state, 'repeat_state':repeat_state, 'artist':artist, 'title':title, 'eltime':eltime, 'volume':int(vol), 'audio_info':audio_info})
		
	def fetch_playlist(self):
		#MPD the current Playlist
		self.pls_info = self._mpd_client.playlistinfo()
		
		return self.pls_info
		
	def save_current_playlist(self, playlist_Last):
		self._mpd_client.save(playlist_Last)
		
	def load_last_playlist(self, playlist_Last):
		self._mpd_client.load(playlist_Last)
		time.sleep(0.5)
		self._mpd_client.rm(playlist_Last)
		
	def load_playlist(self, playlist):
		self._mpd_client.stop()
		self._mpd_client.load(playlist)
		
	def fetch_current_song(self):
		song = self._mpd_client.currentsong()
		# Artist Name
        	if 'artist' in song:
            		artist = song['artist']
        	else:
            		artist = 'Unknown Artist'
        	# Song Name
        	if 'title' in song:
            		title = song['title']
        	else:
            		title = 'Unknown Title'
		# File Name
		if 'file' in song:
			file = song['file']
		else:
			file = 'no filename'
			
		return({'artist':artist, 'title':title, 'file':file})
		
