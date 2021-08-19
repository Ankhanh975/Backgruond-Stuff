import pyautogui, keyboard
import pygame
import array
import logging
import time, random, sys, os, math

def _setup_logger(tlogger_name, tlog_file, tlevel=logging.INFO, tformat='%(asctime)s - %(message)s', tfilemode='a'):
	import win32clipboard
	l = logging.getLogger(tlogger_name)
	formatter = logging.Formatter(tformat)
	fileHandler = logging.FileHandler(tlog_file, mode=tfilemode)
	fileHandler.setFormatter(formatter)
	streamHandler = logging.StreamHandler()
	streamHandler.setFormatter(formatter)

	l.setLevel(tlevel)
	l.addHandler(fileHandler)
	l.addHandler(streamHandler)

def setup_logger(tlogger_name, tlog_file, tlevel=logging.INFO, tformat='%(asctime)s - %(message)s', tfilemode='a'):
	import win32clipboard
	_setup_logger(tlogger_name, tlog_file, tlevel=logging.INFO, tformat='%(asctime)s - %(message)s', tfilemode='a')
	return logging.getLogger(tlogger_name)

def main():
	Logger = setup_logger(str(random.randint(0,100000)), "log.txt")
	print(Logger)
	for a in range(1000):
		Logger.info("Hello")
		time.sleep(1/5)

		#print()
if __name__ == '__main__':
	main()