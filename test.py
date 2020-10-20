from pynput import keyboard
import Quartz

kSystemDefinedEventMediaKeysSubtype = 8

mediaPause = 16
mediaSkipForward = 19
mediaSkipBackwards = 20

def handler(event_type, event):
	if event_type == Quartz.NSSystemDefined:
		sys_event = Quartz.NSEvent.eventWithCGEvent_(event)
		if sys_event.subtype() == kSystemDefinedEventMediaKeysSubtype:
			key = ((sys_event.data1() & 0xffff0000) >> 16)
			print(sys_event.data2())
			print(key)
			return

	return event


with keyboard.Listener(darwin_intercept = handler) as listener:
	listener.join()
