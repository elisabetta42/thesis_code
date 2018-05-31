import plugin
import copy
import random
from random import randint
class Group:
 all_drones=[]
 def __init__(self):
	self.fire_list=[]
 	self.neibourgh_list=[]
 	self.neibourgh_id_list=[]
	
 def update_neibourgh_list(self, drone_list):
	temp=copy.deepcopy(self.neibourgh_id_list[:])
	#print "temp",temp
	self.neibourgh_id_list=[]
	for drone in drone_list:
		self.neibourgh_id_list.append(drone.tag)
	#print "new list", self.neibourgh_id_list
	self.neibourgh_list=drone_list
	diff=list(set(temp)-set(self.neibourgh_id_list))
	diff_drone_ref=[]
	#print len(diff), "difference between set"
	#print diff, "new drones in the flock"
	if len(diff)>0:
	 	#print "I AM MERGING THE FLOCK............................................................................................"		
		random_drone=list(set(self.neibourgh_id_list)-set(diff))
		#print len(random_drone), random_drone, "not new drones"
		if len(random_drone)>0:
			random_index=randint(1, len(random_drone))
			#print random_index, "Random index"	
			for tag in diff:
				diff_drone_ref.append(self.all_drones[tag-1])
				#print "SIZE DIFF_DRONE", len(diff_drone_ref)
			
			for drone in diff_drone_ref:
				#print drone.tag, "drone merging------------"
				self.merge(self.all_drones[random_drone[random_index-1]-1].group.fire_list,drone.group.fire_list,drone)
	

 def publish_point(self,vector):
	for drone in self.neibourgh_list:
		if drone!=self:
			drone.group.receive_message(vector,drone)

 def receive_message(self,vector,current):
	self.add_subscribed_point(current,vector,0)

 def syncronize(self,current,all_drones,radius):
	
	drones=plugin.get_neighbour(current,all_drones,radius)
	self.all_drones=all_drones
	self.update_neibourgh_list(drones)
	
	#print len(self.fire_list), current.tag, "I AM SYNCRONIZING ..."

 def merge(self,other_fire_list,fire_list,drone):
	#print len(other_fire_list),len(fire_list), "LENGTH FIRE LISTS........"
		
	for other in other_fire_list:
		drone.group.add_subscribed_point(drone,other,0)
 
 def add_point(self,current,vector,radius):
	#print current.tag,"I AM ADDING A NODE"
	for other in current.group.fire_list:
		vector.round()
		if other.compare(vector,1)==True:
			#print other.compare(vector,1)
			return None
	current.group.fire_list.append(vector)
	self.publish_point(vector)
	return None
 
 def add_subscribed_point(self,current,vector,radius):
	for other in current.group.fire_list:
		if other.compare_round(vector)==True:
			#print other.compare(vector,radius)
			return None
	current.group.fire_list.append(vector)
	#self.publish_point(vector)
	return None
		
	
	
	
	

    
    
		
