# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 23:02:42 2024

@author: kevin
"""

class State:
    def __init__(self, dirt_status, agent_location):
        self.dirt_status = dirt_status #send a list of the states and room as
        self.agent_location = agent_location #tell which room is the agent (vaccuum)
    
    def actions_possible(self): #defines all the actions possible to apply in the expand function. 
        actions = [] #Create a list of possible actions.
        if self.dirt_status[self.agent_location] == "dirty":
            actions.append("suck")
        if self.agent_location < len(self.dirt_status) - 1:
            actions.append("right")
        if self.agent_location > 0:
            actions.append("left")
        
        return actions
     
    #argument actions is a list of possible actions
    def actions_apply(self,action):
        new_dirt_states = self.dirt_status.copy() #create a variable that copy the list of dirt states
        new_agent_location = self.agent_location #create a vaariable that copy the room of the agent.
        if action == "suck":
            new_dirt_states[self.agent_location] = "clean"
        elif action == "right":
            new_agent_location += 1
        elif action == "left":
            new_agent_location -= 1
            
        return State(new_dirt_states,new_agent_location)
    
    def IS_GOAL(self):
        return all(status == 'clean' for status in self.dirt_status)
    

class Node:
    def __init__(self, state, parent = None,action = None ,path_cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
    

    def expand(self):
        children = []
        action_possible = self.state.actions_possible()
        for action in action_possible:
            new_state = self.state.actions_apply(action)
            new_node = Node(new_state, parent = self, action = action, path_cost= self.path_cost + 1 )
            children.append(new_node)
        return children

                
def BFS(initial_state):
    node = Node(initial_state)
    if node.state.IS_GOAL():
        return node
    frontier = [node] #using list as a data structure for the queue
    reached = []
    while frontier != []:
        current_node = frontier.pop(0)
        reached.append(current_node.state)
        for child in current_node.expand():
            if child.state not in reached and all(not child.state == n.state for n in frontier):
                if child.state.IS_GOAL():
                    return child
                frontier.append(child)
    return None

def solution(node_solution):
    path = []
    while node_solution.parent is not None:
        path.append(node_solution.action)
        node_solution = node_solution.parent
    path.reverse()
    return path
        
    
    
def main():
    rooms = int(input("Enter the number of rooms: "))
    while rooms <= 0:
        print("Wrong input")
        rooms = int(input("Enter a valid number of rooms: "))
    
    dirt_status = [] #Create a list to tell the dirt in each room
    for i in range (rooms) :
        status = input(f"Dirty or clean for room {i+1}: ").lower()
        while status not in ["clean","dirty"]:
            print("Write 'dirty' or 'clean'" )
            status = input(f"Dirty or clean for room {i+1}: ").lower()
        dirt_status.append(status)
    print (dirt_status)

    agent_location = int(input("Enter the location of the vaccum: "))
    while agent_location < 0 or agent_location > rooms-1:
        agent_location = int(input("Please enter a valid number: "))
        
    #create an instance of state with the initial state of the problem
    initial_state = State(dirt_status, agent_location)

    node_solution = BFS(initial_state)
   
    if node_solution:
        actions = solution(node_solution)
        print("\nSolution found!")
        print(f"Initial State: Agent at location {initial_state.agent_location}, Dirt status: {initial_state.dirt_status}")
        print(f"Actions to goal: {actions}")
        print(f"Total actions: {len(actions)}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
                
            
            
            
        
        
