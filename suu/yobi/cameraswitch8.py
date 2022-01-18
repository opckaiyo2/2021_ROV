import pprint
import pygame
import socket
import pickle
import sys
import time
import cv2
sys.path.append("cvui")
import cvui
import numpy as np
import numpy

class PS4Controller(object):
    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    def init(self):        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    # def send(data):
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.connect(('172.21.25.200',10000))
    #     #data = {1: "Apple", 2: "Orange"}
    #     msg = pickle.dumps(data)
    #     print(msg)
    #     s.send(msg)
    #     time.sleep(1)

    def listen(self):

        if not self.axis_data:
            self.axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
        if not self.button_data:
            self.button_data = {0: 0, 1: 0, 2: 0, 3: 0,4: 0, 5: 0, 6: 0, 7: 0 ,8: 0, 9: 0, 10: 0,11: 0,12: 0}

        def getimage():
            HOST = '172.21.25.230'
            PORT = 50000 
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
            sock.connect((HOST,PORT))   
            sock.send(('a').encode("utf-8")) 
            buf=b''
            recvlen=100 
            print(1)
            while recvlen>0:
                print(2)  
                receivedstr=sock.recv(1024)  
                recvlen=len(receivedstr)
                print(recvlen,'Byte')  
                buf +=receivedstr
                print('soket前')
            sock.close()
            print('socket後')  
            narray=numpy.frombuffer(buf,dtype='uint8')   
            return cv2.imdecode(narray,1)

        def getimage2():
            HOST2 = '172.21.25.230'
            PORT2 = 50001 
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
            sock.connect((HOST2,PORT2))   
            sock.send(('a').encode("utf-8")) 
            buf=b''
            recvlen=100
            print(1)
            while recvlen>0:
                print(2)  
                receivedstr2=sock.recv(1024)  
                recvlen=len(receivedstr2)
                print(recvlen,'Byte2')  
                buf +=receivedstr2
                print('soket前')
            sock.close()
            print('socket後')  
            narray2=numpy.frombuffer(buf,dtype='uint8')   
            return cv2.imdecode(narray2,1)

        #コントローラー

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('172.21.25.230',10020))#元のソケット

        #s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s2.connect(('172.21.25.230', 1236))
        #opencv\
        WINDOW_NAME = "CVUI Sample"
        width=1920
        height=1080
        frame = np.zeros((height, 1920, 3), np.uint8)
        is_on = False
        is_on2 = False
        # cvuiの初期化
        cvui.init(WINDOW_NAME)
        img = cv2.imread ("black.jpg",1)
        i=0
        i2=0
        m_threshold=-0.3
        p_threshold=0.3
        #opencv/
        msg = pickle.dumps(self.axis_data)
        s.send(msg)
        #msg2 = s.recv(1024)
        #print(msg2.decode("utf-8"))    
        auto = False 
        mode="None"
        mode2="stop"
        lstick=True
        frontcam=True
        autopower=0

        while True:
            img = getimage()  
            img2 = getimage2()

            
            
            #img = getimage()
            #img2 = getimage2()

            #cv2.imshow('Capture',img)  
            #cv2.imshow('Capture2',img2)

            """#print('test')
            img = getimage()                             #画面表示
            img2 = getimage()
            cv2.imshow('Capture',img)  
            cv2.imshow('Capture2',img2)  
            if cv2.waitKey(100) & 0xFF == ord('q'):

            data={0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
            print('data',data) 
            msg = pickle.dumps(data)
            print('msg',msg)
            s.send(msg)
            time.sleep(20) """
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                    msg = pickle.dumps(self.axis_data)
                    #print('type:')
                    #print(self.axis_data)
                    print('len',len(msg))
                    time.sleep(0.001)   #安定させるため
                    #print(msg)
                    s.send(msg)
                if event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = 1
                    print (str(event.button)+'番目のボタンが押された')
                    msg = pickle.dumps(self.button_data)
                    #print('type:')
                    #print(type(self.button_data))
                    #print(msg)
                    s.send(msg)
                    if event.button==4: auto=not auto
                    if event.button==1: autopower+=1
                    if event.button==2: autopower-=1
                    if event.button==3: frontcam=not frontcam
                if event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = 0
                    print (str(event.button)+'番目のボタンが押された')
                    msg = pickle.dumps(self.button_data)
                    #print('type:')
                    #print(type(self.button_data))
                    #print(msg)
                    s.send(msg)
                msg2 = s.recv(1)
                print(msg2.decode("utf-8"))
                 
            #pprint.pprint(self.axis_data)
            #s.send(msg)
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.connect(('172.21.25.200',10000))
            #time.sleep()
            #opencv/
            frame[:] = (49, 52, 49)
            cvui.rect(frame, 700, 800, 140, 140, 0x000000)
            cvui.rect(frame,1100, 800, 140, 140, 0x000000)

            #cvui.rect(frame, 770-5+65, 870-5+65, 10, 10,0xffff00,0xffff00) #65
            #cvui.rect(frame,1170-5, 870-5, 10, 10, 0xffff00,0xffff00)
            #0:lx 1:-ly 2:rx 3:-ry
            
            lstop=False
            rstop=False
           
            if self.axis_data[2] >= p_threshold and self.axis_data[2] >= m_threshold and self.axis_data[3] <= p_threshold:
                cvui.rect(frame, 1170-5+(65*self.axis_data[2]), 870-5+(65*0), 10, 10,0xffff00,0xffff00)
                mode="turnR"
                cvui.printf(frame, 770, 150, 1.8, 0xffff00, "%.2f ",self.axis_data[2])
            elif self.axis_data[2] <= m_threshold and self.axis_data[3] >= m_threshold and self.axis_data[3] <= p_threshold:
                cvui.rect(frame, 1170-5+(65*self.axis_data[2]), 870-5+(65*0), 10, 10,0xffff00,0xffff00)
                mode="turnL"
                cvui.printf(frame, 770, 150, 1.8, 0xffff00, "%.2f ",self.axis_data[2])
            elif mode2=="stop":
                cvui.rect(frame, 1170-5+(65*self.axis_data[2]), 870-5, 10, 10,0x00ffff,0x00ffff)
                rstop=True

            if self.axis_data[0] >= m_threshold and self.axis_data[0]  <= p_threshold and self.axis_data[1] <= m_threshold:
                cvui.rect(frame, 770-5+(65*0), 870-5+(65*self.axis_data[1]), 10, 10,0xffff00,0xffff00)
                mode="forward"
                cvui.printf(frame, 770, 150, 1.8, 0xffff00, "%.2f ",self.axis_data[1])
            elif self.axis_data[0] >= m_threshold and self.axis_data[0] <= p_threshold and self.axis_data[1] >= p_threshold:
                cvui.rect(frame, 770-5+(65*0), 870-5+(65*self.axis_data[1]), 10, 10,0xffff00,0xffff00)
                mode="back"
                cvui.rect(frame, 720, 50, 10, 10,0xffff00,0xffff00)
                cvui.printf(frame, 770, 150, 1.8, 0xffff00, "%.2f ",self.axis_data[1])
            elif self.axis_data[0] >= p_threshold and self.axis_data[0] >= m_threshold and self.axis_data[1] <= p_threshold:
                cvui.rect(frame, 770-5+(65*self.axis_data[0]), 870-5+(65*0), 10, 10,0xffff00,0xffff00)
                mode="right"
                cvui.printf(frame, 770, 150, 1.8, 0xffff00, "%.2f ",self.axis_data[0])
            elif self.axis_data[0] <= m_threshold and self.axis_data[1] >= m_threshold and self.axis_data[1] <= p_threshold:
                cvui.rect(frame, 770-5+(65*self.axis_data[0]), 870-5+(65*0), 10, 10,0xffff00,0xffff00)
                mode="lef"
                cvui.printf(frame, 770, 150, 1.8, 0xffff00, "%.2f ",self.axis_data[0])
            else:
                cvui.rect(frame, 770-5+(65*self.axis_data[0]), 870-5, 10, 10,0x00ffff,0x00ffff)
                lstop=True

            if auto:
                cvui.printf(frame, 1020, 50, 1.8, 0xff0000, "%s ","auto")
                cvui.printf(frame, 1020+130, 50, 1.8, 0xff0000, "%d ",autopower)
            else :
                cvui.printf(frame, 1020, 50, 1.8, 0xffff00, "%s ",mode2)
                if self.axis_data[2] >= m_threshold and self.axis_data[2]  <= p_threshold and self.axis_data[3] <= m_threshold:
                    cvui.rect(frame, 1170-5+(65*0), 870-5+(65*self.axis_data[3]), 10, 10,0xffff00,0xffff00)
                    mode2="hujou"
                    cvui.printf(frame, 1020, 150, 1.8, 0xffff00, "%.2f ",self.axis_data[3])
                elif self.axis_data[2] >= m_threshold and self.axis_data[2] <= p_threshold and self.axis_data[3] >= p_threshold:
                    cvui.rect(frame, 1170-5+(65*0), 870-5+(65*self.axis_data[3]), 10, 10,0xffff00,0xffff00)
                    mode2="sensui"
                    cvui.printf(frame, 1020, 150, 1.8, 0xffff00, "%.2f ",self.axis_data[3])
                else:
                    #cvui.rect(frame, 1170-5+(65*0), 870-5+(65*self.axis_data[3]), 10, 10,0xffff00,0xffff00)
                    mode2="stop"

            if lstop and rstop:
                mode="stop"
                
            #cvui.rect(frame, 770-5+(65*self.axis_data[0]), 870-5+(65*self.axis_data[1]), 10, 10,0xffff00,0xffff00) #left
            #cvui.rect(frame, 1170-5+(65*self.axis_data[2]), 870-5+(65*self.axis_data[3]), 10, 10,0xffff00,0xffff00) #right
            #cvui.rect(frame,1170-5, 870-5, 10, 10, 0xffff00,0xffff00)
            
            cvui.image(frame,200,200,img)
            cvui.image(frame,1000,200,img2)
            """ cvui.image(frame,400,100,img)
            cvui.image(frame,800,100,img2) """

            cvui.printf(frame, 720, 50, 1.8, 0xffff00, "%s ",mode)
            #msg2 = s.recv(1024)
            #print(msg2.decode("utf-8"))
            #td = pickle.loads(msg2)

            """ cvui.printf(frame, 900, 600, 2.0, 0x0000ff, "%s",td['move']) 
            if td['mode']=='auto':
                cvui.printf(frame, 420, 50, 1.8, 0xff0000, "%s ",td['mode'])
            else:
                cvui.printf(frame, 420, 50, 1.8, 0x000000, "%s",td['mode'])
            cvui.printf(frame, 420, 50, 1.8, 0xff0000, "%s ",td['mode']) """


            """ if not auto:
                cvui.printf(frame, 420, 50, 1.8, 0xff0000, "%s ","auto")
                cvui.printf(frame, 420+70, 50, 1.8, 0xff0000, "%d ",autopower)
            else:
                cvui.printf(frame, 420, 50, 1.8, 0xff0000, "%s ","remote") """
            
            
            #msg = pickle.dumps(self.button_data)#error kaihi
            #s.send(msg)#error kaihi
            cvui.update()
            cv2.imshow(WINDOW_NAME,frame)
            if cv2.waitKey(20) == 27:
                break;
            #opencv/
       #except:
            #print('error')

    def send(data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('172.21.25.200',10000))
        #data = {1: "Apple", 2: "Orange"}
        msg = pickle.dumps(data)
        print(msg)
        s.send(msg)
        time.sleep(1)


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
    #getimage()
    #getiamge2()