#! /usr/bin/env python
import copy, numpy
import Node

MAX_NODES = 100000

class Planner_IW1:
    
    def __init__(self,t):
        self.task = t 
        
        print ("Initializing novelty table")
        self.task.IW1table = [False for i in range(self.task.offsets[-1] + len(self.task.domains[-1]))]
                           
                
    def solve_IW1(self):

        # Root node
        root_node = Node.Node(None,"-Init-",copy.deepcopy(self.task.variables))
        if root_node.get_achieved_subgoals(self.task) == len(self.task.subgoal_functions):
            return root_node

        root_node.novelty_test(self.task)
        open_list = [root_node]
        self.task.ngenerated = 1
        
        # Search                
        while(open_list):

            node = open_list.pop(0)
 
            succesor_nodes = [Node.Node(node,"action"+str(i),self.task.sucessor_functions[i](copy.deepcopy(node.state))) for i in range(0,len(self.task.sucessor_functions))]
            
            for succesor in succesor_nodes:
                # Constraint test
                for f in self.task.constraint_functions:
                    if not f(succesor.state):    
                        continue
                
                # Goal test
                if succesor.get_achieved_subgoals(self.task) == len(self.task.subgoal_functions):                                        
                    return succesor                

                # Memory bound test                
                if len(open_list)>MAX_NODES:
                    print "Goal not found: memory exhausted\n"
                    return None                
                
                # Adding succesor to the open list
                if succesor.novelty_test(self.task)==1:
                    open_list.append(succesor)
                    self.task.ngenerated = self.task.ngenerated + 1
                                            
        print "Goal not found: Exhausted search space!!!\n"                
        return None

