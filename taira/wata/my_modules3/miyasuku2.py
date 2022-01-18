import socket
import pickle
from ROV_Motor4 import ROV_motor
import move_robot
import Adafruit_PCA9685

p_threshold = 0.4
m_threshold = -0.4

def start():
    motor = ROV_motor()
    motor.stop()
    data = {'joy_lx':0.0,'joy_ly' :0.0 ,'joy_rx' :0.0, 'joy_ry' :0.0}
    print('a')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('0.0.0.0', 10020))#IPとポート番号を指定します
    offs =40
    offs2=10  
    s.listen(1)
    
    sensui_autofg=False
    low_power_fg=False

    auto_value=0
    d={0: 0.0, 1: -0.01, 2: 0.0, 3: 0.0}
    c={0: 0, 1: 0, 2: 0, 3: 0,4: 0, 5: 0, 6: 0, 7: 0 ,8: 0, 9: 0, 10: 0,11: 0,12: 0}
    b={1:0,2: 0, 3: 0,4: 0, 5: 0, 6: 0, 7: 0 ,8: 0, 9: 0, 10: 0, 11: 0,12: 0,13:0}
    old_b={1:0,2: 0, 3: 0,4: 0, 5: 0, 6: 0, 7: 0 ,8: 0, 9: 0, 10: 0, 11: 0,12: 0,13:0}
    
    try:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")
        while True:
            msg = clientsocket.recv(1024)
            lenm=len(msg)
            if lenm==60:
                d = pickle.loads(msg)
                
                data['joy_lx']=d[0]
                data['joy_ly']=d[1]
                data['joy_rx']=d[2]
                data['joy_ry']=d[3]
                print('stick',d,'       len:',lenm)
            elif lenm != 60 and 100 > lenm and lenm!=0:
                c = pickle.loads(msg)
                b[1],b[2],b[3],b[4],b[5],b[7],b[8],b[12]=c[0],c[1],c[2],c[3],c[4],c[6],c[7],c[11] #bのkeyと実際のコントローラに書かれているボタンnum一致化
                if b[2] ==1 and old_b[2]==0:
                    auto_value+=1
                    print('b2 re',auto_value)
                if b[3] ==1 and old_b[3]==0:
                    auto_value-=1
                    print('b3 re',auto_value)
                if b[5] ==1 and old_b[5]==0:
                    sensui_autofg=not sensui_autofg
                    print('auto',sensui_autofg)
                    print('auto power',auto_value)
                if b[1] ==1 and old_b[1]==0:
                    motor.stopL()
                    motor.stopR()
                    print('kinkyu sutop')              

                old_b[1],old_b[2],old_b[3],old_b[4],old_b[5],old_b[7],old_b[8],old_b[12]=b[1],b[2],b[3],b[4],b[5],b[7],b[8],b[12]
            
            if d[0] >= m_threshold and d[0]  <= p_threshold and d[1] <= m_threshold:
                
                motor.forward(data)
                print('forward     :')
                #print(d[1])
            elif d[0] >= m_threshold and d[0] <= p_threshold and d[1] >= p_threshold:
                motor.reverse(data)
                print('reverse     :')
            elif d[0] >= p_threshold and d[0] >= m_threshold and d[1] <= p_threshold:
                motor.right_mov(data)
                print('right_mov   :')
            elif d[0] <= m_threshold and d[1] >= m_threshold and d[1] <= p_threshold:
                motor.left_mov(data)
                print('left_mov    :')
            elif d[2]>= p_threshold and d[3] >= m_threshold and d[3] <= p_threshold:
                motor.turn_right(data)

                print('turn_right  ')
            elif d[2] <= m_threshold and d[3] >= m_threshold and d[3] <= p_threshold:
                motor.turn_left(data)
                print('turn_left   ',d[2])
            else:
                motor.stopL()
                print('idoustop')
                
            if sensui_autofg==True:
                print('auto',auto_value)
                if auto_value>=0:
                    motor.forward_rotation(13, 0, 12+auto_value)       #上左
                    motor.forward_rotation(12, 0, 6+auto_value)        #上右
                else:
                    motor.forward_rotation(13, 0, 12+auto_value)       #上左
                    motor.forward_rotation(12, 0, 6+auto_value)        #上右
            else:
                if d[2]>= m_threshold and d[2] <= p_threshold and d[3]  <= m_threshold:
                    motor.rise(data)
                    print('Hujyou ' )
                elif d[2] >= m_threshold and d[2] <= p_threshold and d[3] >= p_threshold:
                    motor.descend(data)
                    print('sensui   ')
                else :
                    motor.stopR()
                    print('sensui stop')
            
            #clientsocket.send(bytes("i", 'utf-8'))
    except KeyboardInterrupt:
        #motor.all_duty0()
        #motor.stop()
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