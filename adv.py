from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


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
traversal_graph = {}

# PLAN TO SOLVE
# Already in starting room
# Add all the exits for the current room
# While "?" in current_room.get_exits():
#   prev_room_id = current_room.id
#   Move random direction
#   traversal_path.append(direction)
#   fill_unknown_exits 
#   traversal_graph[prev_room][direction] = current_room.id

# perform a BFS for nearest exit with a "?"
# extend traversal path with path used to get to "?"

def get_opposite_direction(d):
    if d == "n":
        return "s"
    if d == "s":
        return "n"
    if d == "e":
        return "w"
    if d == "w":
        return "e"

def bfs(start, end="?"):
    visited = {}
    path = []
    
    q = Queue()
    q.enqueue((start, path))

    while q.size() > 0:
        next_room, path = q.dequeue()
        
        if next_room not in visited:
            visited[next_room] = path
            if end in traversal_graph[next_room].values():
                return path
            for direction, room in traversal_graph[next_room].items():
                path_copy = list(path)
                path_copy.append(direction)
                q.enqueue((room, path_copy))

 
def get_next_direction(room_id, last_direction):
    if last_direction is None:
        exits = player.current_room.get_exits()
        next_direction = exits[random.randrange(0, len(exits))]
        return next_direction
    for k, v in traversal_graph[room_id].items():
        if v == "?" and v != get_opposite_direction(last_direction):
            next_direction = k
    
    return next_direction


def populate_new_room():
    traversal_graph[player.current_room.id] = {}
    exits = player.current_room.get_exits()
    for d in exits:
        traversal_graph[player.current_room.id][d] = "?"


populate_new_room()
exits = player.current_room.get_exits()

last_direction = None

while True:
    next_direction = get_next_direction(player.current_room.id, last_direction)
    opposite_d = get_opposite_direction(next_direction)

    prev_room = player.current_room.id

    player.travel(next_direction)
    last_direction = next_direction
    traversal_path.append(last_direction)

    if player.current_room.id not in traversal_graph:
        populate_new_room()
    traversal_graph[player.current_room.id][opposite_d] = prev_room
    traversal_graph[prev_room][next_direction] = player.current_room.id

    if "?" not in traversal_graph[player.current_room.id].values():
        next_path = bfs(player.current_room.id)
        if not next_path:
            break
        for direction in next_path:
            player.travel(direction)
            last_direction = direction
            traversal_path.append(last_direction)
        if player.current_room.id not in traversal_graph:
            populate_new_room()


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
