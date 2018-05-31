#!/usr/bin/env python
from transition import Transition 
from random import randint

class State:
 name=None
 role=None
 event=None
 transition=None
 next=None
 current=None
 complete=False
 drone_id=None
 condition=None
 def __init__(self,name, role, action_method,current,condition):
	self.name=name
	self.role=role
	self.event=action_method
	self.current=current
        self.condition=condition
	self.drone_id=[]
 def get_Next(self):
	return next
 
 def set_Name(self, next):
	self.next=next

 def execute(self,per):
	result=self.event(self.current,per)
	
	if result==True:
	   self.complete=True


 def create_Transition(self,condition):
	self.transition=Transition(self,condition,self.next)
 
 def getNext(self):
	if self.transition.condition.getConditionStatus()==True: 
		return self.next
	


