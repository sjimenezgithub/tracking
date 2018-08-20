#! /usr/bin/env python
import copy
import Node,Task,Planner_IW1
from constraint import *

MAX_NODES = 100000

class Planner_BFWS:

    def __init__(self,t):
        
        self.task = t
        
        print ("Initializing BFWS relevance table")
        self.task.relevantAtoms = [False for i in range(self.task.offsets[-1] + len(self.task.domains[-1]))]
        self.get_relevantAtoms_with_IW1()
#        self.get_relevantAtoms_with_RP()

        print ("\nInitializing hmax novelty tables")
        self.task.nrelevants = self.task.relevantAtoms.count(True)
        self.task.H_MAX = len(self.task.subgoal_functions) * self.task.nrelevants + self.task.nrelevants + 1 
        self.task.IW1table = [False for i in range(self.task.H_MAX) * (self.task.offsets[-1] + len(self.task.domains[-1]))]


    def get_relevantAtoms_with_IW1(self):
        # Computing the relevant atoms for each subgoal
        for g in range(len(self.task.subgoal_functions)):
            # Creating the sub-task            
            print (" --- subtask" + str(g) + " ---")
            t_g = Task.Task()                     
            for i in range(len(self.task.variables)):                            
                 t_g.load_state_variable(self.task.variables[i][0],self.task.domains[i])
            for i in range(len(self.task.sucessor_functions)):
                t_g.load_succesor_function(self.task.sucessor_functions[i],self.task.sucessor_indexes[i])
            for f in self.task.constraint_functions:
                t_g.load_constraint_function(f)                                
            t_g.load_subgoal_function(self.task.subgoal_functions[g],self.task.sucessor_indexes[g])

            # Addressing the sub-task with IW1
            p = Planner_IW1.Planner_IW1(t_g)
            solution_node = p.solve_IW1()

            # Merge the found relevant atoms
            if solution_node != None:
                t_g.get_plan_relevant_atoms(solution_node)
                print ("Relevant atoms found: " + str(t_g.nrelevants))
                print ("Subplan found: " + str(t_g.plan))
                for index in range(len(self.task.relevantAtoms)):
                    if self.task.relevantAtoms[index] == False and t_g.relevantAtoms[index] == True:
                        self.task.relevantAtoms[index] = True

                        
    # !!! Work in progress !!!
    def get_relevantAtoms_with_RP(self):
        # get sucessors
        states = [self.task.sucessor_functions[i](copy.deepcopy(self.task.variables)) for i in range(len(self.task.sucessor_functions))]

        # merge sucessors
        sets=[]
        for i in range(len(self.task.variables)):
            aux = [s[i] for s in states]
            sets.append(list(set([item for sublist in aux for item in sublist])))
        print sets

        # check subgoals
        problem = Problem()
        for i in range(len(self.task.variables)):
            problem.addVariable("V" + str(i), sets[i])

        for g in range(len(self.task.subgoal_functions)):            
            problem.addConstraint(lambda a, b: a*2 == b, ("a", "b"))            
            
        problem.getSolutions()
            
       
                
    def solve_BFWS(self):
        print ("Starting BFWS search")
        
        # Root node
        root_node = Node.heuristic_Node(None,None,copy.deepcopy(self.task.variables),self.task)
        if root_node.get_achieved_subgoals(self.task) == len(self.task.subgoal_functions):                                        
            return root_node        

        open_set = set([root_node])
        closed_set = set([])
        self.task.ngenerated = 1
        best_h = self.task.H_MAX
        
        # Search                
        while(open_set):

            # get best open node
            node = min(open_set, key=lambda o:o.f_novelty(self.task))
            open_set.remove(node)
            closed_set.add(str(node.state))
            if node.f_novelty(self.task) < best_h:
                print "Best heuristic value found: " + str(node.h)
                best_h = node.f_novelty(self.task)
            
            # expand node
            succesor_nodes = [Node.heuristic_Node(node,i,self.task.sucessor_functions[i](copy.deepcopy(node.state)),self.task) for i in range(len(self.task.sucessor_functions))] 
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
