#! /usr/bin/env python
import copy
from timeit import default_timer as timer


class Task:
    
    def __init__(self):
        self.domains = []
        self.variables = []
        self.offsets = []
        self.sucessor_functions = []
        self.subgoal_functions = []
        self.constraint_functions = []        
        self.ngenerated = 0
        self.time_stamp = timer()
        self.plan = []
        self.relevantAtoms = []
        self.nrelevants = 0
        self.IW1table = []
                
        
    def load_state_variable(self,v,d):
        self.domains = self.domains + [range(d)]        
        self.variables = self.variables + [[self.domains[-1][v]]]
        if self.offsets == []:
            self.offsets = self.offsets + [0]
        else:
            acc = self.offsets[-1] + len(self.domains[-2])
            self.offsets = self.offsets + [acc]

        
    def load_succesor_function(self,f):
        self.sucessor_functions = self.sucessor_functions + [f]

        
    def load_subgoal_function(self,f):
        self.subgoal_functions = self.subgoal_functions + [f]

        
    def load_constraint_function(self,f):
        self.constraint_functions = self.constraint_functions + [f]        
        
        
    def __str__(self):
        sout="\n"
        for index in range(0,len(self.domains)):
            sout = sout + "V" + str(index) +": " + str(self.domains[index]) + "\n"
        
        for index in range(0,len(self.variables)):
            sout = sout + "Init V" + str(index) +": " + str(self.variables[index]) + "\n"

        sout = sout + "Elapsed Time: " + str(timer()-self.time_stamp) + "\n"
        sout = sout + "Generated nodes: " + str(self.ngenerated) + "\n"
        
        if self.plan!=[]:
            sout = sout + "Solution plan:" 
            for a in self.plan:
                sout = sout + " " + a
                
        sout = sout + "\n"
        
        if self.relevantAtoms!=[]:
            sout = sout + str(self.nrelevants) + " Relevant Atoms:"
            i=0
            j=0
            for index in range(len(self.relevantAtoms)):                    
                if self.relevantAtoms[index]==True:
                    sout = sout + " V" + str(i) + "="+ str(j) + ","
                if  j== (len(self.domains[i])-1):
                    i = i + 1
                    j = 0
                else:
                    j = j + 1
                                                                
        return sout
        

