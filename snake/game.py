import pygame
import random
import heapq
from queue import Queue, LifoQueue

# Kích thước cửa sổ trò chơi
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)

# Khởi tạo Pygame
pygame.init()
pygame.font.init()
FONT = pygame.font.Font(None, 36)

class Node:
    def __init__(self, x, y, parent=None, g=0, h=0):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = g  # Chi phí từ điểm bắt đầu đến node hiện tại
        self.h = h  # Ước tính chi phí từ node hiện tại đến đích
        self.f = g + h  # Tổng chi phí

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return self.f < other.f

def show_menu(screen):
    algorithms = ['bfs', 'dfs', 'dls', 'ga', 'a_star']
    button_height = 50
    button_width = 200
    spacing = 20
    start_y = (HEIGHT - (len(algorithms) * (button_height + spacing))) // 2

    while True:
        screen.fill(BLACK)
        title = FONT.render("Snake Game - Select Algorithm", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, start_y - 50))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        button_rects = []

        for i, algo in enumerate(algorithms):
            button_y = start_y + i * (button_height + spacing)
            button_rect = pygame.Rect((WIDTH - button_width) // 2, button_y, button_width, button_height)
            button_rects.append(button_rect)
            
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, GRAY, button_rect)
            else:
                pygame.draw.rect(screen, WHITE, button_rect, 2)
            
            text = FONT.render(algo.upper(), True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        return algorithms[i]

def draw_game(screen, snake, food, obstacles, score, algorithm):
    screen.fill(BLACK)
    
    # Vẽ lưới
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
    
    # Vẽ rắn
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else BLUE
        pygame.draw.rect(screen, color, (segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
    
    # Vẽ thức ăn và vật cản
    pygame.draw.rect(screen, RED, (food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, (obs.x * CELL_SIZE, obs.y * CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
    
    # Hiển thị điểm và thuật toán
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    algo_text = FONT.render(f"Algorithm: {algorithm.upper()}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(algo_text, (10, 50))

def get_valid_moves(node, snake, obstacles):
    moves = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = node.x + dx, node.y + dy
        if (0 <= new_x < COLS and 0 <= new_y < ROWS and 
            Node(new_x, new_y) not in obstacles and 
            Node(new_x, new_y) not in snake[:-1]):
            moves.append((dx, dy))
    return moves

def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def bfs(start, goal, snake, obstacles):
    queue = Queue()
    queue.put(start)
    visited = {start: None}
    
    while not queue.empty():
        current = queue.get()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return path[::-1]
        
        for dx, dy in get_valid_moves(current, snake, obstacles):
            next_node = Node(current.x + dx, current.y + dy)
            if next_node not in visited:
                visited[next_node] = current
                queue.put(next_node)
    return None

def dfs(start, goal, snake, obstacles):
    stack = [(start, [start])]
    visited = {start}
    
    while stack:
        current, path = stack.pop()
        if current == goal:
            return path
        
        for dx, dy in get_valid_moves(current, snake, obstacles):
            next_node = Node(current.x + dx, current.y + dy)
            if next_node not in visited:
                visited.add(next_node)
                stack.append((next_node, path + [next_node]))
    return None

def dls(start, goal, snake, obstacles, depth_limit):
    def dls_recursive(node, depth, visited):
        if depth < 0:
            return None
        if node == goal:
            return [node]
        if depth == 0:
            return None
            
        for dx, dy in get_valid_moves(node, snake, obstacles):
            next_node = Node(node.x + dx, node.y + dy)
            if next_node not in visited:
                visited.add(next_node)
                path = dls_recursive(next_node, depth - 1, visited)
                if path:
                    return [node] + path
                visited.remove(next_node)
        return None

    visited = {start}
    result = dls_recursive(start, depth_limit, visited)
    return result

def iddfs(start, goal, snake, obstacles, max_depth=50):
    for depth in range(max_depth):
        result = dls(start, goal, snake, obstacles, depth)
        if result:
            return result
    return None

def a_star(start, goal, snake, obstacles):
    open_set = [start]
    closed_set = set()
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}
    
    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        open_set.remove(current)
        closed_set.add(current)
        
        for dx, dy in get_valid_moves(current, snake, obstacles):
            neighbor = Node(current.x + dx, current.y + dy)
            if neighbor in closed_set:
                continue
                
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue
                
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + manhattan_distance(neighbor, goal)
    
    return None

def generate_food(snake, obstacles):
    while True:
        food = Node(random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if food not in snake and food not in obstacles:
            return food

def generate_obstacles(num_obstacles, snake):
    obstacles = set()
    while len(obstacles) < num_obstacles:
        obs = Node(random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if obs not in snake and obs not in obstacles:
            obstacles.add(obs)
    return obstacles

def game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game with Pathfinding")
    clock = pygame.time.Clock()
    
    while True:
        algorithm = show_menu(screen)
        if algorithm is None:
            break
            
        # Khởi tạo trạng thái game
        snake = [Node(COLS//4, ROWS//2), Node(COLS//4-1, ROWS//2)]
        obstacles = generate_obstacles(15, snake)
        food = generate_food(snake, obstacles)
        score = 0
        path = None
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Tìm đường đi mới nếu cần
            if not path:
                if algorithm == 'bfs':
                    path = bfs(snake[0], food, snake, obstacles)
                elif algorithm == 'dfs':
                    path = dfs(snake[0], food, snake, obstacles)
                elif algorithm == 'dls':
                    path = a_star(snake[0], food, snake, obstacles)
                elif algorithm == 'ga':
                    path = a_star(snake[0], food, snake, obstacles)
                elif algorithm == 'a_star':
                    path = a_star(snake[0], food, snake, obstacles)
                
                if not path:
                    running = False
                    continue
                path.pop(0)  # Bỏ vị trí hiện tại
            
            # Di chuyển rắn
            if path:
                next_pos = path.pop(0)
                snake.insert(0, next_pos)
                
                # Kiểm tra ăn mồi
                if snake[0] == food:
                    score += 1
                    food = generate_food(snake, obstacles)
                    path = None
                else:
                    snake.pop()
            
            # Vẽ game
            draw_game(screen, snake, food, obstacles, score, algorithm)
            pygame.display.flip()
            clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    game()