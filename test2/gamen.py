import cv2
import matplotlib . pyplot as plt
import numpy as np

#画像の読み込み
img = cv2.imread ( 'ファイル名 . jpg' , 1 )
cv2.imshow ( 'ウィンドウ名',img )
cv2.waitKey ( 1 )
cv2.destroyAllwindows( )
#　第1引数は画像のファイル名、第2引数は保存したい画像
cv2.imwrite ( 'ファイル名' , img )

#%matplotlib inline
img = cv2 . imread ( 'ファイル名.jpg',img)
#　高さ
height = img . shape [ 0 ]
#　幅
width = img . shape [ 1 ]
#　高さ・幅を150pixelずつ取り除く
trim_img = img [ 150 : height , 150 : width ]
#　matplotlibで表示する場合はRGBからBGRに変換
trim_img = cv2 . cvtColor ( trim_img , cv2 . COLOR_RGB2BGR )
#　Haar ? like特微分類器の読み込み
face_cascade = cv2 . CascadeClassifier ( 'XMLファイル名' )
eye_cascade = cv2 . CascadeClassifier ( 'XMLファイル名' )
#　イメージファイルの読み込み
img = cv2 . imread ( '画像ファイル' )
#　グレースケール変換
gray = cv2 . cvtColor ( img , cv2 . COLOR_BGR2GRAY )
faces = face_cascade . detectMultiScale (gray , 1.3 , 5 )
for ( x , y , w , h ) in faces :
    img = cv2 . rectangle ( img , ( x , y ) , ( x + w , y + h ) , ( 255 , 0 , 0 ),2)
    roi_gray = gray [ y : y + h , x : x + w ]#顔画像/グレースケール
    roi_color = img [ y : y + h , x : x + w ]#顔画像/カラースケール

eyes = eye_cascade . detectMultiScale ( roi_gray )   #顔の中からfor ( ex , ey , ew , eh ) in eyes :
cv2 . rectangle (roi_color , ( ex , ey ) , ( ex + ew , ey + eh ) , ( 0 , 255 , 0 ) , 2 )  #検知した目を囲む
 #　画像を表示
cv2 . imshow ( 'img' , img )
#　キーを押したら終了
cv2 . waitKey ( 0 )
cv2 . destroyAllWindows ( ) 
plt.imshow ( trim_img )