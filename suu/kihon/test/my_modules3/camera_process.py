import sys
sys.path.append('my_modules/')
import socket
import pickle
import Photo
import time


def camera_process(port):
	ASCII_EOT = b'\x04'

	cap_flag = True #raspi
	#cap_flag = False #elecom
	print('1 camera_process')
	socket.setdefaulttimeout(0.5)
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	print('2')
	s.bind( ('', int(port)) )
	print('3')
	s.listen()
	while(True):
		try:
			soc, addr = s.accept()
			break
		except socket.timeout:
			pass
		except:
			pass

#	print('server start!')
#	print('please access to {}port'.format(port))
	print('4')
	print('Camera_Process Start!')

	while True:
		cnt=0
		skip_flag=0
		print('5')
		try:
			print('6')
			print('connect:', addr)
			print('7')
	
			with soc:
				print('10 camera_process')
				with Photo.Photo("/dev/video0") as photo_front:
					print('11')
					#with Photo.Photo("/dev/video5") as photo_down:
					print('12')
					while True:
						if skip_flag==0:
							#cap_flag = not cap_flag

							print(cap_flag)
							img = None
							print('13')
							command = ""
							command = soc.recv(1024).decode('utf-8')
							print('command:',command)
							print('14')


							if(cap_flag):
								img = photo_front.jpg_photo(20)
							#else:
								#img = photo_down.jpg_photo(20)
						elif skip_flag == 1:
							print('skip')
							cap_flag=not cap_flag
							print('cap_flag:',cap_flag)
							if(cap_flag):
								img = photo_front.jpg_photo(20)
							else:
								img = photo_down.jpg_photo(20)
							skip_flag=0
					
						#if( command == 'front_frame' ):
							print('19')
						#	img = photo_front.jpg_photo(20)
							print('20')
						#if( command == 'down_frame' ):
							print('21')
						#	img = photo_down.jpg_photo(20)
							print('22')
						if( img is not None ):
							print('23')
							msg = pickle.dumps(img)
							print('24')
							data_length = len(msg)
							iflen=len(msg)
							print('iflen:',iflen)
							print('25')
							data_length = str(data_length).encode('utf-8')
							print('26')
							data_length += ASCII_EOT
							print('data_length', data_length)
							msg = data_length + msg
							# if iflen<=100:
							# 	print('continue:')
							# 	skip_flag=1
							# 	continue 
							print('27')
							#a=input()
							print('msg send cnt:',cnt)
							cnt+=1
							soc.sendall(msg)
						else:
							print("else Test camera_process")
							msg = pickle.dumps("None")
							print('30')
							data_length = len(msg)
							print('31')
							data_length = str(data_length).encode('utf-8')
							print('32')
							data_length += ASCII_EOT
							print('33')
							msg = data_length + msg
							print('34')
							print('not image!')
							soc.sendall(msg)


		except InterruptedError:
			print('15')
			print('disconnect')
			print('16')
			break

		except ConnectionResetError:
			print('17')
			print('ConnectionResetError!!')
			print('18')
			break
		
		except KeyboardInterrupt:
			print('8')
			print('End Camera Server')
			print('9')
			s.close()
			break

		except TimeoutError:
			print("timeout")
			time.sleep(1)

		except socket.timeout:
			print("timeout")
			time.sleep(1)



if __name__ == '__main__':
	camera_process('5000')