import sys
import Adafruit_PCA9685



class ROV_Motor:
	def __init__(self):
		self.pca = Adafruit_PCA9685.PCA9685(address = 0x40)
		self.pca.set_pwm_freq(69) #72Hz
		#setting
		self.POWER       = 0.5
		self.standard    = 442  #duty 9.8% motor stoped
		self.max_rotain  = 30   #duty width 25
		#offset
		self.m0 = 10
		self.m1 = 10
		self.m2 = 10
		self.m3 = 10
		self.m4 = 10
		self.m5 = 10
		#for ARM
		self.arm_cnt = 100 
		self.arm_set()
		
		for i in range(16):
			self.setup(i)

	def reverse_rotation(self, pin, joystick_value, offset):
		if joystick_value < 0:
			power = joystick_value * -1
		else:
			power = joystick_value
			
		operation =  self.standard + self.max_rotain * power
		self.pca.set_pwm(pin, 0, int(operation + offset))

	def forward_rotation(self, pin, joystick_value, offset):
		if joystick_value < 0:
			power = joystick_value * -1
		else:
			power = joystick_value
			
		operation = self.standard - self.max_rotain * power
		self.pca.set_pwm(pin, 0, int(operation  - offset))


	def all_duty0(self):
		for i in range(16):
			self.pca.set_pwm(i,0,4096)

	def resolution2duty(self, val):
		duty = float( abs(val / self.max_rotain) )
		return duty

	def setup(self, pin):
		self.pca.set_pwm(pin,0,self.standard)

	def setup2duty(self, pin, duty):
		self.pca.set_pwm(pin,0, int(self.standard + self.max_rotain * duty))

	#remote
	def forward(self,data):
		self.reverse_rotation(0, data['joy_ly'], 10)
		self.forward_rotation(1, data['joy_ly'], 0)
		self.forward_rotation(2, data['joy_ly'], 0)
		self.reverse_rotation(3, data['joy_ly'], 8)

	def reverse(self,data):
		self.forward_rotation(0,data['joy_ly'], 0)
		self.reverse_rotation(1,data['joy_ly'], 10)
		self.reverse_rotation(2,data['joy_ly'], 0)
		self.forward_rotation(3,data['joy_ly'], 10)

	def right_mov(self,data):
		self.reverse_rotation(0,data['joy_lx'], 0)
		self.reverse_rotation(1,data['joy_lx'], 0)
		self.reverse_rotation(2,data['joy_lx'], 13)
		self.reverse_rotation(3,data['joy_lx'], 13)

	def left_mov(self,data):
		self.forward_rotation(0,data['joy_lx'], 10)
		self.forward_rotation(1,data['joy_lx'], 0)
		self.forward_rotation(2,data['joy_lx'], 0)
		self.forward_rotation(3,data['joy_lx'], 10)

	def turn_right(self,data):
		rotate = 0.9
		self.forward_rotation(0,rotate, 0)
		#self.forward_rotation(1,rotate, 0)
		#self.forward_rotation(2,rotate, 0)
		self.reverse_rotation(3,rotate, 0)

	def turn_left(self,data):
		rotate = 0.9
		#self.reverse_rotation(0,rotate, 0)
		self.reverse_rotation(1,rotate, 0)
		self.forward_rotation(2,rotate, 0)
		#self.reverse_rotation(3,rotate, 0)

	def rise(self,data):
		self.forward_rotation(4,data['joy_ry'], 0)
		self.forward_rotation(5,data['joy_ry'], 0)

	def descend(self,data):
		self.reverse_rotation(4,data['joy_ry'], 0)
		self.reverse_rotation(5,data['joy_ry'], 0)

	####auto
	def auto_forward(self,val,offset):
		self.reverse_rotation(0, val, offset['pin0'])
		self.forward_rotation(1, val, offset['pin1'])
		self.forward_rotation(2, val, offset['pin2'])
		self.reverse_rotation(3, val, offset['pin3'])

	def auto_reverse(self,val,offset):
		self.forward_rotation(0,val, offset['pin0'])
		self.reverse_rotation(1,val, offset['pin1'])
		self.reverse_rotation(2,val, offset['pin2'])
		self.forward_rotation(3,val, offset['pin3'])

	def auto_right_mov(self,val,offset):
		self.reverse_rotation(0,val, offset['pin0'])
		self.reverse_rotation(1,val, offset['pin1'])
		self.reverse_rotation(2,val, offset['pin2'])
		self.reverse_rotation(3,val, offset['pin3'])

	def auto_left_mov(self,val,offset):
		self.forward_rotation(0,val, offset['pin0'])
		self.forward_rotation(1,val, offset['pin0'])
		self.forward_rotation(2,val, offset['pin0'])
		self.forward_rotation(3,val, offset['pin0'])

	def auto_turn_right(self,val):
		self.forward_rotation(0,val, 0)
		#self.forward_rotation(1,val, 0)
		#self.forward_rotation(2,val, 0)
		self.reverse_rotation(3,val, 0)

	def auto_turn_left(self,val):
		#self.reverse_rotation(0,val, 0)
		self.reverse_rotation(1,val, 0)
		self.forward_rotation(2,val, 0)
		#self.reverse_rotation(3,val, 0)

	def auto_rise(self,val):
		self.reverse_rotation(4,val, 0)
		self.forward_rotation(5,val, 0)

	def auto_descend(self,val):
		self.forward_rotation(4,val, 0)
		self.reverse_rotation(5,val, 0)
	###
	
	def stop(self):
		for i in range(16):
			self.setup(i)
	#for ARM
	def arm_set(self):
	 self.pca.set_pwm(8, 0, 350 + self.arm_cnt)
	 self.pca.set_pwm(9, 0, 350 - self.arm_cnt)

	def arm_open(self):
	 if self.arm_cnt < 150:
	  self.arm_cnt += 5
	  self.arm_set()
	  print(self.arm_cnt)

	def arm_close(self):
	 if self.arm_cnt > 0:
	  self.arm_cnt -= 5
	  self.arm_set()
	  print(self.arm_cnt)







