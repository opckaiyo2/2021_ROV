import socket
import pickle
def start():
    data = {1: "Apple", 2: "Orange"}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 50000))  # IPとポート番号を指定します
    s.listen(1)

    try:
        while True:
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established!")
            msg = pickle.dumps(data)
            # Output: b'\x80\x04\x95\x1a\x00\x00\x00\x00\x00\x00\x00}\x94(K\x01\x8c\x05Apple\x94K\x02\x8c\x06Orange\x94u.'
            print(msg)

            clientsocket.send(msg)
            clientsocket.close()
    except:
        s.close()

if __name__ == "__main__":
    # test
    start()