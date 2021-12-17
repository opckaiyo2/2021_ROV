import sys
sys.path.append('my_modules/')
import socket
import pickle
import Photo
import time


def camera_process(port):
	ASCII_EOT = b'\x04'

	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	s.bind( ('', int(port)) )
	s.listen()

#	print('server start!')
#	print('please access to {}port'.format(port))
	print('Camera_Process Start!')
	while True:
		try:
			soc, addr = s.accept()
			print('connect:', addr)
		except KeyboardInterrupt:
			print('End Camera Server')
			s.close()
			break
	
		with soc:
			with Photo.Photo("/dev/video0") as photo_front:
				with Photo.Photo("/dev/video1") as photo_down:
					while True:
						try:
							img = None
							command = soc.recv(1024).decode('utf-8')
						except InterruptedError:
							print('disconnect')
							break
						except ConnectionResetError:
							print('ConnectionResetError!!')
							break
					
						if( command == 'front_frame' ):
							img = photo_front.jpg_photo(50)
						if( command == 'down_frame' ):
							img = photo_down.jpg_photo(50)
						if( img is not None ):
							msg = pickle.dumps(img)
							data_length = len(msg)
							data_length = str(data_length).encode('utf-8')
							data_length += ASCII_EOT
							#print('data_length', data_length)
						
							msg = data_length + msg
							try:
								soc.sendall(msg)
							except ConnectionResetError:
								print('ConnectionResetError')
								break
						else:
							msg = pickle.dumps("None")
							data_length = len(msg)
							data_length = str(data_length).encode('utf-8')
							data_length += ASCII_EOT
							msg = data_length + msg
							print('not image!')
							try:
								soc.sendall(msg)
							except ConnectionResetError:
								print('ConnectionResetError')
								break
							break



if __name__ == '__main__':
	camera_process('5000')
