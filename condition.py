#!/usr/bin/env python
class Condition:
 max_count=0
 time_out=0
 def __init__(self,max_count,time_out):
	self.max_count=max_count
	self.time_out=time_out
 def ConditionSatisfied(self):
	self.condition_status=True
 
 def getConditionStatus(self):
	return  self.condition_status
