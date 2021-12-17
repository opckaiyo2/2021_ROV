import socket
import pickle
#from ROV_Mpuru6 import ROV_#motor
#import move_robot
#import Adafruit_PCA9685

p_threshold = 0.2
m_threshold = -0.2


def start():
    #motor = ROV_#motor()
    #motor.stop()
    data = {1: "Apple", 2: "Orange"}
    print('a')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 10008))#IPとポート番号を指定します
    offs =40
    offs2=10  #sensui
    duty = 0
    s.listen(1)
    
    autoduty=2
    sensui_autofg=False
    low_power_fg=False
    auto_value=0
    d={0: 0.0, 1: -0.01, 2: 0.0, 3: 0.0}
    c={0: 0, 1: 0, 2: 0, 3: 0,4: 0, 5: 0, 6: 0, 7: 0 ,8: 0, 9: 0, 10: 0,11: 0,12: 0}
    b={1:0,2: 0, 3: 0,4: 0, 5: 0, 6: 0, 7: 0 ,8: 0, 9: 0, 10: 0, 11: 0,12: 0,13:0}
    old_b={1:0,2: 0, 3: 0,4: 0, 5: 0, 6: 0, 7: 0 ,8: 0, 9: 0, 10: 0, 11: 0,12: 0,13:0}

    text_data={0:'aiueo'}

    #text_socket program 以下\
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind(('0.0.0.0', 1235))  # IPとポート番号を指定します
    s2.listen(1)
    #text_socket program 以上/

    
    try:
        clientsocket, address = s.accept()
        clientsocket2, address2 = s2.accept() 
        print(f"Connection from {address} has been established!")
        print(f"Connection text socket from {address2}has been established!")
        while True:
            msg = clientsocket.recv(1024)
            full_msg=msg
            time.sleep(0.001)
            if (lenm==60):#モータデータは60固定
                d = pickle.loads(full_msg)
                #print('stick',d,'       len:',lenm)
            elif lenm != 60 and 100 > lenm :
                c = pickle.loads(full_msg)
                #print('button',c,'       len:',lenm)
                b[1],b[2],b[3],b[4],b[5],b[7],b[8],b[12]=c[0],c[1],c[2],c[3],c[4],c[6],c[7],c[11]
                if b[2] ==1 and old_b[2]==0:
                    auto_value+=1
                    print('b2 re',auto_value)
                if b[3] ==1 and old_b[3]==0:
                    auto_value-=1
                    print('b3 re',auto_value)
                if b[5] ==1 and old_b[5]==0:
                    sensui_autofg=not sensui_autofg
                    if sensui_autofg ==True:
                        #auto_value=offs2*d[3] 
                        print('true')  
                    print('auto',sensui_autofg)
                    print('auto power',auto_value)
                if b[1] ==1 and old_b[1]==0:
                    #motor.forward_rotation(15, 0, 0) ##motor 0 
                    #motor.forward_rotation(14, 0, 0) ##motor 1
                    #motor.forward_rotation(13, 0, 0) ##motor 2
                    #motor.forward_rotation(12, 0, 0)
                    #motor.forward_rotation(11, 0, 0)
                    #motor.forward_rotation(10, 0, 0)
                    print('kinkyu sutop')
                #if b[8] ==1 and old_b[8]==0:    #R2で出力切り替え
                #    low_power_fg=not low_power_fg
                #    if low_power_fg==True:
                #        offs=offs-80
                #    else:
                #        offs=offs+80   
                    print('power',offs)                   

                old_b[1],old_b[2],old_b[3],old_b[4],old_b[5],old_b[7],old_b[8],old_b[12]=b[1],b[2],b[3],b[4],b[5],b[7],b[8],b[12]
            
            if d[0] >= m_threshold and d[0]  <= p_threshold and d[1] <= m_threshold:
                duty=-1*d[1]
                
                #motor.forward_rotation(15, 0, 7+(offs-18+10)*duty)#0 右前
                #motor.forward_rotation(14, 0, 7+(offs-20+10)*duty)  #1 右後
                #motor.forward_rotation(11, 0, -1*(offs+30+30-5)*duty-7)      #4 左前
                #motor.forward_rotation(10, 0, -1*(offs+28+30)*duty-7)      #5 左後
                
                #print('power0',11+offs*duty)
                print('forward     :',duty)
                #print(d[1])
            elif d[0] >= m_threshold and d[0] <= p_threshold and d[1] >= p_threshold:
                duty=d[1]
                #print('duty:',duty)
                #print('test',10 + offs*duty)
                #motor.forward_rotation(15, 0, -1*(offs)*duty-5) #0 右前　
                #motor.forward_rotation(14, 0, -1*(offs)*duty-6) #1 右後
                #motor.forward_rotation(11, 0, (offs+20)*duty+10)   #4 左前
                #motor.forward_rotation(10, 0, (offs+20)*duty+10)   #5 左後

                print('reverse     :',duty)
                #print(d[1])
            elif d[0] >= p_threshold and d[0] >= m_threshold and d[1] <= p_threshold:
                duty=d[0]
                #print('duty:',duty)
                #print(10 + offs*duty)
                #motor.forward_rotation(15, 0, -1*offs*duty-5)      #0 右前
                #motor.forward_rotation(14, 0, 10 + offs*duty)      #1 右後
                #motor.forward_rotation(11, 0, -1*offs*duty-7)      #4 左前
                #motor.forward_rotation(10, 0, 10+offs*duty)        #5 左後

                print('right_mov   :',duty)
                #print(d[0])
            elif d[0] <= m_threshold and d[1] >= m_threshold and d[1] <= p_threshold:
                duty=-1*d[0]
                #print('duty:',duty)
                #print(10 + offs*duty)

                #motor.forward_rotation(15, 0, 11 + offs*duty)      #0 右前
                #motor.forward_rotation(14, 0, -1*offs*duty-6)      #1 右後
                #motor.forward_rotation(11, 0, 10+offs*duty)        #4 左前   
                #motor.forward_rotation(10, 0, -1*offs*duty-7)      #5 左後

                print('left_mov    :',duty)
                #print(d[0])
            elif d[2]>= p_threshold and d[3] >= m_threshold and d[3] <= p_threshold:
                duty=d[2]
                #print('duty:',duty)
                #print(10 + offs*duty)

                #motor.forward_rotation(15, 0, -1*(offs-18)*duty-5)      #0 右前
                #motor.forward_rotation(14, 0, -1*(offs-18)*duty-6)      #1 右後
                #motor.forward_rotation(11, 0, -1*(offs-18)*duty-7)      #4 左前
                #motor.forward_rotation(10, 0, -1*(offs-18)*duty-7)      #5 左後

                print('turn_right  :',duty)
                print(d[2])
            elif d[2] <= m_threshold and d[3] >= m_threshold and d[3] <= p_threshold:
                duty=-1*d[2]
                #print('duty:',duty)
                #print('test',10 + offs*duty)

                #motor.forward_rotation(15, 0, 11+(offs-18)*duty)        #0 右前
                #motor.forward_rotation(14, 0, 10+(offs-18)*duty)        #1 右後
                #motor.forward_rotation(11, 0, 10+(offs-18)*duty)        #4 左前
                #motor.forward_rotation(10, 0, 10+(offs-18)*duty)        #5 左後
                print('turn_left   :',duty)
                #print(d[2])
            else:
                duty=0
                #print('duty:',duty)
                #motor.forward_rotation(15, 0, 0) ##motor 0
                #motor.forward_rotation(14, 0, 0) ##motor 1
                #motor.forward_rotation(11, 0, 0)
                #motor.forward_rotation(10, 0, 0)
                print('stop')
                
            if sensui_autofg==True:
                print('auto',auto_value)
                #motor.forward_rotation(13, 0, 12+auto_value)       #上左
                #motor.forward_rotation(12, 0, 6+auto_value)        #上右
            else:
                if d[2]>= m_threshold and d[2] <= p_threshold and d[3]  <= m_threshold:
                    duty=-1*d[3]
                    #print('duty:',duty)
                    #motor.forward_rotation(13, 0, -1*offs2*duty-9) #上左  #-9
                    #motor.forward_rotation(12, 0, -1*offs2*duty-8) #上右  #-8
                    print('Hujyou      :',duty)
                    #print(d[3])

                elif d[2] >= m_threshold and d[2] <= p_threshold and d[3] >= p_threshold:
                    duty=d[3]
                    #print('duty:',duty)
                    #motor.forward_rotation(13, 0, 12+offs2*duty)   #上左 #12
                    #motor.forward_rotation(12, 0, 6+offs2*duty)   #上右  #6 
                    print('sensui      :',offs2*duty)
                    #print(d[3])
                else :
                    duty=0
                    #motor.forward_rotation(13, 0, 0)##motor 2
                    #motor.forward_rotation(12, 0, 0)
                    #print('sensui stop')
            
                #print('stick',d,'       len:',lenm)
            
            print(f"Connection from {address2} has been established!")
            clientsocket2.send(bytes("Welcome to the server!", 'utf-8'))
    except KeyboardInterrupt:
        ##motor.all_duty0()
        #motor.forward_rotation(15, 0, 0) ##motor 0 
        #motor.forward_rotation(14, 0, 0) ##motor 1
        #motor.forward_rotation(13, 0, 0) ##motor 2
        #motor.forward_rotation(12, 0, 0)
        #motor.forward_rotation(11, 0, 0)
        #motor.forward_rotation(10, 0, 0)
        clientsocket.close()
        print('endprocess')

if __name__ == "__main__":
    start()