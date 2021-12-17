#This class can calculate the distance and angle

class Calculation:
	def __init__(self):
		#previous speed
		self.__Vox    = 0
		self.__Voy    = 0
		self.__Voz    = 0
		#current speed and degree
		self.__Vx     = 0
		self.__Vy     = 0
		self.__Vz     = 0
		self.__degree = 0
		#total distance and degree
		self.__Xx     = 0
		self.__Xy     = 0
		self.__Xz     = 0
		self.__Xd     = 0

	#calculation of speed
	def calc_speed(self, ax, ay, az, t):
		self.__Vx = ax * t + self.__Vox
		self.__Vy = ay * t + self.__Voy
		self.__Vz = az * t + self.__Voz

	#calculation of total distance
	def calc_distance(self, t):
		self.__Xx = (self.__Vox + self.__Vx) * t * 0.5 + self.__Xx
		self.__Xy = (self.__Voy + self.__Vy) * t * 0.5 + self.__Xy
		self.__Xz = (self.__Voz + self.__Vz) * t * 0.5 + self.__Xz

	#calculation of degree
	def calc_degree(self, angle_speed, t):
		self.__Xd = (angle_speed * t) * 180 / 3.14 + self.__Xd

	#previous speed do updating
	def update_old_speed(self):
		self.__Vox = self.__Vx
		self.__Voy = self.__Vy
		self.__Voz = self.__Vz

	#calculate all parameter and return the value
	def calc_value(self, ax, ay, az, angle_speed, t):
		self.update_old_speed()
		self.calc_speed(ax, ay, az, t)
		self.calc_distance(t)
		self.calc_degree(angle_speed, t)
		return (self.__Xx, self.__Xy, self.__Xz, self.__Xd)

	#get speed
	def get_speed(self):
		return (self.__Vx, self.__Vy, self.__Vz)

	#property clear
	def property_clear(self):
		#previous speed
		self.__Vox    = 0
		self.__Voy    = 0
		self.__Voz    = 0
		#current speed and degree
		self.__Vx     = 0
		self.__Vy     = 0
		self.__Vz     = 0
		self.__degree = 0
		#total distance and degree
		self.__Xx     = 0
		self.__Xy     = 0
		self.__Xz     = 0
		self.__Xd     = 0


if __name__ == '__main__':
	a   = [0.6, 0.73, 1.4]
	a_d = 0.2
	t   = 0.01

	calc = Calculation()

	for i in range(100):
		Xx, Xy, Xz, deg = calc.calc_value(a[0],a[1],a[2],a_d,t)
		aa, bb, cc      = calc.get_speed()
		print('ax:{0}, ay:{1}, az:{2}'.format(aa, bb, cc))
	calc.property_clear()

