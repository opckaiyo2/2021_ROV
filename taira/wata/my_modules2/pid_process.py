from multiprocessing import Value, Lock
from sencer_process import sencer_process
import time

def pid_control_process(
 auto_flag,
 condition_param,
 condition_lock,
	sencer_data,
	sencer_lock,
	M_lock,
	operation_M,
	):

	#PID parameter
	###target
	goal = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0,
		"pressure"              : 0,
		}
	#----------------------------------------------------------------
	###Proportional gain
	Kp = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0.03,
		"pressure"              : 0.6,
		}

	###Integral gain
	Ki = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0.03,
		"pressure"              : 0.02, #0.05,
		}
	###Derivative gain
	Kd = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0.03,
		"pressure"              : 0.5, #0.06,
		}
	#------------------------------------------------------------------
	#Operation amount
	###this time
	M = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0,
		"pressure"              : 0,
		}
	###last time
	M1 = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0,
		"pressure"              : 0,
		}
	#deviation
	###this time
	e = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0,
		"pressure"              : 0,
		}
	###last time
	e1 = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0,
		"pressure"              : 0,
		}
	###two times before
	e2 = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0,
		"pressure"              : 0,
		}
	#time [sec]
	t = 0.02
	#sencer parameter
	S = {
		"a_distance_x"          : 0,
		"a_distance_y"          : 0,
		"degree_z"              : 0,
		"pressure"              : 0,
		}

	#pid main processing
	while True:
		if auto_flag.value == True:
			#reset operation_M
			if M_lock.acquire(True):
				operation_M['accel_x'] = 0
				operation_M['accel_y'] = 0
				operation_M['degree_z'] = 0
				operation_M['pressure'] = 0
				M_lock.release()
			#reset parameter
			for key, val in M.items():
				M[key]  = 0
				M1[key] = 0
				e[key]  = 0
				e1[key] = 0
				e2[key] = 0
				
			#set goal sencer data
			if sencer_lock.acquire(True):
				goal['a_distance_x'] = sencer_data['distance_x']
				goal['a_ditance_y']  = sencer_data['distance_y']
				goal['degree_z']     = sencer_data['degree_z']
				goal['pressure']     = sencer_data['pressure']
				sencer_lock.release()

			#pid processing
			while auto_flag.value == True:
				time.sleep(t)
				#get sencer data
				if sencer_lock.acquire(True):
					#print('pressure: {}'.format(sencer_pressure.value))
					S['a_distance_x'] = sencer_data["distance_x"]
					S['a_distance_y'] = sencer_data["distance_y"]
					S['degree_z']     = sencer_data["degree_z"]
					S['pressure']     = sencer_data["pressure"]
					sencer_lock.release()
				#update
				for key in M.keys():
					M1[key] = M[key]
					e2[key] = e1[key]
					e1[key] = e[key]


				for key in e.keys():
					e[key] = goal[key] - S[key]
					#print('{}:{}'.format(key,e[key]))
					P      = Kp[key] * (e[key] - e1[key])
					I      = Ki[key] * e[key]
					D      = Kd[key] * ((e[key] - e1[key]) - (e1[key] - e2[key]))
					M[key] = M1[key] + P + I + D

					#if key == 'pressure':
					#	print('e[key] : {}'.format(e[key]))
					#	print('P : {}'.format(P))
					#	print('I : {}'.format(I))
					#	print('D : {}'.format(D))

					#M[key] = abs( M[key] )
					if M[key] > 400:
						M[key] = 400
					elif M[key] < -400:
						M[key] = -400
					M[key] = round( M[key] )

					#if key == 'pressure':
					#	print('sub M:{}'.format(M[key]))
				#debug process
				
				#store operation amount
				if M_lock.acquire(True) is True:
					operation_M["accel_x"]              = M['a_distance_x']
					operation_M["accel_y"]              = M['a_distance_y']
					operation_M["degree_z"]             = M['degree_z']
					operation_M["pressure"]             = M['pressure']
					M_lock.release()

				if condition_lock.acquire(True):
					condition_param['com_pressure']    = e['pressure']
					condition_param['degree_z']        = e['degree_z']
					condition_lock.release()
	return


if __name__ == '__main__':
	from multiprocessing import Process
	import time
	#parameter
	camera_data       = dict()
	sencer_data       = dict()
	operation_M       = dict()
	condition_param   = dict()
	auto_flag         = Value('b', 0)
	condition_lock    = Lock()
	camera_lock       = Lock()
	sencer_lock       = Lock()
	M_lock            = Lock()
	

	p1_args = (
		auto_flag,
		condition_param,
		condition_lock,
		camera_data,
		camera_lock,
		sencer_data,
		sencer_lock,
		M_lock,
		operation_M,
		)

	p2_args = (
			sencer_lock,
			sencer_data,
			)
			

	p1 = Process(target=pid_control_process, args=p1_args, daemon=True)
	p2 = Process(target=sencer_process, args=p2_args, daemon=True)
	p2.start()
	time.sleep(1)
	p1.start()
	

	#sencer_lock.acquire(True)
	#sencer_pressure.value = 100
	#sencer_lock.release()

	#auto_flag.value = True
	try:
		while True:
			print('input command!')
			x = input()
			print('\n')

			if x == '1':
				auto_flag.value = True
			else:
				auto_flag.value = False
	except KeyboardInterrupt:
		p1.kill()
		print('end')

		
