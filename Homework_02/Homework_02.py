# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:53:16 2024

@author: kevin
"""


# Defining the State class
class State:
    def __init__(self, dirt_status, agent_location):
        self.dirt_status = dirt_status  # Send a list of the states and room status
        self.agent_location = agent_location  # Indicate which room the agent (vacuum) is in

    def actions_possible(self):  # Defines all the possible actions to apply in the expand function
        actions = []  # Create a list of possible actions
        if self.dirt_status[self.agent_location] == "dirty":
            actions.append("suck")
        if self.agent_location < len(self.dirt_status) - 1:
            actions.append("right")
        if self.agent_location > 0:
            actions.append("left")
        
        return actions
    
    def actions_apply(self, action):
        new_dirt_states = self.dirt_status.copy()  # Create a variable that copies the list of dirt states
        new_agent_location = self.agent_location  # Create a variable that copies the room of the agent
        if action == "suck":
            new_dirt_states[self.agent_location] = "clean"
        elif action == "right":
            new_agent_location += 1
        elif action == "left":
            new_agent_location -= 1
        
        return State(new_dirt_states, new_agent_location)
    
    def IS_GOAL(self):
        return all(status == 'clean' for status in self.dirt_status)

    def __hash__(self):
        return hash((tuple(self.dirt_status), self.agent_location))
    
    def __eq__(self, other):
        return (self.dirt_status, self.agent_location) == (other.dirt_status, other.agent_location)

# Defining the Node class
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def expand(self):
        children = []
        action_possible = self.state.actions_possible()
        for action in action_possible:
            new_state = self.state.actions_apply(action)
            new_node = Node(new_state, parent=self, action=action, path_cost=self.path_cost + 1)
            children.append(new_node)
        return children

# PriorityQueue class for Uniform Cost Search
class PriorityQueue:
    def __init__(self):
        self.queue = []
        
    def insert(self, node):
        self.queue.append(node)
        self.queue.sort(key=lambda x: x.path_cost)
    
    def pop(self):
        return self.queue.pop(0)
    
    def is_empty(self):
        return len(self.queue) == 0

# Breadth-First Search
def BFS(initial_state):
    node = Node(initial_state)
    if node.state.IS_GOAL():
        return node
    frontier = [node]  # Using list as a data structure for the queue
    reached = set()
    reached.add(node.state)
    while frontier:
        current_node = frontier.pop(0)
        for child in current_node.expand():
            if child.state not in reached:
                if child.state.IS_GOAL():
                    return child
                frontier.append(child)
                reached.add(child.state)
    return None


def uniform_cost_search(initial_state):
    return Best_First_Search(initial_state, lambda node: node.path_cost)

# Best-First Search implementation 
def Best_First_Search(initial_state, f):
    node = Node(initial_state)
    if node.state.IS_GOAL():
        return node
    
    frontier = PriorityQueue()
    frontier.insert(node)
    reached = {}
    reached[node.state] = node
    
    while not frontier.is_empty():
        current_node = frontier.pop()
        if current_node.state.IS_GOAL():
            return current_node
        for child in current_node.expand():
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.insert(child)
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
    
    dirt_status = []  # Create a list to tell the dirt in each room
    for i in range(rooms):
        status = input(f"Dirty or clean for room {i+1}: ").lower()
        while status not in ["clean", "dirty"]:
            print("Write 'dirty' or 'clean'")
            status = input(f"Dirty or clean for room {i+1}: ").lower()
        dirt_status.append(status)
    
    agent_location = int(input("Enter the location of the vacuum: "))
    while agent_location < 0 or agent_location > rooms - 1:
        agent_location = int(input("Please enter a valid number: "))
    
    print("Let's find the solution with the Breadth-first search algorithm first")
    initial_state = State(dirt_status, agent_location)
    
    node_solution = BFS(initial_state)
    
    if node_solution:
        actions = solution(node_solution)
        print("\nSolution found for the Breadth-first search algorithm!")
        print(f"Initial State: Agent at location {initial_state.agent_location}, Dirt status: {initial_state.dirt_status}")
        print(f"Actions to goal: {actions}")
        print(f"Total actions: {len(actions)}")
    else:
        print("No solution found.")
    
    print("Now, let's find the solution with a uniform-cost search")
    initial_state = State(dirt_status, agent_location)
    
    node_solution = uniform_cost_search(initial_state)
    
    if node_solution:
        actions = solution(node_solution)
        print("\nSolution found for the uniform cost search")
        print(f"Initial State: Agent at location {initial_state.agent_location}, Dirt status: {initial_state.dirt_status}")
        print(f"Actions to goal: {actions}")
        print(f"Total actions: {len(actions)}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
