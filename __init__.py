# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All credits go to domcross (Github https://github.com/domcross)

import time

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import LOG
from mycroft import intent_file_handler

from pixel_ring import pixel_ring
from gpiozero import LED

class LEDRingRespeaker(MycroftSkill):

	def __init__(self):
		super(LEDRingRespeaker, self).__init__(name="LED Ring - Respeaker")
		self.pixel_ring = None

	def initialize(self):
		self.log.info("Pixel Ring: Initializing")
		self.power = LED(5)
		self.power.on()
		self.pixel_ring = pixel_ring
		self.pixel_ring.set_brightness(10)
		pattern = self.settings.get("theme", "mytheme1")
		self.log.info(f"Input pattern: {pattern}")
		self.pixel_ring.change_pattern(pattern)
		self.log.info(f"Set Pattern: {self.pixel_ring.pattern}")
		self.pixel_ring.wakeup()
		self.enable()

	def enable(self):
		self.log.info("Pixel Ring: Enabling")

		self.add_event('recognizer_loop:wakeword',
				self.handle_listener_wakeup)
		self.add_event('recognizer_loop:record_end',
				self.handle_listener_off)

		self.add_event('mycroft.skill.handler.start',
				self.handle_listener_think)
		self.add_event('mycroft.skill.handler.complete',
				self.handle_listener_off)

		self.add_event('recognizer_loop:audio_output_start',
				self.handler_listener_speak)
		self.add_event('recognizer_loop:audio_output_end',
				self.handle_listener_off)
		self.power.on()
		self.pixel_ring.off()

	def disable(self):
		self.log.info("Pixel Ring: Disabling")
		self.pixel_ring.off()
		self.power.off()
		self.remove_event('recognizer_loop:wakeup')
		self.remove_event('recognizer_loop:record_end')
		self.remove_event('recognizer_loop:audio_output_start')
		self.remove_event('recognizer_loop:audio_output_end')
		self.remove_event('mycroft.skill.handler.start')
		self.remove_event('mycroft.skill.handler.complete')

	def shutdown(self):
		self.log.info("Pixel Ring: Shutdown")
		self.pixel_ring.off()
		self.power.off()

	def handle_listener_wakeup(self, message):
		self.log.info("Pixel Ring: Wakeup")
		pattern = self.settings.get("theme", "mytheme1")
		self.pixel_ring.change_pattern(pattern)
		self.pixel_ring.listen()

	def handle_listener_off(self, message):
		self.log.info("Pixel Ring: Off")
		self.pixel_ring.off()

	def handle_listener_think(self, message):
		self.log.info("Pixel Ring: Think")
		pattern = self.settings.get("theme", "mytheme1")
		self.pixel_ring.change_pattern(pattern)
		self.pixel_ring.think()

	def handler_listener_speak(self, message):
		self.log.info("Pixel Ring: Speak")
		pattern = self.settings.get("theme", "mytheme1")
		self.pixel_ring.change_pattern(pattern)
		self.pixel_ring.speak()

	@intent_handler(IntentBuilder("").require("EnablePixelRing"))
	def handle_enable_pixel_ring_intent(self, message):
		self.enable()
		self.speak_dialog("EnablePixelRing")

	@intent_handler(IntentBuilder("").require("DisablePixelRing"))
	def handle_disable_pixel_ring_intent(self, message):
		self.disable()
		self.speak_dialog("DisablePixelRing")

def create_skill():
	return LEDRingRespeaker()
