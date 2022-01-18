import subprocess

command = ["python3",'/home/pi/2021/taira/wata/my_modules3/miyasuku.py']

proc = subprocess.Popen(command)

command = ["python3",'/home/pi/2021/taira/wata/my_modules3/picture2.py']
proc2 = subprocess.Popen(command)


command = ["python3",'/home/pi/2021/taira/wata/my_modules3/picture.py']
proc3 = subprocess.Popen(command)


print("呼び出し中")

proc.communicate()
proc2.communicate()
proc3.communicate()

