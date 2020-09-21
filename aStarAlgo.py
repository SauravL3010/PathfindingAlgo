import pygame as py
import math
from queue import PriorityQueue

# Pygame Display
WIDTH = 800
WIN = py.display.set_mode([WIDTH, WIDTH])
py.display.set_caption("A* ALGORITHM PATH FINDING")

# All bunch of colors
RED = (212, 76, 76)
GREEN = (129, 204, 135) 
BLUE = (0, 0, 255) # START
YELLOW = (255, 255, 0) # END
WHITE = (255, 255, 255) # DEFAULT
BLACK = (78, 85, 87) # BARRIER
PURPLE = (167, 107, 232) # PATH
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

'''    WORKING OF THE ALGORITHM: 
# class node
# <---- getPosition, boolean (closed, open, barrier cube), reset(to white), make(Closed, Open, Barrier, Path)
# Draw a particular node (a rectangle), update the neighbours(left, right, up, down) ----> All nodes attributes and methods
# heuristic method, make a two dimensional grid --> containing all nodes(return the grid), makeGridLines
# new draw method (to draw each node on the screen as well as GridLines),
# get position clicked (returns the rows and cols not in px)
# Algorithm 
# follow the path (make purple cubes)
# Main Function
'''

# <---------------- Node class ----------------->
class Node:   
    '''
    # (row, cols) are not in px. 
    # dimension ---> width of a single node
    # color --> present color of the node
    # x, y --> in px
    # neighbours --> list of neighbouring nodes (which are valid)
    '''
    def __init__(self, row, cols, dimension, totalRows):
        self.row = row 
        self.cols = cols
        self.dimension = dimension 
        self.totalRows = totalRows 
        self.x = row * dimension # --> in px 
        self.y = cols * dimension # --> in px
        self.color = WHITE #--> initially all nodes are white
        self.neighbours = None

    def getPosition(self): # get the row and cols
        return self.row, self.cols

    # Boolean for type of nodes
    def isDone(self):
        '''
        # the red color --> path is already identified (or node is visited)
        '''
        return self.color == RED

    def isPath(self):
        return self.color == PURPLE

    def isBarrier(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == BLUE

    def isEnd(self):
        return self.color == YELLOW

    # Change the color of the nodes
    def makePath(self):
        self.color = PURPLE

    def makeBarrier(self):
        self.color = BLACK
    
    def makeStart(self):
        self.color = BLUE
    
    def makeEnd(self):
        self.color = YELLOW

    def makeValid(self):
        self.color = GREEN

    def makeDone(self):
        self.color = RED

    # Reset the color of the nodes
    def resetColor(self):
        self.color = WHITE

    def drawNode(self, win):
        '''
        Draws that particular node
        '''
        py.draw.ellipse(win, self.color, (self.x, self.y, self.dimension, self.dimension))
    
    def updateNeighbours(self, grid):
        '''
        grid --> grid containing all nodes
        appends every neighbouring nodes which are valid 
        '''
        self.neighbours = []

        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.cols].isBarrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.cols])

        if self.row > 0 and not grid[self.row - 1][self.cols].isBarrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.cols])

        if self.cols < self.totalRows - 1 and not grid[self.row][self.cols + 1].isBarrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.cols + 1])

        if self.cols > 0 and not grid[self.row][self.cols - 1].isBarrier(): # LEFT
            self.neighbours.append(grid[self.row][self.cols - 1])

        # <----------- Diagonal Neighbours --------->
        # if self.cols > 1 and self.row > 1 and not grid[self.row - 1][self.cols - 1].isBarrier():
        #     self.neighbours.append(grid[self.row - 1][self.cols - 1])   

        # if self.cols < self.totalRows - 1 and self.row > 1 and not grid[self.row - 1][self.cols + 1].isBarrier():
        #     self.neighbours.append(grid[self.row - 1][self.cols + 1])        
            
        # if self.cols < self.totalRows - 1 and self.row < self.totalRows - 1 and not grid[self.row + 1][self.cols + 1].isBarrier():
        #     self.neighbours.append(grid[self.row + 1][self.cols + 1])        

        # if self.cols > 1 and self.row > self.totalRows - 1 and not grid[self.row + 1][self.cols - 1].isBarrier():
        #     self.neighbours.append(grid[self.row + 1][self.cols - 1])        
    
# <-------------- End of Node class -------------------> 


def heu(coor1, coor2):
    '''
    heuristic approach to find the shortest distance from source to end
    Manhattan distance is used
    '''
    x1, y1 = coor1
    x2, y2 = coor2
    # return abs(x1-x2) + abs(y1-y2)
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def makeGrid(rows, width):
    '''
    2D list that will contain all the nodes
    rows --> is rows in no's
    width --> in px
    '''
    grid = []
    dim = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, dim, rows)
            grid[i].append(node)
    
    return grid

def gridLines(win, rows, width):
    '''
    win--> WIN
    rows--> no's of rows
    width--> in px
    '''
    dim = width // rows
    for i in range(rows):
        py.draw.line(win, GREY, (0, i*dim), (width,i*dim))
    for j in range(rows):
        py.draw.line(win, GREY, (j*dim,0), (j*dim,width))
    
def draw(win, rows, width, grid):
    '''
    win --> WIN
    rows --> no's
    width --> in px
    grid --> containing all nodes

    make the background WHITE
    draw every single node on screen
    call the gridLines function 
    Update the display
    '''
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.drawNode(win)

    gridLines(win, rows, width)
    py.display.update()


def getPositionClicked(pos, rows, width):
    '''
    pos --> (y, x) [pygame will return y and x in px]
    rows --> in no's
    width --> in px

    return row, col in no's 
    '''
    dim = width // rows
    y, x = pos
    row = y // dim
    col = x // dim

    return row, col

