#!/usr/bin/env python
from pvector import PVector
import numpy
import math
import temperature_function as temp
import plugin
import time
from random import randint	
def sub_all_x(close_drones, current):
	dx=0
	for other in close_drones:
		dx+=current.xyz[0]-other.xyz[0]
	dx=(-1)*dx
	return dx					
def sub_all_y(close_drones, current):
	dy=0
	for other in close_drones:
		dy+=current.xyz[1]-other.xyz[1]
	dy=(-1)*dy
	return dy
def sum_all_x(close_drones, current):
	dx=0
	for other in close_drones:
		dx+=other.xyz[0]
	return dx
						
def sum_all_y(close_drones, current):
	dy=0
	for other in close_drones:
		dy+=other.xyz[1]
	return dy
		
def sum_all_vel_x(close_drones, current):
	dx=0
	for other in close_drones:
		dx+=current.v_ned_d[0]-other.v_ned_d[0]
	return dx
						
def sum_all_vel_y(close_drones, current):
	dy=0
	for other in close_drones:
		dy+=current.v_ned_d[1]-other.v_ned_d[1]
	return dy
		
def find_neighbours_in_radius(current,radius):
	agents=current.group.all_drones
	neibourgh=[]
	for it in agents:
	    if it.tag!=current.tag:
		if euclidean_distance(it.xyz,current.xyz)<=radius: #and it.role==current.role:
			neibourgh.append(it)
	return neibourgh
		
def euclidean_distance(a,b):
	distance=math.sqrt(pow((a[0] - b[0]), 2) + pow((a[1] - b[1]), 2))
	return distance
def stay_in_border(position):
	v=PVector(0,0)
	Xmin=13
	Xmax=13
	Ymin=13
	Ymax=13
	constant=100
	if position.x <= Xmin:
		v.x = constant
	elif position.x >= Xmax:
		v.x = -constant
		
	if position.y <= Ymin :
		v.y = constant
	elif position.y >= Ymax :
		v.y = -constant
		
	return v.return_as_vector()
def get_coordinates(current):
	return current.xyz[0:1]
def normalize(vector):
	vector=PVector(vector[0],vector[1])
	vector.normalize()
	return vector.return_as_vector()
def temperature_sensor(current):
	fire_x=0.0
	fire_y=0.0
	value=[]
	a=10000
	b=6
	distance=math.sqrt(pow((current.xyz[0] - fire_x), 2) + pow((current.xyz[1] - fire_y), 2))
	temperature=a/(distance+b)
	value.append(temperature)
	return temperature

def get_position_by_radius(current):
	x=float("{0:.2f}".format(current.xyz[0]))	
	y=float("{0:.2f}".format(current.xyz[1]))
	position=numpy.array([x,y])
	for point in current.var:
		print "pointsssss",position,point
		if abs(point[0]-position[0])<=1 and abs(point[1]-position[1])<=1:
			return current.var       		
	current.var.append(position)
	return current.var
		
def separation (current):
	alt_d=8
	position=PVector(current.xyz[0],current.xyz[1])
	close_drones=find_neighbours_in_radius(current,1000)
	if len(close_drones)==0:
		empty=PVector(0,0)
		velocity=PVector(current.v_ned_d[0],current.v_ned_d[1])
		current.set_v_2D_alt_lya(velocity.return_as_vector(),-alt_d)
		return empty.return_as_vector()
	dx=sub_all_x(close_drones,current)
	dx=(dx/len(close_drones))
	dy=sub_all_y(close_drones,current)
	dy=(dy/len(close_drones))	
	sep_vector=numpy.array([dx,dy])
	sep_vector=normalize(sep_vector)
	return sep_vector

