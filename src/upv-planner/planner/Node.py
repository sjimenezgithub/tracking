#! /usr/bin/env python
import Task

class Node:
    
    def __init__(self,p,a,s):
        self.parent = p
        self.action = a        
        self.state = s


    def __str__(self):
        sout = ""
        sout = sout + str(self.action) + "\n"       
        
        for index in range(len(self.state)):
            sout = sout + "V" + str(index) +" :" + str(self.state[index]) + "\n"
                       
        return sout


    def novelty_test(self,task):
        novelty = 0
        for i in range(0,len(self.state)):
            index = task.offsets[i] + self.state[i][0]
            if task.IW1table[index]==False:
                task.IW1table[index] = True
                novelty = 1            
        return novelty
                            

    def get_achieved_subgoals(self,task):
        achieved_subgoals=0
        for f in task.subgoal_functions:
            if f(self.state):
                achieved_subgoals = achieved_subgoals + 1
        return achieved_subgoals
    

    def get_achieved_relevance(self,task):        
        checked = set([])        
        aux_node = self
        while aux_node != None:
            for i in range(len(aux_node.state)):
                index = task.offsets[i]+aux_node.state[i][0]
                if task.relevantAtoms[index]==True and (not index in checked):
                    checked.add(index)
            aux_node = aux_node.parent
        return len(checked)
               
    
class heuristic_Node(Node):
    def __init__(self,p,a,s,task):
        Node.__init__(self, p,a,s)
        
        if self.parent == None:
            self.g = 0
        else:
            self.g = self.parent.g + 1            

        self.h = self.h_subgoals_relAtoms(task)


    def __str__(self):
        sout =  Node.__str__(self)
        sout = sout + "g: " + str(self.g) + "\n"
        sout = sout + "h: " + str(self.h) + "\n"                       
        return sout        


    def heuristic_novelty_test(self, task):
        novelty = 0
        offset = self.h * (task.offsets[-1] + len(task.domains[-1]))
        for i in range(len(self.state)):
            index = offset + task.offsets[i] + self.state[i][0]
            if task.IW1table[index] == False:
                task.IW1table[index] = True
                novelty = 1
        return novelty        
    
    
    def h_subgoals(self,task):
        return len(task.subgoal_functions) - self.get_achieved_subgoals(task)

    
    def h_relevantAtoms(self,task):
        return task.nrelevants - self.get_achieved_relevance(task)

    def h_subgoals_relAtoms(self,task):
        return self.h_subgoals(task) * task.nrelevants + self.h_relevantAtoms(task)

    
    def h_novelty(self,task):
        if self.heuristic_novelty_test(task) == 1:
            return self.h_subgoals(task) * task.nrelevants + self.h_relevantAtoms(task)
        else:
            return len(task.subgoal_functions) * task.nrelevants + self.h_relevantAtoms(task)

