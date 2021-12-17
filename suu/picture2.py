import socketserver  
import cv2
import numpy  
import socket  
import sys
#import cv2.cv as cv  
  
class TCPHandler2(socketserver.BaseRequestHandler):  
    def handle(self):
        print('handler1')
        self.data = self.request.recv(1024).strip()
        #ret, frame=capture.read()
        ret, frame=capture2.read()
        #jpegstring=cv2.imencode('.jpg', frame)[1].tostring()
        #print(len(jpegstring),'Byte2')  
        #elf.request.send(jpegstring)
        jpegstring2=cv2.imencode('.jpg', frame)[1].tostring()
        self.request.send(jpegstring2)
        print('handler2')  
  
#hostとportを設定
HOST2 = '172.21.25.230'
PORT2 = 50001

#カメラの設定
#capture=cv2.VideoCapture()
#capture.set(3,320)
#capture.set(4,240)
capture2=cv2.VideoCapture(0)
capture2.set(3,640)
capture2.set(4,480)
if not capture2:  
    print("Could not open camera")  
    sys.exit()
socketserver.TCPServer.allow_reuse_address = True
#server = socketserver.TCPServer((HOST, PORT), TCPHandler)
server2 = socketserver.TCPServer((HOST2, PORT2), TCPHandler2)
#server.capture=capture  
server2.capture2=capture2  

try:
    #server.serve_forever()
    server2.serve_forever()    
except KeyboardInterrupt:
    pass
server2.shutdown()
print('試し')
sys.exit()