def cohesion (current):
	alt_d=8
	position=PVector(current.xyz[0],current.xyz[1])
	close_drones=find_neighbours_in_radius(current,1000)
	if len(close_drones)==0:
		empty=PVector(0,0)
		velocity=PVector(current.v_ned_d[0],current.v_ned_d[1])
		current.set_v_2D_alt_lya(velocity.return_as_vector(),-alt_d)
		return empty.return_as_vector()
	sx=sum_all_x(close_drones,current)
	sx=(sx/len(close_drones))
	sx=sx - current.xyz[0]
	sy=sum_all_y(close_drones,current)
	sy=(sy/len(close_drones))
	sy=sy - current.xyz[1]
	cohesion_vec=numpy.array([(sx-position.x),(sy-position.y)])
	cohesion_vec=normalize(cohesion_vec)
	return cohesion_vec

def velavg (current):
	alt_d=8
	position=PVector(current.xyz[0],current.xyz[1])
	close_drones=find_neighbours_in_radius(current,1000)
	if len(close_drones)==0:
		empty=PVector(0,0)
		velocity=PVector(current.v_ned_d[0],current.v_ned_d[1])
		current.set_v_2D_alt_lya(velocity.return_as_vector(),-alt_d)
		return empty.return_as_vector()
	velx=sum_all_vel_x(close_drones,current)
	velx=(velx/len(close_drones))
	vely=sum_all_vel_x(close_drones,current)
	vely=(vely/len(close_drones))
	vel_vector=numpy.array([velx,vely])
	vel_vector=normalize(vel_vector)
	return vel_vector

def flocking (current,per):
	#print "flocking" 
	flocking_vec=((separation(current)+cohesion(current))+velavg(current))
	if plugin.reset(per)==True:
		#current.set_v_2D_alt_lya(flocking_vec,-8)
		return flocking_vec
	else:
		#current.set_xyz_ned_lya(current.xyz)
		empty=numpy.array([0,0]) 
		return empty
def spread (current,per):
	#print "flocking" 
	flocking_vec=((separation(current)+-3*cohesion(current))+velavg(current))
	if plugin.reset(per)==True:
		#current.set_v_2D_alt_lya(flocking_vec,-8)
		return flocking_vec
	else:
		#current.set_xyz_ned_lya(current.xyz)
		empty=numpy.array([0,0])
                #current.set_v_2D_alt_lya(empty,-8) 
		return empty
def find_fire (current,per):
	print "find_fire" 
	if not(current.temperature_sensor==True):
		 current.set_xyz_ned_lya(current.xyz)
		 return
	if (temperature_sensor(current)>600): #and plugin.reset(per)==True:
		fire=get_position_by_radius(current)
		current.shared_variable(fire,"fire")
		current.set_xyz_ned_lya(current.xyz)
		return True
	flocking_v=flocking(current,per)
	alt_d=8
	current.set_v_2D_alt_lya(flocking_v,-alt_d)
def tend_away_from_fire (current,per):
	print "tend_away_from_fire" 
	if not(current.temperature_sensor==True):
		 current.set_xyz_ned_lya(current.xyz)
		 return False
	target=numpy.array([0,0])
	target=(target-get_coordinates(current))
	target=(target/10)
	target=normalize(target)
	direction=(flocking(current,per)+(-3*target))
	alt_d=8
	current.set_v_2D_alt_lya(direction,-alt_d)
	return False
def go_to_fire_location (current,per):
	print "go_to_fire_location" 
	if not(current.water_cargo==True):
		 current.set_xyz_ned_lya(current.xyz)
		 return False
	target=numpy.array([0,0])
	target=(target-get_coordinates(current))
	target=(target/10)
	target=normalize(target)
	diff=(target-get_coordinates(current))
	direction=(flocking(current,per)+3*target)
	alt_d=8
	current.set_v_2D_alt_lya(direction,-alt_d)
	if ((diff[0]<=0)and(diff[1]<=0)):
		return True
	return False
def turn_down_fire (current):
	print "turn_down_fire" 
	if not(current.water_cargo==True):
		 current.set_xyz_ned_lya(current.xyz)
		 return
def assign_role(current):
	if (current.temperature_sensor==True):
		current.role="fire_locator"
	if (current.water_cargo==True):
		current.role="fire_fighters"
