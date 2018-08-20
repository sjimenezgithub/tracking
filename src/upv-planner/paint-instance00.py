#! /usr/bin/env python
import sys, copy
import planner
from planner import Task, Planner_IW1, Planner_BFWS
      
# Instance 00
GRID_SIZE=10

# Goal Conditions
def subgoal0(state):
    return (state[12][0]==1)

def subgoal1(state):
    return (state[13][0]==1)

def subgoal2(state):
    return (state[14][0]==1)

def subgoal3(state):
    return (state[15][0]==1)

def subgoal4(state):
    return (state[16][0]==1)

def subgoal5(state):
    return (state[17][0]==1)

    
# Actions   
def inc_V0(state):
    state[0][0]=(state[0][0]+1)%GRID_SIZE
    return state

def dec_V0(state):
    state[0][0]=(state[0][0]-1)%GRID_SIZE
    return state

    
def inc_V1(state):
    state[1][0]=(state[1][0]+1)%GRID_SIZE
    return state    

def dec_V1(state):
    state[1][0]=(state[1][0]-1)%GRID_SIZE
    return state

def visit_V0_V1(state):
    index = state[0][0]*GRID_SIZE + state[1][0] + 2
    state[index][0] = 1
    return state


# Creating the task
t = Task.Task()

t.load_state_variable(0,range(GRID_SIZE))
t.load_state_variable(0,range(GRID_SIZE))
for i in range(0,GRID_SIZE):
    for j in range(0,GRID_SIZE):    
        t.load_state_variable(0,range(2))

t.load_subgoal_function(subgoal0,[12])
t.load_subgoal_function(subgoal1,[13])
t.load_subgoal_function(subgoal2,[14])
t.load_subgoal_function(subgoal3,[15])
t.load_subgoal_function(subgoal4,[16])
t.load_subgoal_function(subgoal5,[17])

t.load_succesor_function(inc_V0, [0])
t.load_succesor_function(dec_V0, [0])
t.load_succesor_function(inc_V1, [1])
t.load_succesor_function(dec_V1, [1])
t.load_succesor_function(visit_V0_V1, [0,1])


# Running the BFS planner on the task
p = Planner_BFWS.Planner_BFWS(t)            
solution_node = p.solve_BFWS()

if solution_node != None:
    t.get_plan_relevant_atoms(solution_node)
    print t
    print solution_node
sys.exit(0)


    
