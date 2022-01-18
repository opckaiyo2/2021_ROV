import socketserver  
import cv2
import numpy  
import socket  
import sys  
  
class TCPHandler(socketserver.BaseRequestHandler):  
    def handle(self):
        self.data = self.request.recv(1024).strip()
        ret, frame=capture.read()
        jpegstring=cv2.imencode('.jpg', frame)[1].tostring()
        print(len(jpegstring),'Byte2')  
        self.request.send(jpegstring)
  
#hostとportを設定
HOST = '172.21.25.230'
PORT = 50000

#カメラの設定
capture=cv2.VideoCapture(1)
capture.set(3,640)
capture.set(4,480)
#capture2=cv2.VideoCapture(2)
#capture.set(3,320)
#capture.set(4,240)
if not capture:  
    print("Could not open camera")  
    sys.exit()
socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer((HOST, PORT), TCPHandler)
#server2 = socketserver2.TCPServer((HOST, PORT), TCPHandler)
server.capture=capture  
#server.capture2=capture21  

try:
    server.serve_forever()  
except KeyboardInterrupt:
    pass
server.shutdown()
print('試し')
sys.exit()