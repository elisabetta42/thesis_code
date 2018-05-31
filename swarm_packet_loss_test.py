#!/usr/bin/env python
from scipy import linalg as la
import copy
import matplotlib.pyplot as pl
import numpy as np
import numpy
import formation_distance as form
import quadrotor as quad
import quadlog
import animation as ani
#import pycopter_rules as rules
import rules as rules
import temperature_function as temperature
from sys import exit
#import plugin
from group import Group
import time as tim
import math
#from statistics import mean
# Quadrotor
m = 0.65 # Kg
l = 0.23 # m
Jxx = 7.5e-3 # Kg/m^2
Jyy = Jxx
Jzz = 1.3e-2
Jxy = 0
Jxz = 0
Jyz = 0
J = np.array([[Jxx, Jxy, Jxz], \
              [Jxy, Jyy, Jyz], \
              [Jxz, Jyz, Jzz]])
CDl = 9e-3
CDr = 9e-4
kt = 3.13e-5  # Ns^2
km = 7.5e-7   # Ns^2
kw = 1/0.18   # rad/s

# Initial conditions
att_0 = np.array([0.0, 0.0, 0.0])
pqr_0 = np.array([0.0, 0.0, 0.0])
xyz1_0 = np.array([1.0, 1.2, 0.0])
xyz2_0 = np.array([2.2, 2.0, 0.0])
xyz3_0 = np.array([-3.1, 20.6, 0.0])

xyz4_0 = np.array([12.0, 8.2, 0.0])
xyz5_0 = np.array([10.2, 9.0, 0.0])
xyz6_0 = np.array([-11.2, 10.6, 0.0])

v_ned_0 = np.array([0.0, 0.0, 0.0])
w_0 = np.array([0.0, 0.0, 0.0, 0.0])

# Setting quads
q1 = quad.quadrotor(1, m, l, J, CDl, CDr, kt, km, kw, \
        att_0, pqr_0, xyz1_0, v_ned_0, w_0)

q2 = quad.quadrotor(2, m, l, J, CDl, CDr, kt, km, kw, \
        att_0, pqr_0, xyz2_0, v_ned_0, w_0)

q3 = quad.quadrotor(3, m, l, J, CDl, CDr, kt, km, kw, \
        att_0, pqr_0, xyz3_0, v_ned_0, w_0)

q4 = quad.quadrotor(4, m, l, J, CDl, CDr, kt, km, kw, \
        att_0, pqr_0, xyz4_0, v_ned_0, w_0)

q5 = quad.quadrotor(5, m, l, J, CDl, CDr, kt, km, kw, \
        att_0, pqr_0, xyz5_0, v_ned_0, w_0)

q6 = quad.quadrotor(6, m, l, J, CDl, CDr, kt, km, kw, \
        att_0, pqr_0, xyz6_0, v_ned_0, w_0)
quad_list=[]
quad_list.append(q1)
quad_list.append(q2)
quad_list.append(q3)

quad_list.append(q4)
quad_list.append(q5)
quad_list.append(q6)

# Formation Control
# Shape
side = 8
Btriang = np.array([[1, 0, -1],[-1, 1, 0],[0, -1, 1]])
dtriang = np.array([side, side, side])

# Motion
mu = 0e-2*np.array([1, 1, 1])
tilde_mu = 0e-2*np.array([1, 1, 1])

fc = form.formation_distance(2, 1, dtriang, mu, tilde_mu, Btriang, 5e-2, 5e-1)

# Simulation parameters
tf = 150
dt = 5e-2
time = np.linspace(0, tf, tf/dt)
it = 0
frames = 100

# Data log
q1_log = quadlog.quadlog(time)
q2_log = quadlog.quadlog(time)
q3_log = quadlog.quadlog(time)

q4_log = quadlog.quadlog(time)
q5_log = quadlog.quadlog(time)
q6_log = quadlog.quadlog(time)

Ed_log = np.zeros((time.size, fc.edges))

# Plots
quadcolor = ['r', 'g', 'b']
pl.close("all")
pl.ion()
fig = pl.figure(0)
axis3d = fig.add_subplot(111, projection='3d')

#ax= fig.add_subplot(111, projection='3d')
#ax.set_xlim(-15, 15)
#ax.set_ylim(-15, 15)
#ax.cla()
#temperature.draw_grid(axis3d)

