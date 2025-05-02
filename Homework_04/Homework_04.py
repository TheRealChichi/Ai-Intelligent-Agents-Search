# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 11:52:18 2024

@author: kevin
"""
import random

class State:
    def __init__(self, location, room_a_status, room_b_status):
        self.location = location
        self.room_a_status = room_a_status
        self.room_b_status = room_b_status
        
    def goal_check(self):
        return self.room_a_status == 'clean' and self.room_b_status == 'clean'
    
    # Create comparisons methods
    def __eq__(self, other):
        return (self.location == other.location
                and
                self.room_a_status == other.room_a_status
                and
                self.room_b_status == other.room_b_status)
    
    #It is used to check if the element is already in the set or not
    def __hash__(self):
        return hash((self.location, self.room_a_status, self.room_b_status))
    
class VacuumCleanerAgent:
    def __init__(self, initial_state=None):
        if initial_state is None:
            self.initial_state = State('A', 'dirty', 'dirty')
        else:
            self.initial_state = initial_state
            
    def goal_test(self, state):
        return state.goal_check()
    
    def RESULTS(self, state):
        successors = []
        
        location = state.location
        room_a = state.room_a_status
        room_b = state.room_b_status
        
        
        if location == 'A':
            if room_a == 'dirty':
                # When the vaccuum sucks the floort it can clean the next room
                # Import the random.choice method to simulate 
                # the non deterministic agent's actions.
                if random.choice([True, False]):
                    successors.append((State('A', 'clean', room_b), 'Suck'))
                else:
                    successors.append((State('A', 'clean', 'clean'), 'Suck'))
            else:
                # When moving it can still put some dirt on the floor
                if random.choice([True, False]):
                    successors.append((State('B', 'dirty', room_b), 'Right'))
                else:
                    successors.append((State('B', room_a, room_b), 'Right'))
            
        if location == 'B':
            if room_b == 'dirty':
                if random.choice([True, False]):
                    successors.append((State('B', room_a, 'clean'), 'Suck'))
                else:
                    successors.append((State('B', 'clean', 'clean'), 'Suck'))
            else:
                if random.choice([True, False]):
                    successors.append((State('A', 'dirty', room_b), 'Left'))
                else:
                    successors.append((State('B', room_a, room_b), 'Left'))

        return successors
    
    def and_or_search(self, state):
        return self.or_search(state, set())
    
    # Use a recursive approach by calling recursively the and_search
    # and_search is calling or_search using almost a recursive appraoch
    def or_search(self, state, path):
        if state.goal_check():
            return []
        if state in path:
            return 'failure'
            
        path.add(state)
        
        for successor, action in self.RESULTS(state):
            plan = self.and_search([successor], path)
            if plan != 'failure':
                return [action] + plan
        
        path.remove(state)
        return 'failure'

    def and_search(self, states, path):
        plans = []
        for state in states:
            plan = self.or_search(state, path)
            if plan == 'failure':
                return 'failure'
            plans.extend(plan) 
            # Method to add eleement to a list from another iterable
            # Here it adds element of a list to another list
        return plans
        
agent = VacuumCleanerAgent()
initial_state = State('A', 'dirty', 'dirty')
solution = agent.or_search(initial_state, set())

if solution != 'failure':
    print(solution)
else:
    print("No solution found.")
