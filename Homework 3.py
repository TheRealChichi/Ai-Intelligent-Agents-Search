# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 12:17:23 2024

@author: kevin
"""
import heapq

map = {
       "Arad": [("Zerind", 75), ("Timisoara", 118), ("Sibiu", 140)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Sibiu": [("Arad", 140), ("Fagaras", 99), ("Rimnicu Vilcea", 80), ("Oradea", 151)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
    "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90)],
    "Giurgiu": [("Bucharest", 90)]
}

heuristic = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Dobreta": 242,
    "Eforie": 161,
    "Fagaras": 178,
    "Giurgiu": 77,
    "Hirosa": 151,
    "Lasi": 226,
    "Luogj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 98,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374,
    }

def get_neighbors(city):
    return map.get(city,[])

def A_search(start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic[start], start))
    
    g_cost = {start: 0}
    
    came_from = {}
    
    while open_list:
        current_f, current_city = heapq.heappop(open_list)
        
        if current_city == goal:
            print(f"Reached goal: {current_city} with total cost: {current_f}")
            return reconstruct_path(came_from, start, goal)
        
        for neighbor, distance in get_neighbors(current_city):
            new_g_cost = g_cost[current_city] + distance
            
            if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_g_cost #Set the new g_cost value for neighbor
                f_value = new_g_cost + heuristic[neighbor] #Caculate f_value function
                heapq.heappush(open_list,(f_value,neighbor)) #Insert f_value with the city in the prority queue
                came_from[neighbor] = current_city 
        
    print("Goal not reachable")
    return None

def reconstruct_path(came_from,start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
    path.append(start)
    path.reverse()
    print("Path:", "->".join(path))
    return path

A_search("Arad", "Bucharest")
    
    
        
            

