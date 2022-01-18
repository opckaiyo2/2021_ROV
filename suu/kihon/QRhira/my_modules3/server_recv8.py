import socket
import pickle
from ROV_Mpuru4 import ROV_Motor
import move_robot
import Adafruit_PCA9685

p_threshold = 0.5
m_threshold = -0.5


def start():
    motor = ROV_Motor()
    motor.stop()
    data = {1: "Apple", 2: "Orange"}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 10000))  # IPとポート番号を指定します
    offs = 1
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
                if d[0] >= m_threshold and d[0]  <= p_threshold and d[1] <= m_threshold:
                    duty=-1*d[0]
                    #print('duty:',duty)
                    #print(10 + offs*duty)
                    motor.forward_rotation(15, 0, (offs*duty)+11) #-7 reverse
                    motor.forward_rotation(14, 0, (offs*duty)+10)
                    motor.forward_rotation(11, 0, (-1*offs*duty)-7)
                    motor.forward_rotation(10, 0, (-1*offs*duty)-7)

                    motor.forward_rotation(13, 0, 0) #motor 2
                    motor.forward_rotation(12, 0, 0)

                    print('motor.forward', d[1])
                elif d[0] >= m_threshold and d[0] <= p_threshold and d[1] >= p_threshold:
                    duty=d[1]
                    #print('duty:',duty)
                    #print('test',10 + offs*duty)
                    motor.forward_rotation(15, 0, (-1*offs*duty)-5) #-7 reverse
                    motor.forward_rotation(14, 0, (-1*offs*duty)-6)
                    motor.forward_rotation(11, 0, (offs*duty)+10)
                    motor.forward_rotation(10, 0, (offs*duty)+10)

                    motor.forward_rotation(13, 0, 0) #motor 2
                    motor.forward_rotation(12, 0, 0)
                    print('motor.reverse', d[1])
                elif d[0] >= p_threshold and d[0] >= m_threshold and d[1] <= p_threshold:
                    duty=d[0]
                    #print('duty:',duty)
                    #print(10 + offs*duty)
                    motor.forward_rotation(15, 0, -1*offs*duty-5) #-7 reverse
                    motor.forward_rotation(14, 0, 10 + offs*duty)
                    motor.forward_rotation(11, 0, -1*offs*duty-7)
                    motor.forward_rotation(10, 0, 10+offs*duty)

                    motor.forward_rotation(13, 0, 0) #motor 2
                    motor.forward_rotation(12, 0, 0)
                    print('motor.right_mov', d[0])
                elif d[0] <= m_threshold and d[1] >= m_threshold and d[1] <= p_threshold:
                    duty=-1*d[0]
                    #print('duty:',duty)
                    #print(10 + offs*duty)
                    motor.forward_rotation(11, 0, 10+offs*duty)
                    motor.forward_rotation(10, 0, -1*offs*duty-7)
                    motor.forward_rotation(15, 0, 11 + offs*duty)
                    motor.forward_rotation(14, 0, -1*offs*duty-6)
                    motor.forward_rotation(13, 0, 0) #motor 2
                    motor.forward_rotation(12, 0, 0)
                    print('motor.left_mov', d[0])
                elif d[2]>= p_threshold and d[3] >= m_threshold and d[3] <= p_threshold:
                    duty=d[2]
                    #print('duty:',duty)
                    #print(10 + offs*duty)
                    motor.forward_rotation(11, 0, -1*offs*duty-7)
                    motor.forward_rotation(10, 0, -1*offs*duty-7)
                    motor.forward_rotation(15, 0, -1*offs*duty-5)
                    motor.forward_rotation(14, 0, -1*offs*duty-6)

                    motor.forward_rotation(13, 0, 0) #motor 2
                    motor.forward_rotation(12, 0, 0)
                    print('motor.turn_right', d[2])
                elif d[2] <= m_threshold and d[3] >= m_threshold and d[3] <= p_threshold:
                    duty=-1*d[2]
                    #print('duty:',duty)
                    #print('test',10 + offs*duty)
                    motor.forward_rotation(11, 0, 10+offs*duty)
                    motor.forward_rotation(10, 0, 10+offs*duty)
                    motor.forward_rotation(15, 0, 11+offs*duty)
                    motor.forward_rotation(14, 0, 10+offs*duty)

                    motor.forward_rotation(13, 0, 0) #motor 2
                    motor.forward_rotation(12, 0, 0)
                    print('motor.turn_left', d[2])
                elif d[2]>= m_threshold and d[2] <= p_threshold and d[3]  <= m_threshold:
                    duty=-1*d[3]
                    #print('duty:',duty)                    
                    motor.forward_rotation(13, 0, -1*offs*duty-7) #motor 2
                    motor.forward_rotation(12, 0, -1*offs*duty-7)
                    motor.forward_rotation(15, 0, 0) #-7 reverse
                    motor.forward_rotation(14, 0, 0)
                    motor.forward_rotation(11, 0, 0)
                    motor.forward_rotation(10, 0, 0)
                    print('motor.Hujyou', d[3])

                elif d[2] >= m_threshold and d[2] <= p_threshold and d[3] >= p_threshold:
                    duty=d[3]
                    #print('duty:',duty)                    
                    motor.forward_rotation(13, 0, 15+offs*duty) #motor 2
                    motor.forward_rotation(12, 0, 10+offs*duty)

                    motor.forward_rotation(15, 0, 0) #-7 reverse
                    motor.forward_rotation(14, 0, 0)
                    motor.forward_rotation(11, 0, 0)
                    motor.forward_rotation(10, 0, 0)
                    print('motor.Sensui', d[3])

                else:
                    duty=0
                    #print('duty:',duty)
                    motor.forward_rotation(15, 0, 0) #motor 0
                    motor.forward_rotation(14, 0, 0) #motor 1
                    motor.forward_rotation(13, 0, 0) #motor 2
                    motor.forward_rotation(12, 0, 0)
                    motor.forward_rotation(11, 0, 0)
                    motor.forward_rotation(10, 0, 0)
                    print('motor.stop')
                    #motor.stop()
                    #else:
                    #print(d[0])#
                    #print(d)
                    #cnt+=1

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