from Cave2 import *
from pynode.main import *
import random

discoveredRooms = [] # Creates a list to store all the rooms that have been visited
stack = [] # Creates a stack ADT
cave = Cave() # Creates the cave

# Creates a function that will map:
# - All the connection of a existing room to other rooms and add an edge between them.
# - Go into one of the adjacent rooms that has not been visited yet (this room is randomly selected)
def map():
    global cave, stack, discoveredRooms # Imports global variables
    
    adjacentRooms = cave.adjacent_rooms() # Places all the rooms the room we are currently in is adjacent to and places them into the variable adjacentRooms
    
    # The block code check if any of the adjacent rooms already exist. If they do, an edge connecting them is added and a transversal animation is played.
    for room in adjacentRooms:
        # If the value in variable room is present in the list nodes and there is not an edge already present between the rooms, run the block of code below
        if room in discoveredRooms and len(graph.edges_between(graph.node(room), graph.node(cave.current_pos()), directed=False)) == 0:
                edge = graph.add_edge(graph.node(room), graph.node(cave.current_pos()), directed=False) # Add an edge between the rooms
                # The rest of this block of code is purely to animate the model and is not required for the function of the algorithm
                pause(500)
                edge.traverse(initial_node=graph.node(cave.current_pos()), color=Color.BLUE, keep_path=False)
                graph.node(room).highlight(color=Color.BLUE, size=graph.node(room).size()*1.5)
                graph.node(room).set_color(color=Color.BLUE)
                graph.node(cave.current_pos()).set_color(color=Color.DARK_GREY)
                pause(1200)
                edge.traverse(initial_node=graph.node(room), color=Color.BLUE, keep_path=False)
                graph.node(cave.current_pos()).highlight(color=Color.BLUE, size=graph.node(cave.current_pos()).size()*1.5)
                graph.node(cave.current_pos()).set_color(color=Color.BLUE)
                graph.node(room).set_color(color=Color.DARK_GREY)
                pause(500)
        
    undiscoveredRooms = [room for room in adjacentRooms if room not in discoveredRooms] # This make a list of all the room that are adjacent to our current room but have not been visited yet.
    
    # The block of code below defines what happens if there are no new rooms to map from the room we are current at. 
    if len(undiscoveredRooms) == 0 and len(stack) != 1: # If there are not unvisited room adjacent to our current room but the stack still has more than 1 room, run the block of code below
        # The next 3 lines of code are purely to animate the model and are not required for the function of the algorithm
        graph.node(cave.current_pos()).set_color(color=Color.DARK_GREY)
        edge = graph.edges_between(graph.node(stack[-2]), graph.node(cave.current_pos()), directed=False)[0]
        edge.traverse(initial_node=graph.node(cave.current_pos()), color=Color.BLUE, keep_path=False)
        stack.pop() # Removes the top value from the stack
        cave.goto_room(stack[-1]) # This tell the program to go the room that is now ontop of the stack
        # The next 3 lines of code are purely to animate the model and are not required for the function of the algorithm
        graph.node(cave.current_pos()).highlight(color=Color.BLUE, size=graph.node(stack[-1]).size()*1.5) 
        graph.node(cave.current_pos()).set_color(color=Color.BLUE)
        pause(500)
        map() # This call the map function allow for another recursive loop
    # The block of code below defines what happens if there are no new rooms to maps and there are no more rooms we can backtrack to
    elif len(stack) == 1 and len(undiscoveredRooms) == 0: # If there is only one room in the stack and there are no unvisited rooms
        stack.pop() # Empty the stack
        # Note: as the map function is not called again, the recursive loop ends.
    # This block of code below defines what happens if there are still rooms to discover from the room we are current
    else:    
        choosenRoom = random.choice(undiscoveredRooms) # A random room is selected from the list of the all the room that adjacent from our current room and have not been visited yet
        stack.append(choosenRoom) # The choosen room is added to the stack
        graph.node(cave.current_pos()).set_color(color=Color.DARK_GREY) # The not we are leaving is color dark grey
        cave.enter_room(choosenRoom) # The choosen room is entered
        newNode = graph.add_node(id=cave.current_pos(), value=str([cave.current_pos(), cave.current_threat()])) # The new node is created
        edge = graph.add_edge(cave.current_pos(), stack[-2], directed=False) # An edge is added to conencted the room we where and the room we have moved into
        pause(500)
        # The next 3 lines of code are purely to animate the model and are not required for the function of the algorithm
        edge.traverse(initial_node=graph.node(stack[-2]), color=Color.BLUE, keep_path=False)
        newNode.highlight(color=Color.BLUE, size=newNode.size()*1.5)
        newNode.set_color(color=Color.BLUE)
        discoveredRooms.append(cave.current_pos()) # The new room we have discovered is added to the list of discovered rooms
        map() # This call the map function allow for another recursive loop

# Defines the main code        
def run():
    global cave, stack, discoveredRooms # All the globals are imported
    cave.populate_cave() # The cave is populated with the threats
    graph.add_node(id=cave.current_pos(), value=str([cave.current_pos(), cave.current_threat()])) # The starting room is created
    discoveredRooms.append(cave.current_pos()) # The starting room is added to the list of discovered rooms
    stack.append(cave.current_pos()) # The starting room is added to the stack
    map() # The map function is called starting the recursive loop
    # The three lines of code below color the room with threats red. This is not required for the algorithm to function and is only for easier readablity
    for i in graph.nodes():
        if eval(i.value())[1] != 'empty':
            i.set_color(color=Color.RED)

# Runs the main code with pynode    
begin_pynode(run)
