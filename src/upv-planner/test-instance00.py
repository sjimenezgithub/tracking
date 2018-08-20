#! /usr/bin/env python
import sys, copy
import planner
from planner import Task, Planner_IW1, Planner_BFWS

# Instance 00
MAX_VARS=5
MAX_VAL=100


# Goal Conditions
def eq0(X):
    if (X==89):
        return True
    else:
        return False

def eq1(X):
    if (X==12):
        return True
    else:
        return False    

def eq2(X):
    if (X==75):
        return True
    else:
        return False

def eq3(X):
    if (X==65):
        return True
    else:
        return False

def eq4(X):
    if (X==5):
        return True
    else:
        return False        

    
# Actions
def inc(X):
    X = (X+1)%MAX_VAL
    return X

def dec(X):
    X = (X-1)%MAX_VAL
    return X


# Creating the task
t = Task.Task()

for i in range(0,MAX_VARS):
    t.load_state_variable(50,range(MAX_VAL))

t.load_subgoal_function(eq0,[0])
t.load_subgoal_function(eq1,[1])
t.load_subgoal_function(eq2,[2])
t.load_subgoal_function(eq3,[3])
t.load_subgoal_function(eq4,[4])

t.load_succesor_function(inc, [0])
t.load_succesor_function(dec, [0])
t.load_succesor_function(inc, [1])
t.load_succesor_function(dec, [1])
t.load_succesor_function(inc, [2])
t.load_succesor_function(dec, [2])
t.load_succesor_function(inc, [3])
t.load_succesor_function(dec, [3])
t.load_succesor_function(inc, [4])
t.load_succesor_function(dec, [4])

sucessors = []
for i in range(len(t.sucessor_functions)):
    str_params = "(" + "".join(["t.variables[" + str(v) + "][0]" for v in t.sucessor_indexes[i]]) + ")"

    eval(t.sucessor_functions[i].__name__ + str_params)
    
    sucessors.append(sucessor)



sys.exit(0)


# Running the IW1 planner on the task
#p = Planner_IW1.Planner_IW1(t)
#solution_node = p.solve_IW1()


# Running the BFS planner on the task
p = Planner_BFWS.Planner_BFWS(t)            
solution_node = p.solve_BFWS()

# Show Results
if solution_node !=None:
    t.get_plan_relevant_atoms(solution_node)
    print t
    print solution_node
sys.exit(0)
