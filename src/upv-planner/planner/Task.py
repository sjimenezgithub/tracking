#! /usr/bin/env python
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
                        
        
    def load_state_variable(self,value,domain):
        if (value in domain):
            self.domains = self.domains + [domain]        
            self.variables = self.variables + [[value]]
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
        

    def get_plan_relevant_atoms(self, solution_node):
        self.relevantAtoms =  [False for i in range(self.offsets[-1] + len(self.domains[-1]))]
        
        checked = set([])        
        aux_node = solution_node
        while aux_node != None:
            self.plan = [aux_node.action] + self.plan
            for i in range(len(aux_node.state)):
                index = self.offsets[i] + aux_node.state[i][0]
                if (not index in checked):
                    self.relevantAtoms[index]=True
                    checked.add(index)
            aux_node = aux_node.parent
            
        self.nrelevants = self.relevantAtoms.count(True)

        
    def __str__(self):
        sout="\n"       
        for index in range(0,len(self.variables)):
            sout = sout + "V" + str(index) +" inited to " + str(self.variables[index]) + " in Domain " + str(self.domains[index]) + "\n"

        sout = sout + "Elapsed Time: " + str(timer()-self.time_stamp) + "\n"
        sout = sout + "Generated nodes: " + str(self.ngenerated) + "\n"
        
        if self.plan!=[]:
            sout = sout + "Solution plan (" + str(len(self.plan)-1) + " actions):" 
            for a in self.plan:
                sout = sout + " " + a
                
        sout = sout + "\n"
        
        if self.relevantAtoms!=[]:
            sout = sout + "Relevant Atoms (" + str(self.nrelevants) + "):"
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

    

