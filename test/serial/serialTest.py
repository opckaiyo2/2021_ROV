import serial
# シリアルポートへの接続
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
while 1:
    # シリアル通信で1行読み込む
    line = ser.readline()
    # 余分な空白や改行を除き、バイト列を文字列に変換する
    temp = line.strip().decode()
    print(f'温度: {temp}°C')
# シリアルポートを閉じる
ser.close()
