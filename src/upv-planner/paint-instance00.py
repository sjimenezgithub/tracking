#! /usr/bin/env python
import sys, copy
import planner
from planner import Task, Planner_IW1, Planner_BFWS
      
# Instance 00
GRID_SIZE=10

# Goal Conditions
def subgoal0(state):
    return (state[53][0]==1)
def subgoal1(state):
    return (state[54][0]==1)
def subgoal2(state):
    return (state[55][0]==1)
def subgoal3(state):
    return (state[56][0]==1)
def subgoal4(state):
    return (state[57][0]==1)
def subgoal5(state):
    return (state[58][0]==1)
def subgoal6(state):
    return (state[59][0]==1)
def subgoal7(state):
    return (state[60][0]==1)
def subgoal8(state):
    return (state[61][0]==1)
def subgoal9(state):
    return (state[62][0]==1)
def subgoal10(state):
    return (state[63][0]==1)

    
# Actions   
def inc_V0(state):
    if state[0][0] < (GRID_SIZE-1):
        state[0][0] = (state[0][0]+1)
    return state

def inc_V1(state):
    if state[1][0] < (GRID_SIZE-1):
        state[1][0] = (state[1][0]+1)
    return state

def dec_V0(state):
    if state[0][0] > 0:
        state[0][0] = (state[0][0]-1)
    return state

def dec_V1(state):
    if state[1][0]  > 0:
        state[1][0] = (state[1][0]-1)
    return state

def visit_V0_V1(state):
    index = state[0][0]*GRID_SIZE + state[1][0] + 2
    state[index][0] = 1
    return state


# Creating the task
t = Task.Task()

t.load_state_variable(0,GRID_SIZE)
t.load_state_variable(0,GRID_SIZE)
for i in range(0,GRID_SIZE):
    for j in range(0,GRID_SIZE):    
        t.load_state_variable(0,1)

t.load_subgoal_function(subgoal0)
t.load_subgoal_function(subgoal1)
t.load_subgoal_function(subgoal2)
t.load_subgoal_function(subgoal3)
t.load_subgoal_function(subgoal4)
t.load_subgoal_function(subgoal5)
t.load_subgoal_function(subgoal6)
t.load_subgoal_function(subgoal7)
t.load_subgoal_function(subgoal8)
t.load_subgoal_function(subgoal9)
t.load_subgoal_function(subgoal10)

t.load_succesor_function(inc_V0)
t.load_succesor_function(inc_V1)
t.load_succesor_function(dec_V0)
t.load_succesor_function(dec_V1)


# Running the IW1 planner on the task
#p = Planner_IW1.Planner_IW1(t)
#print ("Starting IW1 search")
#solution_node = p.solve_IW1()


# Running the BFS planner on the task
p = Planner_BFWS.Planner_BFWS(t)
print ("Starting BFWS search")            
solution_node = p.solve_BFWS()

if solution_node !=None:
    solution_node.get_path_info(t)
print solution_node
print t
sys.exit(0)


    