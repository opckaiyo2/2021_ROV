import socket
import pickle
from ROV_Mpuru5 import ROV_Motor
import move_robot
import Adafruit_PCA9685

p_threshold = 0.4
m_threshold = -0.4


def start():
    motor = ROV_Motor()
    motor.stop()
    data = {1: "Apple", 2: "Orange"}
    print('a')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 10000))  # IPとポート番号を指定します
    offs =25
    offs2=1  #sensui
    duty = 0
    s.listen(1)
    autoduty=0
    sensui_autofg=False
    auto_value=0
    d={0: 0.0, 1: -0.01, 2: 0.0, 3: 0.0}
    c={0: 0.0, 1: 0.0, 2: 0, 3: 0.0,4: 0.0, 5: 0.0, 6: 0, 7: 0.0 ,8: 0.0, 9: 0.0, 10: 0, 10: 0.0}
    b={2: 0.0, 3: 0.0, 4: 0.0}
    old_b={2: 0.0, 3: 0.0, 4: 0.0}
    try:
        while True:
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established!")

            while True:
                full_msg = b''
                while True:
                    msg = clientsocket.recv(1024)
                    full_msg += msg
                    if len(msg) > 0:
                        break
                if (len(full_msg)>=60): #データの大きさでボタンなのかスティックなのか判断 button3つ同時押しできない60こえる
                    d = pickle.loads(full_msg)
                    print('stick',d,'       len:',len(full_msg))
                else:
                    c = pickle.loads(full_msg)
                    print('button',c,'       len:',len(full_msg))
                    b[2],b[3],b[4]=c[1],c[2],c[3]
                    if b[2] ==1 and old_b[2]==0:
                        auto_value+=1
                        print('b2 re',auto_value)
                    if b[3] ==1 and old_b[3]==0:
                        auto_value-=1
                        print('b4 re',auto_value)
                    if b[4] ==1 and old_b[4]==0:
                        sensui_autofg=not sensui_autofg
                        print('auto',sensui_autofg)

                    old_b[2],old_b[3],old_b[4]=c[1],c[2],c[3]
                
                if d[0] >= m_threshold and d[0]  <= p_threshold and d[1] <= m_threshold:
                    duty=-1*d[1]
                    motor.forward_rotation(15, 0, 11+offs*duty)
                    motor.forward_rotation(14, 0, 10+offs*duty)
                    motor.forward_rotation(11, 0, -1*offs*duty-7)
                    motor.forward_rotation(10, 0, -1*offs*duty-7)
                    
                    print('power0',11+offs*duty)
                    print('motor.forward')
                    print(d[1])
                elif d[0] >= m_threshold and d[0] <= p_threshold and d[1] >= p_threshold:
                    duty=d[1]
                    #print('duty:',duty)
                    #print('test',10 + offs*duty)
                    motor.forward_rotation(15, 0, -1*offs*duty-5) #-7 reverse
                    motor.forward_rotation(14, 0, -1*offs*duty-6)
                    motor.forward_rotation(11, 0, offs*duty+10)
                    motor.forward_rotation(10, 0, offs*duty+10)

                    print('motor.reverse')
                    print('power',-1*offs*duty-5)
                    print('power 4',(offs-4)*duty+10)
                    print(d[1])
                elif d[0] >= p_threshold and d[0] >= m_threshold and d[1] <= p_threshold:
                    duty=d[0]
                    #print('duty:',duty)
                    #print(10 + offs*duty)
                    motor.forward_rotation(15, 0, -1*offs*duty-5) #-7 reverse
                    motor.forward_rotation(14, 0, 10 + offs*duty)
                    motor.forward_rotation(11, 0, -1*offs*duty-7)
                    motor.forward_rotation(10, 0, 10+offs*duty)

                    print('motor.right_mov')
                    print(d[0])
                elif d[0] <= m_threshold and d[1] >= m_threshold and d[1] <= p_threshold:
                    duty=-1*d[0]
                    #print('duty:',duty)
                    #print(10 + offs*duty)
                    motor.forward_rotation(11, 0, 10+offs*duty)
                    motor.forward_rotation(10, 0, -1*offs*duty-7)
                    motor.forward_rotation(15, 0, 11 + offs*duty)
                    motor.forward_rotation(14, 0, -1*offs*duty-6)

                    print('motor.left_mov')
                    print(d[0])
                elif d[2]>= p_threshold and d[3] >= m_threshold and d[3] <= p_threshold:
                    duty=d[2]
                    #print('duty:',duty)
                    #print(10 + offs*duty)
                    motor.forward_rotation(11, 0, -1*offs*duty-7)
                    motor.forward_rotation(10, 0, -1*offs*duty-7)
                    motor.forward_rotation(15, 0, -1*offs*duty-5)
                    motor.forward_rotation(14, 0, -1*offs*duty-6)

                    print('motor.turn_right')
                    print(d[2])
                elif d[2] <= m_threshold and d[3] >= m_threshold and d[3] <= p_threshold:
                    duty=-1*d[2]
                    #print('duty:',duty)
                    #print('test',10 + offs*duty)
                    motor.forward_rotation(11, 0, 10+offs*duty)
                    motor.forward_rotation(10, 0, 10+offs*duty)
                    motor.forward_rotation(15, 0, 11+offs*duty)
                    motor.forward_rotation(14, 0, 10+offs*duty)
                    print('motor.turn_left')
                    print(d[2])

                else:
                    duty=0
                    #print('duty:',duty)
                    motor.forward_rotation(15, 0, 0) #motor 0
                    motor.forward_rotation(14, 0, 0) #motor 1
                    motor.forward_rotation(11, 0, 0)
                    motor.forward_rotation(10, 0, 0)
                    print('motor.stop')
                    
                if sensui_autofg==True:
                    print('automodooooo on!')
                    motor.forward_rotation(13, 0, 15+auto_value)#motor 2
                    motor.forward_rotation(12, 0, 9+auto_value)
                else:
                    if d[2]>= m_threshold and d[2] <= p_threshold and d[3]  <= m_threshold:
                        duty=-1*d[3]
                        #print('duty:',duty)
                        motor.forward_rotation(13, 0, -1*offs2*duty-7) #motor
                        motor.forward_rotation(12, 0, -1*offs2*duty-7)
                        print('motor.Hujyou')
                        print(d[3])

                    elif d[2] >= m_threshold and d[2] <= p_threshold and d[3] >= p_threshold:
                        duty=d[3]
                        #print('duty:',duty)                    
                        motor.forward_rotation(13, 0, 15+offs2*duty)#motor 2
                        motor.forward_rotation(12, 0, 10+offs2*duty)

                        print('powersensui',3+15+offs2*duty)
                        print(d[3])
                    else :
                        duty=0
                        motor.forward_rotation(13, 0, 0)#motor 2
                        motor.forward_rotation(12, 0, 0)
                        print('sensui stop')

    except KeyboardInterrupt:
        #motor.all_duty0()
        motor.forward_rotation(15, 0, 0) #motor 0 
        motor.forward_rotation(14, 0, 0) #motor 1
        motor.forward_rotation(13, 0, 0) #motor 2
        motor.forward_rotation(12, 0, 0)
        motor.forward_rotation(11, 0, 0)
        motor.forward_rotation(10, 0, 0)
        clientsocket.close()
        print('endprocess')

if __name__ == "__main__":
    start()