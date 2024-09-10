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
    def __init__(self):
        self.neighbors = {}
        self.circles = {}
        self.count = 0
        self.result = ''
        self.state = 'place'
        self.marked_circle = None
        self.target = None

    def get_neighbors(self, node):
        return self.neighbors[node]

    def add_neighbor(self, node, neighbor):
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
        for circle in self.circles.values():
            circle.set_color(GREEN)
        for k in range(1, len(self.neighbors)+1):
            self.neighbors[k] = []
        self.result = ''
        self.target = None

    def restart(self):
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


c = CustomGraph()


def visit(node, target=None):
    i, d = node
    print('Visited node ' + str(i))
    c.mark(i, RED)
    pygame.time.wait(150)
    pygame.draw.ellipse(WIN, c.get_circle_color(i), c.get_circle(i))
    if i == target:
        c.change_result('Shortest path to node ' + str(i) + ' is distance ' + str(d))
        return True
    pygame.display.update()


def BFS_ShortestPath(origin, target):
    c.reset_colors()
    pygame.display.update()
    if c.get_count() == 0:
        return
    visited = [False] * c.get_count()
    previous = [None] * c.get_count()
    ans = []
    stack = [origin]
    while stack:
        i, d = stack.pop(0)
        if visit((i, d), target):
            while True:
                ans.append(i)
                if not previous[i-1]:
                    print(ans)
                    break
                else:
                    i = previous[i-1]
            for k in ans:
                c.mark(k, BLUE)
            break
        visited[i - 1] = True
        n = c.get_neighbors(i)
        for j in n:
            if not visited[j-1]:
                stack.append((j, d+1))
                if not previous[j-1]:
                    previous[j-1] = i
    if not c.get_result():
        c.change_result('Search Complete.')

def DFS(origin, target):
    c.reset_colors()
    pygame.display.update()
    found = False
    if c.get_count() == 0:
        return
    visited = [False] * c.get_count()
    stack = [origin]
    while stack:
        i, d = stack.pop()
        if visit((i, d), target):
            found = True
        visited[i - 1] = True
        n = c.get_neighbors(i)
        for j in n:
            if not visited[j-1]:
                stack.append((j, d+1))
    if found:
        c.change_result(f'Depth-First Search Complete. Target node {target} reachable from origin.')
    else:
        c.change_result('Depth-First Search Complete.')


def generate_random_neighbors():
    j = c.get_count()
    for k in range(1, j+1):
        t = random.randrange(1, j+1)
        while t == k:
            t = random.randrange(1, j+1)
        c.add_neighbor(k, t)


def update_lines():
    for i in range(1, c.count+1):
        x, y = c.get_circle(i).centerx, c.get_circle(i).centery
        for j in c.get_neighbors(i):
            a, b = c.get_circle(j).centerx, c.get_circle(j).centery
            pygame.draw.line(WIN, BLACK, (x, y), (a, b), 4)


button = pygame.Rect(900, 600, 150, 40)
restartButton = pygame.Rect(960, 50, 120, 50)
resetButton = pygame.Rect(930, 120, 150, 50)
BFSsearchButton = pygame.Rect(905, 200, 175, 50)
DFSsearchButton = pygame.Rect(930, 290, 150, 50)

def draw_window():
    WIN.fill(WHITE)
    for i in range(1, c.get_count()+1):
        pygame.draw.ellipse(WIN, c.get_circle_color(i), c.get_circle(i))
        WIN.blit(font.render(str(i), True, BLACK), (c.get_circle(i).centerx-7, c.get_circle(i).centery-12))
    WIN.blit(font.render(c.get_result(), True, BLACK), (50, 50))
    pygame.draw.rect(WIN, GREEN, restartButton)
    pygame.draw.rect(WIN, GREEN, resetButton)
    WIN.blit(font.render('Remove All', True, BLACK), (970, 60))
    WIN.blit(font.render('Set Target Node:', True, BLACK), (890, 560))
    WIN.blit(font.render('Reset Nodes', True, BLACK), (950, 130))
    WIN.blit(font.render(f'Target Node: {c.get_target()}', True, BLACK), (930, 260))
    if c.get_state() == 'type':
        pygame.draw.rect(WIN, (210, 210, 210), button)
    else:
        pygame.draw.rect(WIN, (130, 130, 130), button)
    pygame.draw.rect(WIN, GREEN, BFSsearchButton)
    pygame.draw.rect(WIN, GREEN, DFSsearchButton)
    WIN.blit(font.render('BFS Shortest Path', True, BLACK), (910, 210))
    WIN.blit(font.render('DFS Search', True, BLACK), (935, 300))
    WIN.blit(font.render(textBox, True, BLACK), (920, 610))
    update_lines()
    pygame.display.update()


textBox = ''

def check_click(x, y):
    g = True
    for i in range(1, c.count+1):
        circle = c.get_circle(i)
        x1, y1 = circle.centerx, circle.centery
        if math.sqrt((x1-x)**2 + (y1-y)**2) <= 22.5:
            res = c.get_marked_circle()
            if res:
                c.add_neighbor(i, res)
            else:
                c.set_marked_circle(i)
            g = False
    if ((900 < x < 1050) and (600 < y < 640)):
        if c.get_state() != 'type':
            c.set_state('type')
        else:
            c.set_state('place')
    elif ((930 < x < 1080) and (120 < y < 170)):
        c.reset()
    elif ((960 < x < 1080) and (50 < y < 100)):
        c.restart()
    elif ((905 < x < 1080) and (200 < y < 250)):
        BFS_ShortestPath((1, 0), c.get_target())
    elif ((930 < x < 1080) and (290 < y < 340)):
        DFS((1, 0), c.get_target())
    else:
        if g == True:
            c.add_circle(x, y)



def game_loop():
    global textBox
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
                if event.key == pygame.K_LEFT:
                    generate_random_neighbors()
                elif c.get_state() == 'type':
                    if event.key == pygame.K_RETURN:
                        c.set_target(int(textBox))
                        textBox = ''
                        c.set_state('place')
                    else:
                        textBox += event.unicode

        draw_window()
    pygame.quit()

if __name__ == '__main__':
    game_loop()


