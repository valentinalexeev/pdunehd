import requests
import re

BASE_COMMAND_URL_FORMAT = "http://{}/cgi-bin/do"

PLAYBACK_SPEED_PLAY = 256
PLAYBACK_SPEED_PAUSE = 0
PLAYBACK_SPEED_FFWD = 512
PLAYBACK_SPEED_RWD = -512

STATE_PARSER = re.compile('.*name="(.*)" value="(.*)"')

TIMEOUT = 5

class DuneHDPlayer():
	def __init__(self, address):
		self._address = address

	def launch_media_url(self, mediaUrl):
		return self.__send_command('launch_media_url', {'media_url': mediaUrl})

	def play(self):
		return self.__change_playback_speed(PLAYBACK_SPEED_PLAY)

	def pause(self):
		return self.__change_playback_speed(PLAYBACK_SPEED_PAUSE)

	def ffwd(self):
		return self.__change_playback_speed(PLAYBACK_SPEED_FFWD)

	def rwd(self):
		return self.__change_playback_speed(PLAYBACK_SPEED_RWD)

	def stop(self):
		return self.__send_command('standby')

	def update_state(self):
		state = self.__send_command('status')
		if state.get('playback_url'):
			state['playback_url'] = state['playback_url'].encode('latin1').decode('utf8')
		return state

	def turn_on(self):
		return self.__send_ir_code('A05FBF00')

	def turn_off(self):
		return self.__send_ir_code('A15EBF00')

	def previous_track(self):
		return self.__send_ir_code('B649BF00')

	def next_track(self):
		return self.__send_ir_code('E21DBF00')

	def volumeUp(self):
		state = self.update_state()
		return self.__send_command('set_playback_state', {'volume': max(100, int(state.get('playback_volume', 0)) + 10)})

	def volumeDown(self):
		state = self.update_state()
		return self.__send_command('set_playback_state', {'volume': min(0, int(state.get('playback_volume', 0)) - 10)})

	def mute(self, mute = True):
		if mute:
			return self.__send_command('set_playback_state', {'mute': 1})
		else:
			return self.__send_command('set_playback_state', {'mute': 0})

	def get_last_state(self):
		return self._lastState

	def __send_ir_code(self, code):
		return self.__send_command('ir_code', { 'ir_code': code })

	def __change_playback_speed(self, newSpeed):
		return self.__send_command('set_playback_state', { 'speed': newSpeed })

	def __parse_status(self, status):
		statuses = STATE_PARSER.findall(status)
		self._lastState = { val[0]: val[1] for val in statuses }
		return self._lastState

	def __send_command(self, cmd, params = {}):
		params["cmd"] = cmd
		try:
			r = requests.get(
				BASE_COMMAND_URL_FORMAT.format(self._address),
				params = params,
				timeout = TIMEOUT
				)
		except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
			return {}

		if r.status_code == 200:
			return self.__parse_status(r.text)
		else:
			return {}