import socket
import pickle
def start():
    #data = {1: "Apple", 2: "Orange"}

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind(('0.0.0.0', 49999))  # IPとポート番号を指定します
    s2.bind(('0.0.0.0', 50000))  # IPとポート番号を指定します
    s3.bind(('0.0.0.0', 50001))  # IPとポート番号を指定します
    s1.listen(1)
    s2.listen(1)
    s3.listen(1)

    try:
            clientsocket, address = s1.accept()
            clientsocket2, address = s2.accept()#もしかしたらClientsoket2にする
            clientsocket3, address = s3.accept()#もしかしたらClientsoket2にする
            while True:
                msg = clientsocket.recv(1024)
                #print(f"Connection from {address} has been established!")
                #d = pickle.loads(full_msg)
                d = pickle.loads(msg)

                int_d = int(d)

                if int_d == 0:
                    print('モーター')
                elif int_d == 1:
                    print('コントローラー')
                elif int_d == 2:
                    print('上カメラ') 
                elif int_d == 3:
                    print('下カメラ')
                else:
                    print('それ以外')

                #d = pickle.loads(msg)
                #msg = pickle.dumps(data)
                # Output: b'\x80\x04\x95\x1a\x00\x00\x00\x00\x00\x00\x00}\x94(K\x01\x8c\x05Apple\x94K\x02\x8c\x06Orange\x94u.'
                print(d)#こっちも変える

                #clientsocket.send(msg)
                #clientsocket.recv(msg)
                #clientsocket.close()
    except:
        s1.close()
        s2.close()
        s3.close()

if __name__ == "__main__":
    start()