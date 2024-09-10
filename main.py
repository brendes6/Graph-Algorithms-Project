# graphProject - Graph Algorithm Visualiser
# Author: Brendan Desjardins
# Made: July - November 2023

# import necessary modules
import pygame
import random
import math

#initialize pygame, window, font, and colors for convenience
pygame.init()
WHITE = (255, 255, 255)
GREEN = (30, 255, 30)
BLACK = (0, 0, 0)
RED = (255, 30, 30)
BLUE = (30, 30, 255)
WIN = pygame.display.set_mode((1100, 700))
WIN.fill(WHITE)
font = pygame.font.SysFont('Arial', 20)


class CustomGraph:

    # CustomGraph Class
    # Graph class that stores and manages all aspects of the graph as well as methods

    def __init__(self):
        # Neighbors maps a node number to a list of its neighbors
        self.neighbors = {}
        # Circles maps a node number to its Circle object
        self.circles = {}
        self.count = 0
        self.result = ''
        self.state = 'place'
        self.textBox = ''
        self.marked_circle = None
        self.target = None

    def get_neighbors(self, node):
        return self.neighbors[node]

    def add_neighbor(self, node, neighbor):
        # Given two nodes, adds both nodes as eachothers neighbors if not already set

        if neighbor not in self.neighbors[node]:
            self.neighbors[node] += [neighbor]
            self.neighbors[neighbor] += [node]

    def get_circle(self, node):
        return self.circles[node].get_rect()

    def get_circle_color(self, node):
        return self.circles[node].get_color()

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def add_circle(self, x, y):
        node = self.count + 1
        self.circles[node] = Circle(node, pygame.Rect(x-22.5, y-22.5, 45, 45), GREEN)
        self.neighbors[node] = []
        self.count += 1

    def mark(self, node, color):
        self.circles[node].set_color(color)

    def reset(self):
        # reset method resets all circle marks and neighbors that are set

        for circle in self.circles.values():
            circle.set_color(GREEN)
        for k in range(1, len(self.neighbors)+1):
            self.neighbors[k] = []
        self.result = ''
        self.target = None

    def restart(self):
        # restart method removes all circles from the graph
        
        self.circles.clear()
        self.neighbors.clear()
        self.count = 0
        self.result = ''
        self.target = None

    def get_count(self):
        return self.count

    def get_result(self):
        return self.result

    def change_result(self, s):
        self.result = s

    def set_marked_circle(self, node):
        self.marked_circle = node

    def get_marked_circle(self):
        temp = self.marked_circle
        self.marked_circle = None
        return temp

    def set_target(self, target):
        self.target = target

    def get_target(self):
        return self.target

    def reset_colors(self):
        for circle in self.circles.values():
            circle.set_color(GREEN)

class Circle:

    # Circle Class
    # Class contains a circles number, its pygame rect object, and its color
    # Class methods are getters and setters for these attributes

    def __init__(self, num, rect, color):
        self.num = num
        self.rect = rect
        self.color = color

    def get_num(self):
        return self.num

    def get_rect(self):
        return self.rect

    def get_color(self):
        return self.color

    def set_color(self, new):
        self.color = new


# Create graph object
currentGraph = CustomGraph()


def visit(node, target=None):
    # visit() function
    # When a node is visited, mark it red. If it is the target, update the graph result.

    index, dist = node
    print('Visited node ' + str(index))
    currentGraph.mark(index, RED)
    pygame.time.wait(150)
    pygame.draw.ellipse(WIN, currentGraph.get_circle_color(index), currentGraph.get_circle(index))
    if index == target:
        currentGraph.change_result('Shortest path to node ' + str(index) + ' is distance ' + str(dist))
        return True
    pygame.display.update()


