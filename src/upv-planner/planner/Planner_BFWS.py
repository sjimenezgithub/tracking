#! /usr/bin/env python
import copy, heapq, sys
import Node,Task,Planner_IW1

MAX_NODES = 100000

class Planner_BFWS:

    def __init__(self,t):
        
        self.task = t
        
        print ("Initializing relevance table")
        self.task.relevantAtoms = [False for i in range(self.task.offsets[-1] + len(self.task.domains[-1]))]
        
        # Computing the relevant atoms for each subgoal                 
        for g in self.task.subgoal_functions:
            # Creating subtasks
            t_g = Task.Task()            
            
            for i in range(len(self.task.variables)):                            
                 t_g.load_state_variable(0,self.task.domains[i])

            for f in self.task.sucessor_functions:
                t_g.load_succesor_function(f)

            for f in self.task.constraint_functions:
                t_g.load_constraint_function(f)                
                
            t_g.load_subgoal_function(g)

            # Solving sub-task with IW1
            p = Planner_IW1.Planner_IW1(t_g)
            solution_node = p.solve_IW1()
            solution_node.get_path_info(t_g)

            # Merge the found relevant atoms
            for index in range(len(self.task.relevantAtoms)):
                if solution_node != None:
                    if self.task.relevantAtoms[index] == False and t_g.relevantAtoms[index] == True:
                        self.task.relevantAtoms[index] = True
                        self.task.nrelevants = self.task.nrelevants + 1

        if self.task.nrelevants == 0:                        
            # Merge the found atoms
            for index in range(len(self.task.relevantAtoms)):
                if self.task.relevantAtoms[index] == False and p.IW1table[index] == True:
                    self.task.relevantAtoms[index] = True
                    self.task.nrelevants = self.task.nrelevants + 1

        print ("Initializing hmax novelty tables")                        
        self.task.IW1table = [False for i in range(self.task.nrelevants + 1) * (self.task.offsets[-1] + len(self.task.domains[-1]))]

                
    def solve_BFWS(self):

        # Root node
        root_node = Node.heuristic_Node(None,"-Init-",copy.deepcopy(self.task.variables),self.task)            
        if root_node.get_achieved_subgoals(self.task) == len(self.task.subgoal_functions):
            return root_node

        open_set = set([root_node])
        closed_set = set([])
        self.task.ngenerated = 1
        
        # Search                
        while(open_set):

            # get best open node
            node = min(open_set, key=lambda o:o.h_novelty(self.task))
            open_set.remove(node)
            closed_set.add(str(node.state))
 
            succesor_nodes = [Node.heuristic_Node(node,"action"+str(i),self.task.sucessor_functions[i](copy.deepcopy(node.state)),self.task) for i in range(0,len(self.task.sucessor_functions))] 
            for succesor in succesor_nodes:

                # Duplicate nodes test                
                if str(succesor.state) in closed_set:
                    continue

                # Constraint test
                for f in self.task.constraint_functions:
                    if not f(succesor.state):    
                        continue
               
                # Goals test
                if succesor.get_achieved_subgoals(self.task) == len(self.task.subgoal_functions):                                        
                    return succesor

                # Memory bound test                
                if len(open_set)>MAX_NODES:
                    print "Goal not found: memory exhausted\n"
                    return None                                                                        
                                
                # Adding succesor to the open set
                open_set.add(succesor)
                self.task.ngenerated = self.task.ngenerated + 1
                                            
        print "Goal not found: search space exhausted \n"                
        return None

