import requests
import re

BASE_COMMAND_URL_FORMAT = "http://{}/cgi-bin/do"

PLAYBACK_SPEED_PLAY = 256
PLAYBACK_SPEED_PAUSE = 0
PLAYBACK_SPEED_FFWD = 512
PLAYBACK_SPEED_RWD = -512

STATE_PARSER = re.compile('.*name="(.*)" value="(.*)"')

class DuneHDPlayer():
	def __init__(self, address):
		self._address = address
		self.updateState()

	def launchMediaUrl(self, mediaUrl):
		return self.__sendCommand('launch_media_url', {'media_url': mediaUrl})

	def play(self):
		return self.__changePlaybackSpeed(PLAYBACK_SPEED_PLAY)

	def pause(self):
		return self.__changePlaybackSpeed(PLAYBACK_SPEED_PAUSE)
	
	def ffwd(self):
		return self.__changePlaybackSpeed(PLAYBACK_SPEED_FFWD)

	def rwd(self):
		return self.__changePlaybackSpeed(PLAYBACK_SPEED_RWD)

	def stop(self):
		return self.__sendCommand('standby')

	def updateState(self):
		return self.__sendCommand('status')

	def getLastState(self):
		return self._lastState

	def __changePlaybackSpeed(self, newSpeed):
		return self.__sendCommand('set_playback_state', { 'speed': newSpeed })

	def __parseStatus(self, status):
		statuses = STATE_PARSER.findall(status)
		self._lastState = { val[0]: val[1] for val in statuses }
		return self._lastState

	def __sendCommand(self, cmd, params = {}):
		params["cmd"] = cmd
		r = requests.get(
			BASE_COMMAND_URL_FORMAT.format(self._address),
			params = params
			)

		if r.status_code == 200:
			return self.__parseStatus(r.text)
		else:
			raise Exception("Unable to commucate with Dune HD")