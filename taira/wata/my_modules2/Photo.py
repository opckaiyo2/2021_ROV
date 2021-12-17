import cv2

class Photo:
	#コンストラクタ
	def __init__(self, cameraID = 0):
		#print('処理1')
		self.cameraID = cameraID
		
	#with構文の最初で実行される
	def __enter__(self):
		#print('処理2')
		self.cap = cv2.VideoCapture(self.cameraID)
		#self.cap.set(cv2.CAP_PROP_FPS, 60)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		return self
	
	#with構文の最後で実行される
	def __exit__(self, exc_type, exc_value, traceback):
		#print('処理3')
		self.cap.release()
	
	#カメラから画像を取得しjpeg変換を行う
	def jpg_photo(self, jpg_quality):
		status, frame = self.cap.read()
		
		if not status:
			return -1
		
		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality]
		result, encimg = cv2.imencode('.jpg', frame, encode_param)
		
		if result == False:
			return -2
		
		return encimg
	
	#jpeg画像をデコードする
	def img_decode(*img):
		#print(img[1])
		decimg = cv2.imdecode(img[1], cv2.IMREAD_COLOR)
		return decimg


if __name__ == '__main__':
	photo = Photo(0)
	
	with photo:
		img = photo.jpg_photo(50)
		img = photo.img_decode(img)
	
		cv2.imshow("Photo", img)
		cv2.waitKey(0)
	
