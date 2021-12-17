import socket  
import numpy  
import cv2
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
from PIL import ImageFont, ImageDraw, Image

#cap = cv.VideoCapture(0)

def getimage():#ソケット通信
    HOST = '172.21.25.230'
    PORT = 50000
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
    sock.connect((HOST,PORT))   
    sock.send(('a').encode("utf-8"))  
    buf=b''
    recvlen=100  
    while recvlen>0:  
        receivedstr=sock.recv(1024)  
        recvlen=len(receivedstr)
        print(recvlen,'Byte')  
        buf +=receivedstr
    sock.close()  
    narray=numpy.fromstring(buf,dtype='uint8')   
    return cv2.imdecode(narray,1)  
while True:
    frame = getimage()
    #cv2.imshow('Capture',frame)
    #カメラから1コマのデータを取得する
    #ret,frame = cap.read()
    #バーコードからデータを読み取る
    for barcode in decode(frame):
        print(barcode.data)



        #QRコードデータはバイトオブジェクトなので、カメラ上に描くために、文字列に変換する
        myData = barcode.data.decode('utf-8')
        img_pil = Image.fromarray(frame) # 配列の各値を8bit(1byte)整数型(0～255)をPIL Imageに変換。
        draw = ImageDraw.Draw(img_pil) # drawインスタンスを生成
        position = (50, 100) # テキスト表示位置
        print('6')
        draw.text(position, input, font = font , fill = (b, g, r, a) ) # drawにテキストを記載 fill:色 BGRA (RGB)
        img = np.array(img_pil) # PIL を配列に変換
	    


        print(myData)
        #QRコードの周りに長方形を描画しデータを表示する
        pts =np.array([barcode.polygon],np.int32)
        #polylines()関数で複数の折れ線を描画
        cv.polylines(frame,[pts],True,(255,0,0),5)
        pts2 =barcode.rect


        #putText()関数で文字列を描画
        cv.putText(frame,myData,(pts2[0],pts2[1]),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)




        #imshow()関数で出力ウィンドウを表示
        cv.imshow('test',frame)
        cv2.imshow("res", img)  ####
        cv2.imwrite("res.png", img)




    #qキーが押されるまで待機
        #if cv.waitKey(1) & 0xFF == ord('q'):
        #cv2.imshow('test',frame)  
        #img = getimage()
        #img2 = getimage()
        #cv2.imshow('Capture',img)  
        #cv2.imshow('Capture2',img2)  
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

HOST = '172.21.25.230'
PORT = 50000
getimage