init_area = 5
s = 2
# Make data
#u = np.linspace(0, 2 * np.pi, 100)
#v = np.linspace(0, np.pi, 100)
#x = range(-15,15)
#y = range(-15,15)
#x_1,y_1,z = temperature.create_array(15,15,-15,-15)
# create x,y
#x, y = numpy.meshgrid(range(15), range(15))
#x=numpy.asarray(x)
#y=numpy.asarray(y)
#x, y, z = np.meshgrid(range(-15,15), range(-15,15),range(-15,15))
#z = temperature.create_array(x,y,z)
#z=numpy.asarray(z)
#pl.pause(0)
#exit(0)

# Desired altitude and heading
alt_d = 4
q1.yaw_d =  -np.pi
q2.yaw_d =  -np.pi
q3.yaw_d =  -np.pi

q4.yaw_d =  -np.pi
q5.yaw_d =  -np.pi
q6.yaw_d =  -np.pi
radius=50
quad_list[0].water_cargo=True
quad_list[1].water_cargo=True
quad_list[2].water_cargo=True
quad_list[3].temperature_sensor=True
quad_list[4].temperature_sensor=True
quad_list[5].temperature_sensor=True

times=[]
result=[]
#times.append(0)
packets=range(0,101,10)
complete_pac=[]
list_of_list=[]
average=[]
std=[]
for drone in quad_list:
	drone.group.syncronize(drone,quad_list,radius)
for p in range(0,11):
 #list_of_list=list_of_list+times
 list_of_list.append(copy.deepcopy(times))
 #print "list of lists", list_of_list
 #print times, "times"
 times[:]=[] 
 for per in range(0,11):
  print packets[p], "percentage of packet loss"
  q1.xyz=xyz1_0 
  q2.xyz=xyz2_0 
  q3.xyz=xyz3_0 

  q4.xyz=xyz4_0
  q5.xyz=xyz5_0
  q6.xyz=xyz6_0
  count=0
  for t in time:  	
    radius=25
    completed=True
    for current in quad_list:
	   #if t > 120:
           #     print "spreading..........................................."
           rules.flocking(current,packets[p])
           #else: 
	   #	rules.flocking(current,packets[p])
           position=current.xyz
       	   for other in quad_list:
	 	if current.tag!=other.tag:
	          neighbour=other.xyz
	          distance=math.sqrt(pow((position[0] - neighbour[0]), 2) + pow((position[1] -neighbour[1]), 2))
	          #print distance
	          if distance<=radius:
			completed=False
                        
			
    if completed==True:	
    	    count=count+1
            

    if count==1:
        print "times added"
	times.append(t)
    #    if per==0:
        if packets[p] not in complete_pac:
        	complete_pac.append(packets[p])
        #break;
   
    
    for d in quad_list:
    	d.step(dt)
  
    
    if it%frames == 0:
        axis3d.cla()
	

        ani.draw3d(axis3d, q1.xyz, q1.Rot_bn(), quadcolor[0])
	ani.draw3d(axis3d, q2.xyz, q2.Rot_bn(), quadcolor[0])
	ani.draw3d(axis3d, q3.xyz, q3.Rot_bn(), quadcolor[0])
	
	ani.draw3d(axis3d, q4.xyz, q4.Rot_bn(), quadcolor[0])
	ani.draw3d(axis3d, q5.xyz, q5.Rot_bn(), quadcolor[0])
	ani.draw3d(axis3d, q6.xyz, q6.Rot_bn(), quadcolor[0])
	
	
	
	        
	
	axis3d.set_xlim(-15, 15)
        axis3d.set_ylim(-15, 15)
        axis3d.set_zlim(0, 15)
        axis3d.set_xlabel('South [m]')
        axis3d.set_ylabel('East [m]')
        axis3d.set_zlabel('Up [m]')
        axis3d.set_title("Time %.3f s" %t)
	
	temperature.draw_grid(axis3d)
	
        pl.pause(0.01)
        pl.draw()

    it+=1
 
# Stop if crash
    #if (q1.crashed == 1):
    #    break
    
    #print len(complete_pac),complete_pac
    #print len(times),times,"time"
