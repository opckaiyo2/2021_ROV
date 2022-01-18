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
    offs =0
    duty = 0
    s.listen(1)

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
                d = pickle.loads(full_msg)
                
                if d[0] >= m_threshold and d[0] <= p_threshold and d[1] >= p_threshold:
                    duty=d[1]
                    motor.forward_rotation(15, 0, -1*offs*duty-5) #-7 reverse
                    motor.forward_rotation(14, 0, -1*offs*duty-6)
                    motor.forward_rotation(11, 0, offs*duty+10)
                    motor.forward_rotation(10, 0, offs*duty+10)
                    
                    print('power0',11+offs*duty)
                    print('motor.reverse')
                    print(d[1])
                elif d[0] >= m_threshold and d[0] <= p_threshold and d[1] <= m_threshold:
                    #duty=-1*d[0]
                    motor.forward_rotation(15, 0, -1*offs*duty-5) #-7 reverse
                    motor.forward_rotation(14, 0, -1*offs*duty-6)
                    motor.forward_rotation(11, 0, offs*duty+10)
                    motor.forward_rotation(10, 0, offs*duty+10)
                    print('motor.forwad')
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

                if d[2]>= m_threshold and d[2] <= p_threshold and d[3]  <= m_threshold:
                    duty=-1*d[3]
                    #print('duty:',duty)
                    motor.forward_rotation(13, 0, -1*offs*duty-7-3) #motor
                    motor.forward_rotation(12, 0, -1*offs*duty-7-3)
                    print('motor.Hujyou')
                    print(d[3])

                elif d[2] >= m_threshold and d[2] <= p_threshold and d[3] >= p_threshold:
                    duty=d[3]
                    #print('duty:',duty)                    
                    motor.forward_rotation(13, 0, 3+15+offs*duty)#motor 2
                    motor.forward_rotation(12, 0, 3+10+offs*duty)
                    print('motor.Sensui')
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