def definePath(draw, refNodePath, curNode):
    '''
    refNodePath --> dict of node and previous references
    curNode --> currentNode
    draw --> draw it on screen
    '''
    while curNode in refNodePath:
        curNode = refNodePath[curNode]
        curNode.makePath()
        draw()

def algorithm(draw, grid, start, end):
    '''
    grid --> contains all nodes
    start --> the start node
    end ---> the end node
    draw --> calls the draw() function to draw every single node and gridLines on WIN

    <---- WORKING ---->
    a priority queue, reference to previous node (started from), initialized dict() {to find nodes} (set) , gScore, fScore
    priority queue -- > (priority, *args)
    while there are nodes in queue:
        remove the min element from queue and {}
        for every neighbour set a temporary gScore of gScore(currentNode + 1)
        if temp gScore < than previous gScore (could be infinity or assigned gScore):
            set the neighbours reference to currentNode
            update it's gScore and fScore
            if neighbour not already in set: (deosn't matter since it's a set, won't duplicate stuff)
                add the neighbour to priority queue and {}
            if this node is the end:
                definePath
    '''
    pQueue = PriorityQueue()
    count = 0

    pQueue.put((0, count, start))
    initQueue = {start}
    refNodePath = {}

    gScore = {node: float("inf") for row in grid for node in row}
    fScore = {node: float("inf") for row in grid for node in row}

    gScore[start] = 0
    fScore[start] = heu(start.getPosition(), end.getPosition())

    while not pQueue.empty():
        '''
        pQueue becomes empty after all the nodes are exausted or visited 
        '''
        for event in py.event.get():
            if event.type == py.QUIT:
                return False

        currentNode = pQueue.get()[2]
        initQueue.remove(currentNode)

        if currentNode == end:
            start.makeStart()
            end.makeEnd()
            definePath(draw, refNodePath, currentNode)
            # for row in range(len(grid)):
            #     for col in range(len(grid)):
            #         if not grid[row][col] in refNodePath and grid[row][col] != start and grid[row][col] != end:
            #             grid[row][col].resetColor()

            return True

        for neighbour in currentNode.neighbours:
            tempGScore = gScore[currentNode] + 1

            if tempGScore < gScore[neighbour]:
                refNodePath[neighbour] = currentNode
                gScore[neighbour] = tempGScore
                fScore[neighbour] = tempGScore + heu(neighbour.getPosition(), end.getPosition())

                if neighbour not in initQueue:
                    count+=1
                    pQueue.put((fScore[neighbour], count, neighbour))
                    initQueue.add(neighbour)
                    neighbour.makeValid()

        if currentNode != end:
            currentNode.makeDone()

        draw()
    return False


#     # <---- Alternative start ----->

# def algorithm(draw, grid, start, end):
# 	count = 0
# 	open_set = PriorityQueue()
# 	open_set.put((0, count, start))
# 	came_from = {}
# 	g_score = {spot: float("inf") for row in grid for spot in row}
# 	g_score[start] = 0
# 	f_score = {spot: float("inf") for row in grid for spot in row}
# 	f_score[start] = heu(start.getPosition(), end.getPosition())

# 	open_set_hash = {start}

# 	while not open_set.empty():
# 		for event in py.event.get():
# 			if event.type == py.QUIT:
# 				py.quit()

# 		current = open_set.get()[2]
# 		open_set_hash.remove(current)

# 		if current == end:
# 			definePath(draw, came_from, end)
# 			end.makeEnd()
# 			return True

# 		for neighbor in current.neighbours:
# 			temp_g_score = g_score[current] + 1

# 			if temp_g_score < g_score[neighbor]:
# 				came_from[neighbor] = current
# 				g_score[neighbor] = temp_g_score
# 				f_score[neighbor] = temp_g_score + heu(neighbor.getPosition(), end.getPosition())
# 				if neighbor not in open_set_hash:
# 					count += 1
# 					open_set.put((f_score[neighbor], count, neighbor))
# 					open_set_hash.add(neighbor)
# 					neighbor.makeValid()

# 		draw()

# 		if current != start:
# 			current.makeDone()

# 	return False

    # <---- Alternative end --> 
    
def main(win, width):
    '''
    win --> WIN
    width --> in px
    call grid function
    while loop(ends at py.quit() or key == QUIT)
        left clicks
        right clicks
        spaceBar 
        and clear
    '''
    ROWS = 40
    grid = makeGrid(ROWS, width)

    start = None
    end = None
    running = True
    while running:
        draw(WIN, ROWS, width, grid)

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            
            #left clicks
            if py.mouse.get_pressed()[0]:
                # start and end
                # barriers
                currentPosition = py.mouse.get_pos()
                row, col = getPositionClicked(currentPosition, ROWS, width)
                currentNode = grid[row][col]

                if not start and currentNode != end:
                    start = currentNode
                    start.makeStart()

                elif not end and currentNode != start:
                    end = currentNode
                    end.makeEnd()

                elif currentNode != start and currentNode != end: 
                    currentNode.makeBarrier()

            #right clicks
            elif py.mouse.get_pressed()[2]:
                currentPosition = py.mouse.get_pos()
                row, col = getPositionClicked(currentPosition, ROWS, width)
                currentNode = grid[row][col]

                currentNode.resetColor()

                if currentNode == start:
                    start = None
                if currentNode == end:
                    end = None

    
            #spaceBar --> Algorithm
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbours(grid)

                    #algorithm
                    algorithm(lambda: draw(WIN, ROWS, width, grid), grid, start, end)

            
                if event.key == py.K_c:
                    start = None
                    end = None
                    grid = makeGrid(ROWS, width)

    py.quit()

main(WIN, WIDTH)
