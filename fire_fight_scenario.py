#!/usr/bin/env python
from scipy import linalg as la
import matplotlib.pyplot as pl
import numpy as np
import numpy
import formation_distance as form
import quadrotor as quad
import quadlog
import animation as ani
#import pycopter_rules as rules
import sequence_rules as rules
import temperature_function as temperature
from sys import exit
#import plugin
from group import Group
import time as tim
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
tf = 170
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
temperature.draw_grid(axis3d)

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

for current in quad_list:
 rules.assign_role(current)
for current in quad_list:
 current.create_ensemble(quad_list,"name")

for drone in quad_list:
	drone.group.syncronize(drone,quad_list,radius)

for t in time:
    for current in quad_list:
                current.group.syncronize(current,quad_list,radius)
    		current.ensemble.synchronize_state(current,t,100)
	        current.step(dt)
    
    if it%frames == 0:
        axis3d.cla()
	
	q1_label=q1.stat_m.current_state.name+" "+str(q1.tag)+" "+str(q1.stat_m.current_state.complete)+" "+q1.role+" "+str(len(q1.var))
	q2_label=q2.stat_m.current_state.name+" "+str(q2.tag)+" "+str(q2.stat_m.current_state.complete)+" "+q2.role+" "+str(len(q2.var))
	q3_label=q3.stat_m.current_state.name+" "+str(q3.tag)+" "+str(q3.stat_m.current_state.complete)+" "+q3.role+" "+str(len(q3.var))
	q4_label=q4.stat_m.current_state.name+" "+str(q4.tag)+" "+str(q4.stat_m.current_state.complete)+" "+q4.role+" "+str(len(q4.var))
	q5_label=q5.stat_m.current_state.name+" "+str(q5.tag)+" "+str(q5.stat_m.current_state.complete)+" "+q5.role+" "+str(len(q5.var))
	q6_label=q6.stat_m.current_state.name+" "+str(q6.tag)+" "+str(q6.stat_m.current_state.complete)+" "+q6.role+" "+str(len(q6.var))

    	axis3d.text2D(0.05, 0.95,q1_label , transform=axis3d.transAxes)
    	axis3d.text2D(0.05, 0.90,q2_label , transform=axis3d.transAxes)
    	axis3d.text2D(0.05, 0.85,q3_label , transform=axis3d.transAxes)
    	axis3d.text2D(0.05, 0.80,q4_label , transform=axis3d.transAxes)
    	axis3d.text2D(0.05, 0.75,q5_label , transform=axis3d.transAxes)
    	axis3d.text2D(0.05, 0.70,q6_label , transform=axis3d.transAxes)
	

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
	
	
	
         # Log
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
    
    

    it+=1
 
# Stop if crash
    if (q1.crashed == 1):
        break



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
pl.legend()



pl.pause(0)






        