def BFS_ShortestPath(origin, target):
    # BFS_SortestPath() Algorithm
    # Breadth-First-Search algorithm capable of finding the shortest path to a target node

    # Reset graph appearance when function called
    currentGraph.reset_colors()
    pygame.display.update()

    # If empty graph, return
    if currentGraph.get_count() == 0:
        return

    # Initialize visited array as well as "previous" array to store the node previously used to reach a certain node
    visited = [False] * currentGraph.get_count()
    previous = [None] * currentGraph.get_count()

    # ans array will store the nodes used to reach target node once we backtrack
    ans = []

    stack = [origin]
    while stack:

        # Popping from index 0 is what allows this algorithm to perform BFS rather than DFS
        index, dist = stack.pop(0)

        # If node visited is the target, run backtracking algorithm to display shortest path
        if visit((index, dist), target):
            while True:

                # target node is part of the shortest path
                ans.append(index)

                # Check if node has a previous node stored. If not, break from while loop.
                if not previous[index-1]:
                    print(ans)
                    break

                # If node has a previous node stored, change current node index to the previous
                else:
                    index = previous[index-1]

            # For node stored in ans, mark with blue to show it is part of shortest path
            for node in ans:
                currentGraph.mark(node, BLUE)
            break

        # Mark current node as visited
        visited[index - 1] = True

        # Get node neighbors, check if they have been visited. If not, append them to stack.
        neighbors = currentGraph.get_neighbors(index)
        for n in neighbors:
            if not visited[n-1]:
                stack.append((n, dist+1))

                # Mark neigbor's previous node as current node
                if not previous[n-1]:
                    previous[n-1] = index

    if not currentGraph.get_result():
        currentGraph.change_result('Search Complete.')

def DFS(origin, target):
    # DFS() function
    # Depth-First-Search function implemented on the customGraph
    # Searches for a specified target node from origin node

    # Reset graph appearance at start of algorithm run
    currentGraph.reset_colors()
    pygame.display.update()

    # Initialize node found to be false until proven otherwise
    found = False

    # If graph empty, return
    if currentGraph.get_count() == 0:
        return

    # Initialize visited array of size count to keep track of which nodes have been visited
    visited = [False] * currentGraph.get_count()

    # Initialize stack implementation of DFS. Stack starts with just the origin in it.
    stack = [origin]

    # While stack = while nodes need to be explored
    while stack:

        # Pop from top of stack
        index, dist = stack.pop()

        # Visit function performs operations and returns if a node is the target. If returned true, found is true.
        if visit((index, dist), target):
            found = True

        # Mark node as visited
        visited[index - 1] = True

        # For neighbors of current index, if not visited, append to the stack.
        neigbors = currentGraph.get_neighbors(index)
        for n in neigbors:
            if not visited[n-1]:
                stack.append((n, dist+1))

    # Print result whether target node was found or not
    if found:
        currentGraph.change_result(f'Depth-First Search Complete. Target node {target} reachable from origin.')
    else:
        currentGraph.change_result('Depth-First Search Complete.')


def generate_random_neighbors():
    # generate_random_neighbors() function
    # Assigns each circle a random neighbor from the existing circles in the graph

    count = currentGraph.get_count()
    for num in range(1, count+1):
        t = random.randrange(1, count+1)
        while t == num:
            t = random.randrange(1, count+1)
        currentGraph.add_neighbor(num, t)


def update_lines():
    # update_lines() function
    # Checks for any neighbors of circles in the graph
    # Draws a line from circle.centerx to neighbor.centerx

    for i in range(1, currentGraph.count+1):
        x, y = currentGraph.get_circle(i).centerx, currentGraph.get_circle(i).centery
        for j in currentGraph.get_neighbors(i):
            a, b = currentGraph.get_circle(j).centerx, currentGraph.get_circle(j).centery
            pygame.draw.line(WIN, BLACK, (x, y), (a, b), 4)


# Initializing all buttons as pygame Rect objects
button = pygame.Rect(900, 600, 150, 40)
restartButton = pygame.Rect(960, 50, 120, 50)
resetButton = pygame.Rect(930, 120, 150, 50)
BFSsearchButton = pygame.Rect(905, 200, 175, 50)
DFSsearchButton = pygame.Rect(930, 290, 150, 50)
randomNeighborsButton = pygame.Rect(905, 380, 175, 60)

