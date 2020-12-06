from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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
# 11/23/2020

traversal_path = []
visited = set()

def random_walk():
    # possible paths
    paths = player.current_room.get_exits()

    # ensure not to revisit same room
    new_paths = []
    for path in paths:
        if player.current_room.get_room_in_direction(path) not in visited:
            new_paths.append(path)
    
    # find paths
    if len(new_paths) > 0:
        path = random.choice(new_paths)
        return path

    # no paths case
    if len(new_paths) == 0:
        return False


# bft search
def bft_search():
    global visited
    visted_paths = {}
    starting_room = player.current_room

    # empty queue created along with starting room
    path_queue = []
    path_queue.append([starting_room])

    # non-empty queue loop
    while len(path_queue) > 0:
        # current path
        cur_path = path_queue[0]

        # remove it from queue
        path_queue.pop(0)
        
        # set current room to last room in the path
        cur_room = cur_path[-1]

        # add this to path to visted_paths so dont keep visiting
        visited_paths[cur_room] = cur_path

        # visited room check
        if cur_room not in visited:
            cur_path.pop(0)
            backtrack_path = []

            # directions to find first room
            for i in range(0, len(cur_path)):
                if starting_room.get_room_in_direction('n') == cur_room[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('n')
                
                elif starting_room.get_room_in_direction('e') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('e')

                elif starting_room.get_room_in_direction('s') == cur_paht[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('s')
                
                elif starting_room.get_room_in_direction('w') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('w')
            
            return backtrack_path

            # add path to neighbors into queue if visited
            if cur_room in visited:
                for direction in cur_room.get_exits():
                    new_path = list(cur_path)
                    new_path.append(cur_room.get_room_in_direction(direction))

                    if new_path[-1] not in visted_paths:
                        path_queue.append(new_path)

def adv():
    # add cur room to visited
    visited.add(player.current_room)

    playing = True
    dft = True
    bft = True

    # main game
    while playing:

        # bft traversal
        while dft:
            bft = True
            direction = random_walk()

            if direction == False:
                dft = False

            else:
                traversal_path.append(direction)
                player.travel(direction)
                visited.add(player.current_room)

        while bft:
            backtrack_path = bft_search()

            if backtrack_path == None:
                bft = False
                playing = False

            else:
                # return to location
                for direction in backtrack_path:
                    player.travel(direction)
                    visited.add(player.current_room)
                    traversal_path.append(direction)

                # start depth first traversal again
                bft = False
                dft = True



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
