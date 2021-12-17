from multiprocessing import Value, Lock
import board
import busio
import time

import ms5837_python.ms5837 as ms5837
import Adafruit_CircuitPython_BNO055.adafruit_bno055 as adafruit_bno055
import sencer_Calculation

def sencer_process(
		sencer_lock,
		sencer_data,
	):
	#Value Memory
	pressure       = None
	acceleration_x = None
	acceleration_y = None
	acceleration_z = None
	deg_accel_z    = None
	Xx             = None
	Xy             = None
	Xz             = None
	Xd             = None
	#around time
	t       = 0.1
	real_time = None
	#create calculation Object!
	calc    = sencer_Calculation.Calculation()
	#create sencer Object!
	MS5837  = ms5837.MS5837_30BA()
	i2c     = busio.I2C(board.SCL, board.SDA)
	BNO055  = adafruit_bno055.BNO055_I2C(i2c)
	#initialize
	if not MS5837.init():
		print('MS5837 could not be initialized!')
		exit(-1)

	while True:
		real_time = time.time()
		if not MS5837.read():
			print("MS5837 Sencer read failed!")

		#acceleration
		result         = BNO055.acceleration
		acceleration_x = result[0]
		acceleration_y = result[1]
		acceleration_z = result[2]
		#deg_acceleration
		result         = BNO055.gyro
		deg_accel_z    = result[2]
		#pressure
		pressure       = MS5837.pressure(ms5837.UNITS_hPa)

		#check
		#print("acceleration_x : ", acceleration_x)
		#print("acceleration_y : ", acceleration_y)
		#print("acceleration_z : ", acceleration_z)
		#print("deg_accel_z    : ", deg_accel_z)
		#print("pressure       : ", pressure)
		#print("")


		Xx, Xy, Xz, Xd = calc.calc_value(
					acceleration_x,
					acceleration_y,
					acceleration_z,
					deg_accel_z,
					t
				)

		#print('Xx:{0}, Xy:{1}, Xz:{2}, Xd:{3}'.format(Xx, Xy, Xz, Xd))

		#exclusion control
		if sencer_lock.acquire(True):
			sencer_data["distance_x"] = Xx
			sencer_data["distance_y"] = Xy
			sencer_data["degree_z"]   = Xd
			sencer_data["pressure"]   = pressure
			sencer_lock.release()

		#fixed cycle
		real_time = time.time() - real_time
		if real_time < t:
			time.sleep(t - real_time)





if __name__ == '__main__':
	try:
		lock = Lock()
		d    = dict()
		sencer_process(*(lock, d, ))
	except KeyboardInterrupt:
		print("end process!")
		exit(1)
	
