from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

graph = {}

def bfs(starting_room):
    queue = Queue()
    queue.enqueue([starting_room])
    visited = set()
    while queue.size() > 0:
        current_path = queue.dequeue()
        current_room = current_path[-1]
        visited.add(current_room)
        for direction in graph[current_room]:
            if graph[current_room][direction] == '?':
                return current_path
            if graph[current_room][direction] not in visited:
                new_path = list(current_path)
                new_path.append(graph[current_room][direction])
                queue.enqueue(new_path)

def search_graph():
    directions = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
    count = 0
    while len(graph) != len(room_graph):
        current_room = player.current_room
        room_id = current_room.id
        room_dict = {}
        if room_id not in graph:
            for exit in current_room.get_exits():
                room_dict[exit] = '?'
            if traversal_path:
                previous_room = directions[traversal_path[-1]]
                room_dict[previous_room] = count
            graph[room_id] = room_dict
        else:
            room_dict = graph[room_id]

        possible_exits = list()
        for direction in room_dict:
            if room_dict[direction] == '?':
                possible_exits.append(direction)

        if len(possible_exits) != 0:
            random.shuffle(possible_exits)
            direction = possible_exits[0]
            traversal_path.append(direction)
            player.travel(direction)
            room_move = player.current_room
            graph[current_room.id][direction] = room_move.id
            visited_room_id = current_room.id
        else:
            next_room = bfs(room_id)
            if next_room is not None and len(next_room) > 0:
                for i in range(len(next_room)-1):
                    for direction in graph[next_room[i]]:
                        if graph[next_room[i]][direction] == next_room[i + 1]:
                            traversal_path.append(direction)
                            player.travel(direction)
            else:
                break




search_graph()
print("graph", graph)
print("------------------")
print("Traversal path", traversal_path)
print("------------------")


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
