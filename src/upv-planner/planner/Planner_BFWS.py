#! /usr/bin/env python
import copy
import Node,Task,Planner_IW1

MAX_NODES = 100000

class Planner_BFWS:

    def __init__(self,t):
        
        self.task = t
        
        print ("Initializing BFWS relevance table")
        self.task.relevantAtoms = [False for i in range(self.task.offsets[-1] + len(self.task.domains[-1]))]
        
        # Computing the relevant atoms for each subgoal
        for g in range(len(self.task.subgoal_functions)):
            print (" --- subtask" + str(g) + " ---")

            # Creating the sub-task            
            t_g = Task.Task()                     
            for i in range(len(self.task.variables)):                            
                 t_g.load_state_variable(0,self.task.domains[i])
            for f in self.task.sucessor_functions:
                t_g.load_succesor_function(f)
            for f in self.task.constraint_functions:
                t_g.load_constraint_function(f)                                
            t_g.load_subgoal_function(self.task.subgoal_functions[g])

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

        print ("\nInitializing hmax novelty tables")
        self.task.nrelevants = self.task.relevantAtoms.count(True)
        H_MAX = self.task.nrelevants + 1
        self.task.IW1table = [False for i in range(H_MAX) * (self.task.offsets[-1] + len(self.task.domains[-1]))]        

                
    def solve_BFWS(self):
        print ("Starting BFWS search")
        
        # Root node
        root_node = Node.heuristic_Node(None,"-Init-",copy.deepcopy(self.task.variables),self.task)            

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
