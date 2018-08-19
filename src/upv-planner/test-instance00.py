#! /usr/bin/env python
import sys, copy
import planner
from planner import Task, Planner_IW1, Planner_BFWS
      
# Instance 00
MAX_VARS=5
MAX_VAL=100

# Goal Conditions
def subgoal0(state):
    if (state[0][0]==89):
        return True
    else:
        return False

def subgoal1(state):
    if (state[1][0]==12):
        return True
    else:
        return False    

def subgoal2(state):
    if (state[2][0]==75):
        return True
    else:
        return False

def subgoal3(state):
    if (state[3][0]==65):
        return True
    else:
        return False

def subgoal4(state):
    if (state[4][0]==5):
        return True
    else:
        return False        

    
# Actions   
def inc_V0(state):
    state[0][0]=(state[0][0]+1)%MAX_VAL
    return state

def dec_V0(state):
    state[0][0]=(state[0][0]-1)%MAX_VAL
    return state

def inc_V1(state):
    state[1][0]=(state[1][0]+1)%MAX_VAL
    return state

def dec_V1(state):
    state[1][0]=(state[1][0]-1)%MAX_VAL
    return state

def inc_V2(state):
    state[2][0]=(state[2][0]+1)%MAX_VAL
    return state

def dec_V2(state):
    state[2][0]=(state[2][0]-1)%MAX_VAL
    return state

def inc_V3(state):
    state[3][0]=(state[3][0]+1)%MAX_VAL
    return state

def dec_V3(state):
    state[3][0]=(state[3][0]-1)%MAX_VAL
    return state

def inc_V4(state):
    state[4][0]=(state[4][0]+1)%MAX_VAL
    return state

def dec_V4(state):
    state[4][0]=(state[4][0]-1)%MAX_VAL
    return state


# Creating the task
t = Task.Task()

for i in range(0,MAX_VARS):
    t.load_state_variable(50,range(MAX_VAL))

t.load_subgoal_function(subgoal0)
t.load_subgoal_function(subgoal1)
t.load_subgoal_function(subgoal2)
t.load_subgoal_function(subgoal3)
t.load_subgoal_function(subgoal4)

t.load_succesor_function(inc_V0)
t.load_succesor_function(dec_V0)
t.load_succesor_function(inc_V1)
t.load_succesor_function(dec_V1)
t.load_succesor_function(inc_V2)
t.load_succesor_function(dec_V2)
t.load_succesor_function(inc_V3)
t.load_succesor_function(dec_V3)
t.load_succesor_function(inc_V4)
t.load_succesor_function(dec_V4)

# Running the IW1 planner on the task
#p = Planner_IW1.Planner_IW1(t)
#solution_node = p.solve_IW1()


# Running the BFS planner on the task
p = Planner_BFWS.Planner_BFWS(t)            
solution_node = p.solve_BFWS()

if solution_node !=None:
    t.get_plan_relevant_atoms(solution_node)
    print t
    print solution_node
sys.exit(0)
