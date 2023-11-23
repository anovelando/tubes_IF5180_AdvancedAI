class Player(object):
    # Kelas Player ini boleh ditambahkan atribut/ method lain, tapi jangan menghapus/ mengubah kode yang sudah ada
    # You can add other attributes and/or methods to this Player class, but don't delete or change the existing code.
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.num_movement = 0
        self.percept = {
            "stench" : False,
            "breeze": False,
        }

        # Added Attributes
        self.visited = {}
        self.wall = []
        self.safe = []
        self.threat = []
        self.pit = []
        self.wumpus = []
        self.path = []

        self.prev_x = None
        self.prev_y = None
        self.safe.append((self.x, self.y))
        self.last_move = None

    def move(self, board, direction):
        board.update_board(self.x, self.y, board.board_static[self.x][self.y])

        if direction=="W" and self.x > 0:
            self.x = self.x-1
        elif direction=="A" and self.y > 0:
            self.y = self.y - 1
        elif direction=="S" and self.x < board.size-1:
            self.x = self.x + 1
        elif direction=="D" and self.y < board.size-1:
            self.y = self.y+1


        board.update_board(self.x, self.y, "P")
        self.percept["stench"] = board.board_static[self.x][self.y] == "~" or board.board_static[self.x][self.y] == "≌"
        self.percept["breeze"] = board.board_static[self.x][self.y] == "=" or board.board_static[self.x][self.y] == "≌"

    def is_finished(self, listWumpus, listPit, gold):
        for wumpus in listWumpus:
            if self.x == wumpus.x and self.y == wumpus.y:
                print("======================\nYou are eaten by Wumpus. You lose 😭")
                return True
        for pit in listPit:
            if self.x == pit.x and self.y == pit.y:
                print("======================\nYou fall into the pit. You lose 😭")
                return True
        if self.x == gold.x and self.y == gold.y:
            print("======================\nCongratulations, you win 😄")
            return True
        return False
    
    # Added methods

    def update_knowledge(self):
        cur_pos = (self.x, self.y)
        prev_pos = (self.prev_x, self.prev_y)

        # Delete current position from unvisited list
        if cur_pos in self.safe:
            self.safe.remove(cur_pos)
        if cur_pos in self.threat:
            self.threat.remove(cur_pos)

        # Hit the wall
        if cur_pos == prev_pos:
            if self.last_move not in self.wall:
                self.wall.append(self.last_move)
            if self.last_move in self.safe:
                self.safe.remove(self.last_move)
            if self.last_move in self.threat:
                self.threat.remove(self.last_move)

        # Percept
        self.visited[cur_pos] = self.percept

        # Update adjacent rooms
        adjs = self.get_adjacent(cur_pos)
        if not self.percept['stench'] and not self.percept['breeze']:
            for p in adjs:
                if p not in self.safe:
                    self.safe.append(p)    
        else:
            for p in adjs:
                self.safe_threat(p)

        # Find threats
        self.find_threat()

    def get_adjacent(self, position):
        x, y = position
        adj = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        adj = list(filter(lambda p: p not in self.visited and p not in self.wall and p not in self.wumpus and p not in self.pit, adj))
        return adj
    
    def safe_threat(self, position):
        x, y = position
        adj = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        adj = list(filter(lambda p: p in self.visited, adj))
        
        for i in range(len(adj)):
            i_percept = (self.visited[adj[i]]['stench'], self.visited[adj[i]]['breeze'])
            if i_percept == (True, True):
                continue
            for j in range(i+1,len(adj)):
                j_percept = (self.visited[adj[j]]['stench'], self.visited[adj[j]]['breeze'])
                if j_percept == (True, True):
                    continue
                if i_percept != j_percept:
                    if position not in self.safe:
                        self.safe.append(position)
                    if position in self.threat:
                        self.threat.remove(position)
                    return
                
        if position not in self.threat:
            self.threat.append(position)
    
    def find_threat(self):
        x, y = self.x, self.y
        percept = (self.visited[(x, y)]['stench'], self.visited[(x, y)]['breeze'])
        if percept == (False, False):
            return
        adj = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        potential_threat = list(filter(lambda p: p not in self.visited and p not in self.safe and p not in self.wall, adj))
        wumpus = list(filter(lambda p: p in self.wumpus, adj))
        pit = list(filter(lambda p: p in self.pit, adj))
        if len(potential_threat) == 1:
            if percept[0] and len(wumpus) == 0:
                self.wumpus.append(potential_threat[0])
                self.threat.remove(potential_threat[0])
                return
            if percept[1] and len(pit) == 0:
                self.pit.append(potential_threat[0])
                self.threat.remove(potential_threat[0])
                return
        
        if len(potential_threat) == 2 and percept == (True, True) and (len(wumpus) == 0 or len(pit) == 0):
            self.wumpus += potential_threat
            self.pit += potential_threat
            for p in potential_threat:
                if p in self.threat:
                    self.threat.remove(p)

            
    def forward(self):
        cur_pos = (self.x, self.y)
        if len(self.path) == 0:
            if len(self.safe):
                goal_position = self.safe[-1]
                self.path = self.goto(goal_position)
            elif len(self.threat):
                goal_position = self.threat[-1]
                self.path = self.goto(goal_position)
            else:
                import sys
                sys.exit("No solution")

        next_pos = self.path.pop(0)
        self.prev_x, self.prev_y = cur_pos
        self.last_move = next_pos

        return self.forward_command(cur_pos, next_pos)


    # Map point to command based on move function
    def forward_command(self, cur_pos, next_pos):
        x, y = cur_pos
        dx, dy = next_pos
        move = (dx-x, dy-y)
        if move == (0, 1):
            return 'D'
        if move == (0, -1):
            return 'A'
        if move == (1, 0):
            return 'S'
        if move == (-1, 0):
            return 'W'
            
    def goto(self, end):
        start = (self.x, self.y)
        visited = set()
        queue = [(start, [])]  # Queue stores tuples of (node, path)
        visited.add(start)
        while queue:
            node, path = queue.pop(0)
            
            if node == end:
                return path
            
            if node not in self.visited:
                continue
            
            x, y = node
            adj = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

            for a in adj:
                if a not in visited:
                    visited.add(a)
                    queue.append((a, path + [a]))
        
        return []  # If no path is found
                