#print times
	
 '''        # Log
    q1_log.xyz_h[it, :] = q1.xyz
    q1_log.att_h[it, :] = q1.att
    q1_log.w_h[it, :] = q1.w
    q1_log.v_ned_h[it, :] = q1.v_ned
    q1_log.xi_g_h[it] = q1.xi_g
    q1_log.xi_CD_h[it] = q1.xi_CD

	 # Log
    q2_log.xyz_h[it, :] = q2.xyz
    q2_log.att_h[it, :] = q2.att
    q2_log.w_h[it, :] = q2.w
    q2_log.v_ned_h[it, :] = q2.v_ned
    q2_log.xi_g_h[it] = q2.xi_g
    q2_log.xi_CD_h[it] = q2.xi_CD


 	# Log
    q3_log.xyz_h[it, :] = q3.xyz
    q3_log.att_h[it, :] = q3.att
    q3_log.w_h[it, :] = q3.w
    q3_log.v_ned_h[it, :] = q3.v_ned
    q3_log.xi_g_h[it] = q3.xi_g
    q3_log.xi_CD_h[it] = q3.xi_CD


	  # Log
    q4_log.xyz_h[it, :] = q4.xyz
    q4_log.att_h[it, :] = q4.att
    q4_log.w_h[it, :] = q4.w
    q4_log.v_ned_h[it, :] = q4.v_ned
    q4_log.xi_g_h[it] = q4.xi_g
    q4_log.xi_CD_h[it] = q4.xi_CD

	 # Log
    q5_log.xyz_h[it, :] = q5.xyz
    q5_log.att_h[it, :] = q5.att
    q5_log.w_h[it, :] = q5.w
    q5_log.v_ned_h[it, :] = q5.v_ned
    q5_log.xi_g_h[it] = q5.xi_g
    q5_log.xi_CD_h[it] = q5.xi_CD


 	# Log
    q6_log.xyz_h[it, :] = q6.xyz
    q6_log.att_h[it, :] = q6.att
    q6_log.w_h[it, :] = q6.w
    q6_log.v_ned_h[it, :] = q6.v_ned
    q6_log.xi_g_h[it] = q6.xi_g
    q6_log.xi_CD_h[it] = q6.xi_CD
    
    



pl.figure(7)
pl.xlabel('Time [s]')
pl.ylabel('x coordinate [m]')
pl.plot(time, q1_log.xyz_h[:, 0], label="UAV 1")
pl.plot(time, q2_log.xyz_h[:, 0], label="UAV 2")
pl.plot(time, q3_log.xyz_h[:, 0], label="UAV 3")
pl.plot(time, q4_log.xyz_h[:, 0], label="UAV 4")
pl.plot(time, q5_log.xyz_h[:, 0], label="UAV 5")
pl.plot(time, q6_log.xyz_h[:, 0], label="UAV 6")
pl.legend()

pl.figure(8)
pl.xlabel('Time [s]')
pl.ylabel('y coordinate [m]')
pl.plot(time, q1_log.xyz_h[:, 1], label="UAV 1")
pl.plot(time, q2_log.xyz_h[:, 1], label="UAV 2")
pl.plot(time, q3_log.xyz_h[:, 1], label="UAV 3")
pl.plot(time, q4_log.xyz_h[:, 1], label="UAV 4")
pl.plot(time, q5_log.xyz_h[:, 1], label="UAV 5")
pl.plot(time, q6_log.xyz_h[:, 1], label="UAV 6")
pl.legend()'''

print "I am here"
print list_of_list
for ind,value in enumerate(list_of_list):
        if len(list_of_list[ind])>=1:
                print list_of_list[ind]
		average.append(numpy.mean(list_of_list[ind]))
		std.append(numpy.std(list_of_list[ind], axis=0))
#print times
#for i in range(1,8):
#	print [sum(list_of_list[i:i+8]) for i in range(0, len(list_of_list), i)], "sum"

		
print average, "avg"		
print complete_pac, "cp"

pl.figure(6)
pl.ylabel('Time [s]')
pl.xlabel('Packets loss [percentage]')
reverse=complete_pac[::-1]
for i in range(len(reverse)):
  reverse[i] -= 10
#e=std*1;
print reverse, "reverse"
pl.scatter(reverse[0:len(average)],average, alpha=0.8)
pl.plot(reverse[0:len(average)],average)
pl.errorbar(reverse[0:len(average)],average, std, linestyle='None', marker='^')

pl.pause(0)




        
