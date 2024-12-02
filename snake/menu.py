import pygame
import sys

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Kích thước cửa sổ
WIDTH = 600
HEIGHT = 400

# Hàm vẽ các nút bấm
def draw_button(screen, x, y, width, height, text, color):
    font = pygame.font.SysFont('Arial', 30)
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Hàm vẽ menu và các nút
def draw_menu(screen):
    screen.fill(BLACK)

    # Tiêu đề
    font = pygame.font.SysFont('Arial', 40)
    title_text = font.render("Chọn thuật toán", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Vẽ các nút
    button_width = 200
    button_height = 50
    button_y_start = 150

    draw_button(screen, WIDTH // 2 - button_width // 2, button_y_start, button_width, button_height, "BFS", BLUE)
    draw_button(screen, WIDTH // 2 - button_width // 2, button_y_start + 60, button_width, button_height, "DFS", GREEN)
    draw_button(screen, WIDTH // 2 - button_width // 2, button_y_start + 120, button_width, button_height, "DLS", RED)
    draw_button(screen, WIDTH // 2 - button_width // 2, button_y_start + 180, button_width, button_height, "IDDFS", (255, 165, 0))
    draw_button(screen, WIDTH // 2 - button_width // 2, button_y_start + 240, button_width, button_height, "A*", (255, 215, 0))

# Hàm xử lý menu và trả về thuật toán đã chọn
def show_menu(screen):
    running = True
    selected_algorithm = None

    while running:
        draw_menu(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Kiểm tra nếu nhấp chuột trái
                    mouse_x, mouse_y = event.pos

                    # Kiểm tra nếu nhấp vào nút BFS
                    if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and 150 < mouse_y < 200:
                        selected_algorithm = 'bfs'
                        running = False
                    # Kiểm tra nếu nhấp vào nút DFS
                    elif WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and 210 < mouse_y < 260:
                        selected_algorithm = 'dfs'
                        running = False
                    # Kiểm tra nếu nhấp vào nút DLS
                    elif WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and 270 < mouse_y < 320:
                        selected_algorithm = 'dls'
                        running = False
                    # Kiểm tra nếu nhấp vào nút IDDFS
                    elif WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and 330 < mouse_y < 380:
                        selected_algorithm = 'iddfs'
                        running = False
                    # Kiểm tra nếu nhấp vào nút A*
                    elif WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100 and 390 < mouse_y < 440:
                        selected_algorithm = 'a_star'
                        running = False

    return selected_algorithm
