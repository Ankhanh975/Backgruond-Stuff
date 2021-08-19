import win32api, win32con, win32gui
import pyautogui, keyboard
import pygame
import time, random, sys, os, math
from Sub_Method import *
from Preprocess_instruction import *
from Condition import *
import _List

class GetInput():
	def __init__(self, data: dict):
		self.screenSize = [pyautogui.size()[0], pyautogui.size()[1]]
		self.NeedCheckedKey = []
		self.Instruction = data
		self.UsingKey(data)
		self.VK_CODE_REVERSE = _List.VK_CODE_REVERSE
		self.VK_CODE = _List.VK_CODE

		self.Global_HoldKey = []
		self.Global_MousePos = [-1,-1]
		self.Global_ActiveWindow = "None"
		
	def Update(self):
		flags, hcursor, self.Global_MousePos = win32gui.GetCursorInfo()
		self.Global_ActiveWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
		self.Global_HoldKey = self.getKeyState()

	def UsingKey(self, data):
		def KeyboardInUse(data, turnToNumbers=True):
			# data is a json from original .yaml->dict file
			Z=[]
			data = JsonToTxt(data)
			data = data.split("\n")
			for x in data:
				if ("keypress" in x) or ("switchevent" in x):
					n=x
					n = n.replace("keypress", "")
					n = n.replace("switchevent", "")
					n = n.replace('"', "")
					n = n.replace(" ", "")
					n = n.replace(",", "")
					n = n.replace(":", "")
					Z+=Loadyaml.LoadKeyStrokes(n)

			Z.append("lbutton")
			Z.append("rbutton")
			Z.append("mbutton")
			if turnToNumbers:
				import _List
				Z2=[]
				for x in range(len(Z)):
					Z2.append(self.VK_CODE_REVERSE.index(Z[x]))

				return Z2
			else:
				return Z
		self.NeedCheckedKey = KeyboardInUse(data)
		return KeyboardInUse(data)

	def IsPressed(CheckKeyStrokes):
	    for x in CheckKeyStrokes:
	        if x not in self.Global_HoldKey:
	                return False
	    return True

	def getKeyState(self):
	    keyPressed = []
	    if self.NeedCheckedKey==[]:
	        for x in range(256):
	            a = win32api.GetKeyState(x)
	            if a<0 and self.VK_CODE_REVERSE[x] !=None:
	                keyPressed.append(self.VK_CODE_REVERSE[x])
	    else:
	        for x in self.NeedCheckedKey:
	            a = win32api.GetKeyState(x)
	            if _List.VK_CODE_REVERSE[x] !=None:
	                if a<0: 
	                    keyPressed.append(self.VK_CODE_REVERSE[x])
	            else:
	                print(self.NeedCheckedKey, keyPressed, x, "What wrong?, why you requst a None keyNumber ")
	    return keyPressed
	def __str__(self):
		return "Global_ActiveWindow: " + str(self.Global_ActiveWindow) + ", Global_HoldKey: " + str(self.Global_HoldKey) + ", Global_MousePos: " + str(self.Global_MousePos)

	def debug(self):
		print("screenSize:", self.screenSize)
		print("NeedCheckedKey:", self.NeedCheckedKey )
		print("Global_HoldKey:", self.Global_HoldKey )
		print("Global_MousePos:", self.Global_MousePos )
		print("Global_ActiveWindow:", self.Global_ActiveWindow )
		print("\n\n\n" )

#if __name__ == '__main__':
#	a= GetInput({})
#	import time
#
#	for x in range(1000):
#		a.Update()
#		a.debug()
#		time.sleep(1/60)

class Base:
	def __init__(self, tName=""):
		if tName=="": #TODO
			self.name = "id: " + str(random.randint(0,10000))
		else:
			self.name = str(tName)

		self.StartCondition = Condition()
		self.KillCondition = Condition()
		self.EventCondition = Condition()

		self.State="__init__ed"

		self.init_time = time.perf_counter()
		self.start_time = 0
		self.run_time = 0
		self.init_run_time = 0
		self.CreatedEvent = 0
		self.stop_time = None

	def Update(self, Global_HoldKey, Global_MousePos, Global_ActiveWindow):
		self.StartCondition.O_Switch.Update(Global_HoldKey)
		self.KillCondition.O_Switch.Update(Global_HoldKey)
		self.EventCondition.O_Switch.Update(Global_HoldKey)

		if self.State=="started":
			self.run_time = time.perf_counter() - self.start_time
			self.init_run_time = time.perf_counter() - self.init_time

		if self.State== "__init__ed" and self.StartCondition.IsTrue(Global_HoldKey, Global_MousePos, Global_ActiveWindow):
			self.Start()

		if self.State=="started": #TODO: only need (self.KillCondition.O_Switch.SwitchEvent == []) ?
			if not(self.KillCondition.O_Switch.SwitchEvent == [] and
				   self.KillCondition.KeyPressCondition == [] and
				   self.KillCondition.Box == None and
				   self.KillCondition.ActiveWindow == None and
				   self.KillCondition.ActiveTime == None):
				if self.KillCondition.IsTrue(Global_HoldKey, Global_MousePos, Global_ActiveWindow):
					self.Kill()

	def Start(self):
		self.start_time = time.perf_counter()
		self.run_time = 0
		self.State="started"

	def Kill(self):
		self.State="ended"
		self.stop_time = time.perf_counter()

	def Event(self, Global_HoldKey, Global_MousePos, Global_ActiveWindow):
		if self.EventCondition.IsTrue(Global_HoldKey, Global_MousePos, Global_ActiveWindow):
			if self.State == "started":
				self.CreatedEvent+=1
				return True
		return False

class Global(Base):
	def __init__(self, tFPS=60):
		super().__init__(tName="_Controller")
		self.screenSize = pyautogui.size()
		self.FPS = tFPS
		self.clock = pygame.time.Clock()
		self.frameCount = 0
		self.NeedCheckedKey = []

		self.UserInput = GetInput()

		self.running_object = 0 #TODO
		self.running_object_names = [] #TODO

	def Update(self):
		super().Update(self.Global_HoldKey, self.Global_MousePos, self.Global_ActiveWindow)
		self.frameCount +=1
		self.clock.tick(self.FPS)

		self.UserInput.Update()

	def get_fps(self):
		return round(self.clock.get_fps(), 2)

	def Kill(self):
		super().Kill()
		pygame.quit(); sys.exit()
		#TODO: sound

if __name__ == '__main__':
	a= Global()
	for b in range(1000):
		a.Update
		print()