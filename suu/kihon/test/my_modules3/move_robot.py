from ROV_Motor import ROV_Motor

p_threshold = 0.5
m_threshold = -0.5


#def move_robot(motor, obj):
def move_robot(motor, obj, auto_flag):
	print(auto_flag)
	if auto_flag == False:
		if obj['joy_rx'] >= m_threshold and obj['joy_rx'] <= p_threshold and obj['joy_ry'] <= m_threshold:
			motor.rise( (obj) )
		elif obj['joy_rx'] >= m_threshold and obj['joy_rx'] <= p_threshold and obj['joy_ry'] >= p_threshold:
			motor.descend( (obj) )
		else:
			motor.setup(4)
			motor.setup(5)
	
	
	if obj['joy_lx'] >= m_threshold and obj['joy_lx'] <= p_threshold and obj['joy_ly'] <= m_threshold:
		motor.forward( (obj) )
	elif obj['joy_lx'] >= m_threshold and obj['joy_lx'] <= p_threshold and obj['joy_ly'] >= p_threshold:
		motor.reverse( (obj) )
	elif obj['joy_lx'] >= p_threshold and obj['joy_ly'] >= m_threshold and obj['joy_ly'] <= p_threshold:
		motor.right_mov( (obj) )
	elif obj['joy_lx'] <= m_threshold and obj['joy_ly'] >= m_threshold and obj['joy_ly'] <= p_threshold:
		motor.left_mov( (obj) )
	elif obj['joy_rx'] >= p_threshold and obj['joy_ry'] >= m_threshold and obj['joy_ry'] <= p_threshold:
		motor.turn_right( (obj) )
	elif obj['joy_rx'] <= m_threshold and obj['joy_ry'] >= m_threshold and obj['joy_ry'] <= p_threshold:
		motor.turn_left( (obj) )
	else:
		for i in range(4):
			motor.setup(i)
  
	if obj['btn_5'] == 1:
		motor.arm_open()	
	elif obj['btn_6'] == 1:
		motor.arm_close()	

if __name__ == '__main__':
	robot = ROV_Motor()
	obj = {
		"joy_lx" : 0.5,
		"joy_ly" : 0.5,
		"joy_rx" : 0.5,
		"joy_ry" : 0.5,
		}

	args = ( robot, obj )

	print("command 0 : stop")
	print("command 1 : forward")
	print("command 2 : reverse")
	print("command 3 : right_move")
	print("command 4 : left_move")
	print("command 5 : trun_right")
	print("command 6 : trun_left")
	print("command 7 : rise")
	print("command 8 : descend")

	while True:
		print("please command!")
		number = input()
		number = int(number)

		if number == 1:
			obj["joy_lx"] = 0
			obj["joy_ly"] = -0.75
			obj["joy_rx"] = 0
			obj["joy_ry"] = 0
			print(obj)
			move_robot(*args)
		elif number == 2:
			obj["joy_lx"] = 0
			obj["joy_ly"] = 0.75
			obj["joy_rx"] = 0
			obj["joy_ry"] = 0
			print(obj)
			move_robot(*args)
		elif number == 3:
			obj["joy_lx"] = 0.75
			obj["joy_ly"] = 0
			obj["joy_rx"] = 0
			obj["joy_ry"] = 0
			print(obj)
			move_robot(*args)
		elif number == 4:
		 obj["joy_lx"] = -0.75
		 obj["joy_ly"] = 0
		 obj["joy_rx"] = 0
		 obj["joy_ry"] = 0
		 print(obj)
		 move_robot(*args)
		elif number == 5:
		 obj["joy_lx"] = 0
		 obj["joy_ly"] = 0
		 obj["joy_rx"] = 0.75
		 obj["joy_ry"] = 0
		 print(obj)
		 move_robot(*args)
		elif number == 6:
		 obj["joy_lx"] = 0
		 obj["joy_ly"] = 0
		 obj["joy_rx"] = -0.75
		 obj["joy_ry"] = 0
		 print(obj)
		 move_robot(*args)
		elif number == 7:
		 obj["joy_lx"] = 0
		 obj["joy_ly"] = 0
		 obj["joy_rx"] = 0
		 obj["joy_ry"] = -0.75
		 print(obj)
		 move_robot(*args)
		elif number == 8:
		 obj["joy_lx"] = 0
		 obj["joy_ly"] = 0
		 obj["joy_rx"] = 0
		 obj["joy_ry"] = 0.75
		 print(obj)
		 move_robot(*args)
		else :
		 obj["joy_lx"] = 0
		 obj["joy_ly"] = 0
		 obj["joy_rx"] = 0
		 obj["joy_ry"] = 0
		 print(obj)
		 move_robot(*args)