def draw_window():
    # draw_window() function
    # Displays all objects on screen of program


    WIN.fill(WHITE)

    # Display all circles on graph as pygame ellipses
    for i in range(1, currentGraph.get_count()+1):
        pygame.draw.ellipse(WIN, currentGraph.get_circle_color(i), currentGraph.get_circle(i))
        WIN.blit(font.render(str(i), True, BLACK), (currentGraph.get_circle(i).centerx-7, currentGraph.get_circle(i).centery-12))

    # Display all text and buttons on the screen
    WIN.blit(font.render(currentGraph.get_result(), True, BLACK), (50, 50))
    pygame.draw.rect(WIN, GREEN, restartButton)
    pygame.draw.rect(WIN, GREEN, resetButton)
    pygame.draw.rect(WIN, GREEN, BFSsearchButton)
    pygame.draw.rect(WIN, GREEN, DFSsearchButton)
    pygame.draw.rect(WIN, GREEN, randomNeighborsButton)

    if currentGraph.get_state() == 'type':
        pygame.draw.rect(WIN, (210, 210, 210), button)
    else:
        pygame.draw.rect(WIN, (130, 130, 130), button)

    WIN.blit(font.render('Remove All', True, BLACK), (970, 60))
    WIN.blit(font.render('Set Target Node:', True, BLACK), (890, 560))
    WIN.blit(font.render('Reset Nodes', True, BLACK), (950, 130))
    WIN.blit(font.render(f'Target Node: {currentGraph.get_target()}', True, BLACK), (930, 260))
    WIN.blit(font.render('BFS Shortest Path', True, BLACK), (910, 210))
    WIN.blit(font.render('DFS Search', True, BLACK), (935, 300))
    WIN.blit(font.render('Generate Random', True, BLACK), (910, 390))
    WIN.blit(font.render('Neighbors', True, BLACK), (940, 410))
    WIN.blit(font.render(currentGraph.textBox, True, BLACK), (920, 610))

    # update_lines() function handles displaying all lines for neighbors on the graph
    update_lines()
    pygame.display.update()



def check_click(x, y):
    # check_click()
    # This function handles all seperate cases of mouse clicks

    # We assume a click on the screen will add a circle until proven otherwise
    add_circle = True

    # Iterate through all circles on the graph
    for i in range(1, currentGraph.count+1):
        circle = currentGraph.get_circle(i)
        x1, y1 = circle.centerx, circle.centery

        # Check if click is within the area of the circle
        if math.sqrt((x1-x)**2 + (y1-y)**2) <= 22.5:
            res = currentGraph.get_marked_circle()

            # If another circle has already been 'marked', or chosen to add a neighbor, then add its neighor as the newly clicked circle
            # Else, make the newly clicked circle the new 'marked' circle
            if res:
                currentGraph.add_neighbor(i, res)
            else:
                currentGraph.set_marked_circle(i)
            add_circle = False

    # If text box is clicked, set program in typing state, else exit typing state
    if ((900 < x < 1050) and (600 < y < 640)):
        if currentGraph.get_state() != 'type':
            currentGraph.set_state('type')
        else:
            currentGraph.set_state('place')

    # If reset button is clicked, reset
    elif ((930 < x < 1080) and (120 < y < 170)):
        currentGraph.reset()

    # If restart button is clicked, restart
    elif ((960 < x < 1080) and (50 < y < 100)):
        currentGraph.restart()

    # Perform BFS shortest path if BFS button is clicked
    elif ((905 < x < 1080) and (200 < y < 250)):
        BFS_ShortestPath((1, 0), currentGraph.get_target())

    # Perform DFS if DFS button is clicked
    elif ((930 < x < 1080) and (290 < y < 340)):
        DFS((1, 0), currentGraph.get_target())

    # If random neighbors button is clicked, generate random neighbors
    elif ((905 < x < 1080) and (380 < y < 440)):
        generate_random_neighbors()
    # Only other case is the user wants to add a circle. Add circle
    else:
        if add_circle == True:
            currentGraph.add_circle(x, y)



def game_loop():
    # game_loop() function
    # This function contains the game loop "while run: ..."
    # This loop keeps the program running while checking for events
    # Events checked for are mouse clicks, key presses, and window closes

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                check_click(x, y)
            if event.type == pygame.KEYDOWN:
                if currentGraph.get_state() == 'type':
                    if event.key == pygame.K_RETURN:
                        currentGraph.set_target(int(currentGraph.textBox))
                        currentGraph.textBox = ''
                        currentGraph.set_state('place')
                    else:
                        currentGraph.textBox += event.unicode

        draw_window()
    pygame.quit()

if __name__ == '__main__':
    game_loop()


