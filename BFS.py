import queue

def createMaze():
    maze = []
    maze.append(["#","#", "#", "#", "#", "O", "#", "#", "#"])
    maze.append(["#"," ", " ", " ", "#", " ", " ", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", " ", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", "X", "#", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", " ", " ", " ", " ", "#"])
    maze.append(["#","#", "#", "#", "#", "#", "#", "#", "#"])
    return maze

    
# def checkPath (path, row, col, maze, validation, position = None):
#     for _ in path:
#         if _ == "L":
#             col -= 2
#         elif _ == "R":
#             col += 1
#         elif _ == "U":
#             row -= 1
#         else:
#             row += 1
#         if position is not None:
#             position.add(row, col)
        
#         if validation == True:
#             if not (0 <= col <= len(maze[0]) and (0 <= row <= len(maze))):
#                 return False
#             elif maze[row][col] == '#':
#                 return False
#             return True
        

def startPosition (maze):
    # start = 0
    for index, value in enumerate(maze[0]):
        if value == "O":
            # start = index
            return index
            
    
def printMaze (maze, path = ''):
    start = startPosition(maze)
    
    col = start
    row = 0
    position = set()
    
    for _ in path:
        if _ == "L":
            col -= 1
        elif _ == "R":
            col += 1
        elif _ == "U":
            row -= 1
        elif _ == "D":
            row += 1
        position.add((row, col))
    
    for row, value_row in enumerate(maze):
        for col, value_col in enumerate(value_row):
            if (row, col) in position:
                print(">  ", end = '')
            else:
                print(value_col, " ", end = '')
        print()
        

def validateMaze(maze, path):
    start = startPosition(maze)
    
    col = start
    row = 0
    
    for _ in path:
        if _ == "L":
            col -= 1
        elif _ == "R":
            col += 1
        elif _ == "U":
            row -= 1
        elif _ == "D":
            row += 1
            
        if not (0 <= col < len(maze[0]) and (0 <= row < len(maze))):
            return False
        elif maze[row][col] == '#':
            return False
    return True
    
    
def reachedEnd (maze, path):
    start = startPosition(maze)
    # print(start)
    
    col = start
    row = 0
    
    for _ in path:
        if _ == "L":
            col -= 1
        elif _ == "R":
            col += 1
        elif _ == "U":
            row -= 1
        elif _ == "D":
            row += 1
    
    if maze[row][col] == 'X':
        print('Path Taken: ', path)
        printMaze(maze, path)
        return True
        
    return False

    
# Algorithm 
path = queue.Queue()
path.put('')
final_path = ''
maze = createMaze()

while not reachedEnd(maze, final_path):
    final_path = path.get()
    for direction in 'L R U D'.split():
    	intermidiate_path = final_path + direction
    	if validateMaze(maze, intermidiate_path):
    		path.put(intermidiate_path)