if __name__ == '__main__':
	motor = ROV_Motor()
	motor.stop()
	"""
	#single moter check
	while True:
		try:
			print("-1.0 to 1.0 value.")
			x = input()
			y = float(x)
			print(type(y), y)
			if  y <= 1.0 and y > 0:
				for pin in range(16):
					motor.setup2duty(pin, y)
			elif y < 0 and y >= -1.0:
					motor.setup2duty(pin,-y)
			else:
				print('aa')
				#morter.all_duty0()
				motor.setup()
		except KeyboardInterrupt:
			motor.all_duty0()
			break
	"""
	offset = {
		"pin0" : 10,
		"pin1" : 0,
		"pin2" : 0,
		"pin3" : 10,
		"pin4" : 0,
		"pin5" : 0
	}
	
	try:
		offs=0
		duty = 0
		print("command number")
		print("0 : stop")
		print("1 : forward")
		print("2 : reverse")
		print("3 : right_move")
		print("4 : left_move")
		print("5 : turn_right")
		print("6 : trun_left")
		print("7 : rise")
		print("8 : descend")
		while True:
			print("please command!")
			x = input()
			x = int(x)

			if x == 0:
				motor.forward_rotation(15, duty, 0) #motor 0
				motor.forward_rotation(14, duty, 0) #motor 1
				motor.forward_rotation(13, duty, 0) #motor 2
				motor.forward_rotation(12, duty, 0)
				motor.forward_rotation(11, duty, 0)
				motor.forward_rotation(10, duty, 0)
			elif x == 1:
				#motor.forward_rotation(0, duty, offset['pin0'])
				motor.forward_rotation(15, duty, 9) #-7 reverse
				motor.forward_rotation(14, duty, 9)
				motor.forward_rotation(13, duty, 12)
				motor.forward_rotation(12, duty, 9)
				motor.forward_rotation(11, duty, 9)
				motor.forward_rotation(10, duty, 9)
				#motor.reverse_rotation(0, duty, offset['pin0'])
				#motor.pca.set_pwm(0,0,2000)
			elif x == 2:
				motor.forward_rotation(1, duty, offset['pin1']) #seiten
				#motor.reverse_rotation(1, duty, offset['pin0'])
			elif x == 3:
				#motor.forward_rotation(2, duty, offset['pin2']) #seiten
				#motor.reverse_rotation(2, duty, offset['pin0']) #gyakuten
				#motor.pca.set_pwm(2,0,2000)
				#motor.forward_rotation(2, duty, offs)
				motor.forward_rotation(0, duty, 0)
			elif x == 4:
				#motor.forward_rotation(3, duty, offs)
				print("input motor num:")
				pin_n=input()
				pin_n=int(pin_n)
				pin_n=15-pin_n #0 to F 
				#motor.pca.set_pwm(pin_n,0,401+offs)
				motor.forward_rotation(pin_n, duty, offs)
				#motor.forward_rotation(3, duty, offset['pin3'])
				#motor.reverse_rotation(3, duty, offset['pin0'])
			elif x == 5:
				print("motor kosuu:")
				ko=input()	
				ko=	int(ko)
				if ko==3:
					motor.forward_rotation(15, duty, 15) #-7 reverse
					#motor.forward_rotation(14, duty, 9)
					motor.forward_rotation(12, duty, 15)
				elif ko ==4:
					motor.forward_rotation(15, duty, 10) #-7 reverse
					motor.forward_rotation(14, duty, 9)
					motor.forward_rotation(13, duty, 15)
					motor.forward_rotation(12, duty, 9)
				elif ko ==5:
					motor.forward_rotation(15, duty, 10) #-7 reverse
					motor.forward_rotation(14, duty, 9)
					motor.forward_rotation(13, duty, 15)
					motor.forward_rotation(12, duty, 9)
					motor.forward_rotation(11, duty, 9)
				elif ko == 6:
					motor.forward_rotation(15, duty, -8) #-7 reverse
					motor.forward_rotation(14, duty, 7)
					motor.forward_rotation(13, duty, 13)
					motor.forward_rotation(12, duty, 7)
					motor.forward_rotation(11, duty, 7)
					motor.forward_rotation(10, duty, -10)
				#motor.forward_rotation(4, duty, offset['pin4']) #seiten
				#motor.reverse_rotation(4, duty, offset['pin0'])
			elif x == 6:
				motor.forward_rotation(5, duty, offset['pin5'])
				#motor.reverse_rotation(5,duty, offset['pin0'])
			elif x == 7:
				a=input()
				motor.forward_rotation(15, duty, 9) #0
				a=input()
				motor.forward_rotation(15, duty, 0)
				a=input()
				motor.forward_rotation(15, duty, -9)
				a=input()
				motor.forward_rotation(15, duty, 0)
				a=input()
				motor.forward_rotation(14, duty, 9) #1
				a=input()
				motor.forward_rotation(14, duty, 0)
				a=input()
				motor.forward_rotation(14, duty, -9)
				a=input()
				motor.forward_rotation(14, duty, 0)
				a=input()
				motor.forward_rotation(13, duty, 14) #2
				a=input()
				motor.forward_rotation(13, duty, 0)
				a=input()
				motor.forward_rotation(13, duty, -14)
				a=input()
				motor.forward_rotation(13, duty, 0)
				a=input()
				motor.forward_rotation(12, duty, 9) #3
				a=input()
				motor.forward_rotation(12, duty, 0)
				a=input()
				motor.forward_rotation(12, duty, -11)
				a=input()
				motor.forward_rotation(12, duty, 0)
				a=input()
				motor.forward_rotation(11, duty, 9)
				a=input()
				motor.forward_rotation(11, duty, 0) #4
				a=input()
				motor.forward_rotation(11, duty, -11)
				a=input()
				motor.forward_rotation(11, duty, 0)
				a=input()
				motor.forward_rotation(10, duty, 10) #5
				a=input()
				motor.forward_rotation(10, duty, 0)
				a=input()
				motor.forward_rotation(10, duty, -11)
				a=input()
				motor.forward_rotation(10, duty, 0)
			elif x == 8:
				offs = offs + 1
				print(offs)
			elif x == 9:
				offs = offs - 1
				print(offs)
			else:
				motor.stop()
	except KeyboardInterrupt:
		motor.forward_rotation(15, duty, 0)
		motor.forward_rotation(14, duty, 0)
		motor.forward_rotation(13, duty, 0)
		motor.forward_rotation(12, duty, 0)
		motor.forward_rotation(11, duty, 0)
		motor.forward_rotation(10, duty, 0)
		#motor.all_duty0()
		print("end process!")