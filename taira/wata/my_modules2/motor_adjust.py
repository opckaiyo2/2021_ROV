from ROV_Motor import ROV_Motor

old_cmd = None

def input_cmd():
	global old_cmd
	cmd = None
	val = None
	while True:
		print(">>>", end="")
		input_cmd = input()
			
		if input_cmd.isdecimal():
			cmd = int(input_cmd)
			if 0 <= cmd and cmd <= 4:
				old_cmd = cmd
				return cmd, val
			else:
				print('{0} is not command! Re-enter.'.format(input_cmd))

		elif input_cmd == 'duty':
			cmd = input_cmd
			while True:
				print('set duty (0.0 - 1.0)')
				print('>>>', end='')
				duty = input()
				duty = float(duty)
				if 0.0 <= duty and duty <= 1.0:
					return cmd, duty
				else:
					print('{0} is not duty!'.format(duty))

		elif input_cmd.startswith('pin'):
			pin    = int(input_cmd[3])
			offset = int(input_cmd[5:])
			if 0 <= pin and pin <= 5:
				return input_cmd[:4], offset

		elif input_cmd.startswith('file'):
			return input_cmd, old_cmd

		elif input_cmd.startswith('help'):
			return input_cmd, None
		elif input_cmd == 'exit':
			exit(0)
		else:
			print("{0} is not command! Re-enter.".format(input_cmd))
	return cmd


def adjust():
	global old_cmd
	motor = ROV_Motor()
	file  = open('offset_adjust.txt', 'w')

	offset = {
		"pin0" : 0,
		"pin1" : 0,
		"pin2" : 0,
		"pin3" : 0,
		"pin4" : 0,
		"pin5" : 0,
	}

	description = "this program is for adjusting motor output.\n"
	cmd_desc    = "cmd : 0           desc = stop\n"
	cmd_desc   += "cmd : 1           desc = forward \n"
	cmd_desc   += "cmd : 2           desc = reverse \n"
	cmd_desc   += "cmd : 3           desc = right_mov \n"
	cmd_desc   += "cmd : 4           desc = left_mov \n"
	cmd_desc   += "cmd : pin? offset desc = set offset\n"
	cmd_desc   += "cmd : duty        desc = set duty \n"
	cmd_desc   += "cmd : file        desc = write down \n"
	cmd_desc   += "cmd : help        desc = command_help\n"

	adjust_desc  = ""
	cmd = 0
	duty = 0.1

	print("adjusting start!!\n")
	print(description)
	print(cmd_desc)
	while True:
		print("\nplease command")
		try:
			cmd, val = input_cmd()
		except:
			print('end program.')
			break

		if cmd == 0:
			motor.stop()
		elif cmd == 1:
			motor.auto_forward(*(duty, offset))
		elif cmd == 2:
			motor.auto_reverse(*(duty, offset))
		elif cmd == 3:
			motor.auto_right_mov(*(duty, offset))
		elif cmd == 4:
			motor.auto_left_mov(*(duty, offset))
		elif cmd == 'duty':
			print('set duty : ', val)
			duty = val
		elif cmd.startswith('pin'):
			offset[cmd] = val
			print(offset)
			if old_cmd == 1:
				motor.auto_forward(*(duty, offset))
			elif old_cmd == 2:
				motor.auto_reverse(*(duty, offset))
			elif old_cmd == 3:
				motor.auto_right_mov(*(duty, offset))
			elif old_cmd == 4:
				motor.auto_left_mov(*(duty, offset))
		elif cmd == 'file':
			msg = None
			if   val == 1:
				msg = "forward offset\n"
			elif val == 2:
				msg = "reverse offset\n"
			elif val == 3:
				msg = "right_mov offset\n"
			elif val == 4:
				msg = "left_mov offset\n"
			else:
				msg = " offset\n"
			msg += '{}\n'.format(offset)
			file.write(msg)
			print('write down \'offset_adjust.txt\'')
		elif cmd == 'help':
			print(cmd_desc)

if __name__ == '__main__':
	offset = {
		"pin_0" : 0,
		"pin_1" : 0,
		"pin_2" : 0,
		"pin_3" : 0,
		"pin_4" : 0,
		"pin_5" : 0,
	}

	#cmd = input_cmd()
	#print(cmd)
	adjust()
