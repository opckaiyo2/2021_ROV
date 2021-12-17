import sys
import socket
import pickle
import configparser

import ROV_Motor
from move_robot import move_robot

def remote_process(port, auto_flag, M_lock, operation_M,):
	ASCII_EOT = b'\x04'
	p_threshold = 0.5
	m_threshold = -0.5
	old_auto_flag = False
	output        = 0

	motor = ROV_Motor.ROV_Motor()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind( ('', int(port)) )
	s.listen()

	print('Remote_Process Start!!\n')
	while True:
		try:
			print('\n\n')
			soc, addr = s.accept()
			print('connect!')
		except KeyboardInterrupt:
			print('end Server!')
			s.close()
			break

		with soc:
			while True:
				all_data    = bytes()
				data_length = bytes()
				try:
					command    = soc.recv(1024).decode('utf-8')
					

					if command == 'send_data':
						soc.sendall('OK'.encode('utf-8'))

						while True:
							d = soc.recv(1)
							if d == ASCII_EOT:
								break
							elif len(d) == 0:
								break
							data_length += d

						if len(d) == 0:
							break
						msg_length = int( data_length )

						while True:
							data = soc.recv(2048)
							all_data += data
							if msg_length == len(all_data):
								break
							elif len(data) == 0:
								break

						if len(data) == 0:
							break
						obj = pickle.loads(all_data)
						print(obj)
						#auto flag setting
						if obj['btn_11'] == 1:
							auto_flag.value = True
						elif obj['btn_1'] == 1:
							auto_flag.value = False
						
						#motor control function
						if auto_flag.value != old_auto_flag:
							output = obj['joy_ry']
							old_auto_flag = auto_flag.value
						move_robot(*(motor, obj, auto_flag.value))
						if auto_flag.value == True:
							operation =  motor.resolution2duty(operation_M['pressure'] * 0.1)
							operation += output
							if operation < 0:
								operation = 0
								motor.auto_descend(operation)
							
					else:
						soc.sendall('NO'.encode('utf-8'))
						break
				except ConnectionResetError:
					print('disconnect')
					break




if __name__ == '__main__':
#	config = configparser.ConfigParser()
#	config.read('setting.conf')
#	port = config.get('Server', 'service_port')

	port = '10000'
	remote_process(port)
