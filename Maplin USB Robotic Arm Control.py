#!/usr/bin/python

import usb.core, sys, time
from Tkinter import *

class USBControl:
	
	def connecttoarm(self):
		''' 	connects to the Maplin USB Robotic Arm
			returns Device not found error if unable to connect
		'''
		dev = usb.core.find(idVendor=0x1267, idProduct=0x0000)
		
		if dev is None:
			raise ValueError('Device not found')           # if device not found report an error
	
		print 'Robotic Arm Connected...'
	
		# configure device
		dev.set_configuration()

		return dev
		
	def buildcommand(self,shoulder=0, elbow=0, wrist=0, grip=0, rotate=0, light=0):
		'''	creates the code to send to USB robot arm
			usage buildcommand(shoulder,elbow,wrist,grip,rotate,light) 
			where 	shoulder,elbow,wrist,are 0,1,2
					0 = off/stop.  1=motor up.   2=motor down
				grip is 0,1,2
					0 = off/stop.  1=close.   2=open
				rotate is 0,1,2
					0 = off/stop.  1=rotate c/wise.   2=rotate c/cwise
				light is 0,1
					0 is off.   1 is on.
			values default to 0 if not set.
		'''
		#print str(shoulder), str(elbow).rjust(5), str(wrist).rjust(5), str(grip).rjust(5), str(rotate).rjust(5), str(light).rjust(5)

		# first check parameters are valid		
		if shoulder not in range(0,3): raise ValueError('Shoulder out of range')
		if elbow not in range(0,3): raise ValueError('Elbow out of range')
		if wrist not in range(0,3): raise ValueError('Wrist out of range')
		if grip not in range(0,3): raise ValueError('Grip out of range')
		if rotate not in range(0,3): raise ValueError('Rotate out of range')
		if light not in range(0,3): raise ValueError('Light out of range')

		# create the bytes 
		byte1 = (shoulder<<6)+ (elbow<<4) + (wrist<<2) + (grip)
		byte2 = (rotate)
		byte3 = (light)

		# return the bytes

		thebytes = [byte1, byte2, byte3]
		return thebytes

	def sendcommand(self,device, command='0,0,0') :
		''' 	writes the command to the device (as a USB Command type)
			if no command is given three O characters are used which stops motors etc
			returns number of bytes written
		'''
		timeout=1000
		return device.ctrl_transfer(0x40, 6, 0x100, 0, command, timeout)
		
class App:
	
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()
		
		self.light = 1
		
		self.x = USBControl()
		self.dev = self.x.connecttoarm()

		self.quit = Button(frame, text="QUIT", fg="red", command=frame.quit).pack(side=LEFT)

		self.GripOpen = Button(frame, text="Open Grip", command=self.gripOpen).pack(side=LEFT)
		self.gripclose = Button(frame, text="close Grip", command=self.gripClose).pack(side=LEFT)
		self.stopActuators = Button(frame, text="Stop Actuators", command=self.stop).pack(side=LEFT)
		self.light = Button(frame, text="Light", command=self.Light).pack(side=LEFT)
		self.baseClockwise = Button(frame, text='Base Clockwise', command=self.baseClockwise).pack(side=LEFT)
		self.baseCounterClockwise = Button(frame, text='base Counter Clockwise', command=self.baseCounterClockwise).pack(side=LEFT)
		self.WristUp = Button(frame, text='Wrist Up', command=self.wristUp).pack(side=LEFT)
		self.wristdown = Button(frame, text='Wrist Down', command=self.wristDown).pack(side=LEFT)
		self.elbowUp = Button(frame, text='Elbow Up', command=self.elbowUp).pack(side=LEFT)
		self.elbowDown = Button(frame, text='Elbow Down', command=self.elbowDown).pack(side=LEFT)
		self.shoulderUp = Button(frame, text='Shoulder Up', command=self.shoulderUp).pack(side=LEFT)
		self.shoulderDown = Button(frame, text='Shoulder Down', command=self.shoulderDown).pack(side=LEFT)

		
		print 'initiating communication...'
		print 'Data:'
		
	def shoulderUp(self):
		self.cmd = self.x.buildcommand(1,0,0,0,0,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '100000'
		
	def shoulderDown(self):
		self.cmd = self.x.buildcommand(2,0,0,0,0,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '200000'

	def elbowUp(self):
		self.cmd = self.x.buildcommand(0,1,0,0,0,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '010000'	
		
	def elbowDown(self):
		self.cmd = self.x.buildcommand(0,2,0,0,0,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '020000'			

	def wristUp(self):
		self.cmd = self.x.buildcommand(0,0,1,0,0,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '001000'
		
	def wristDown(self):
		self.cmd = self.x.buildcommand(0,0,2,0,0,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '001000'

	def Light(self):
		if self.light == 1:
			self.light = 0
			self.cmd = self.x.buildcommand(0,0,0,0,0,1)
			print '000001'
		else:
			self.light = 1
			self.cmd = self.x.buildcommand(0,0,0,0,0,0)
			print '000000'
			
		self.x.sendcommand(self.dev, self.cmd)
		
	def baseCounterClockwise(self):
		self.cmd = self.x.buildcommand(0,0,0,0,2,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '000020'
		
	def baseClockwise(self):
		self.cmd = self.x.buildcommand(0,0,0,0,1,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '000010'
		
	def gripOpen(self):
		self.cmd = self.x.buildcommand(0,0,0,2,0,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '000200'

	def gripClose(self):
		self.cmd = self.x.buildcommand(0,0,0,1,0,0)
		self.x.sendcommand(self.dev, self.cmd)
		print '000100'

	def stop(self):
		print '000000'
		self.x.sendcommand(self.dev)
		
def main():
	root = Tk()
	app = App(root)
	root.mainloop()
	
if __name__== '__main__':
	main()
