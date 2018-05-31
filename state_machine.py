#!/usr/bin/env python
from state import State 
from transition import Transition 
from condition import Condition 
import sequence_rules as sim
import time

class StateMachine:
 states=None
 initial_state=None
 last_state=None
 current_state=None
 current=None
 count=1
 flag=None
 timer=None
 def __init__(self,current):
	self.states=[]
 	self.current=current
 	self.build()
	self.flag=False
	self.timer=[]
 def create_initial_state(self,name, role, action_method,condition):
	state=State(name,role,action_method,self.current,condition)
	self.initial_state=state
	self.last_state=state
	self.current_state=self.initial_state
	#print "state ",self.count,state.name
	self.count=self.count+1
	self.states.append(state)
	return self
 	
 def create_state(self,name, role, action_method,condition):
	state=State(name,role,action_method,self.current,condition)
	self.last_state.next=state
	self.last_state=state
	#print "state ",self.count,state.name
	self.count=self.count+1
	self.states.append(state)
	return self
 
 def receive_message(self,new_state):
	 if self.current_state.next!=None:
	 	self.update_state(new_state,self.current_state.next)
		
 def reset(self):
	self.current=self.initial_state
 def update_state(self,new_state,current_state):
	if current_state==None:
		return 
	elif current_state.name==new_state.name:
		self.current_state=current_state
		return
	elif(current_state.next!=None): self.update_state(new_state,current_state.next)
		
 def execute(self, state,t,per):	
	if self.current_state.next!=None  and len(state.drone_id)==state.condition.max_count:
		 self.current_state=self.current_state.next
		 self.timer.append(t)
	state.execute(per)
 
			
 def send_message(self):
	return self.current_state


 def trigger_state_change(self,state):
	if state!=self.current_state:
		return True
	else: return False

 def print_states(self,state):
	print "current state= ",state.name
	if state.next==None:
		return
	self.print_states(state.next)
 
 def build(self):
      self.create_initial_state("s1","fire_locator",sim.find_fire,Condition(3,0)).create_state("s2","fire_fighters",sim.go_to_fire_location,Condition(3,0)).create_state("s3","fire_locator",sim.tend_away_from_fire,Condition(3,0))
