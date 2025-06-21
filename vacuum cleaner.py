import pygame
import random
from collections import deque
import sys

# --- Configuration ---
GRID_SIZE = 9
CELL_SIZE = 50
MARGIN = 2
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + 300

# Colors
DIRTY_COLOR = (255, 180, 180)
CLEAN_COLOR = (180, 255, 180)
AGENT_COLOR = (0, 0, 255)
GOAL_COLOR = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (30, 30, 30)

# --- Environment Setup ---
room = [[random.choice([0, 1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
memory = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # -1: unknown, 0: clean, 1: dirty

# Agent state
agent_x, agent_y = 3, 3
log = []
path_to_goal = []
moves = 0

# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Goal-Based Agent")
font = pygame.font.SysFont("consolas", 16)


def draw_text(text, x, y, color=TEXT_COLOR):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        rendered = font.render(line, True, color)
        screen.blit(rendered, (x, y + i * 18))


def draw_environment():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = CLEAN_COLOR if room[y][x] == 0 else DIRTY_COLOR
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN))
            label = "C" if room[y][x] == 0 else "D"
            text = font.render(label, True, (0, 0, 0))
            screen.blit(text, (x * CELL_SIZE + 18, y * CELL_SIZE + 14))

            if (x, y) == (agent_x, agent_y):
                pygame.draw.rect(screen, AGENT_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN), 3)


def get_neighbors(x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors


def all_cells_clean():
    return all(cell == 0 for row in room for cell in row)


def find_dirty_cell(start_x, start_y):
    queue = deque([(start_x, start_y, [])])
    visited = set()

    while queue:
        x, y, path = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if room[y][x] == 1:
            return path + [(x, y)]

        for nx, ny in get_neighbors(x, y):
            queue.append((nx, ny, path + [(x, y)]))

    return []


def clean_cell():
    global room, memory
    if room[agent_y][agent_x] == 1:
        room[agent_y][agent_x] = 0
        memory[agent_y][agent_x] = 1
        log.append(f"Cleaned ({agent_x}, {agent_y})")
    else:
        memory[agent_y][agent_x] = 0
        log.append(f"Checked clean cell ({agent_x}, {agent_y})")


def move_agent():
    global agent_x, agent_y, moves, path_to_goal
    if not path_to_goal:
        path_to_goal = find_dirty_cell(agent_x, agent_y)

    if path_to_goal:
        agent_x, agent_y = path_to_goal.pop(0)
        moves += 1
        log.append(f"Moved to ({agent_x}, {agent_y})")


def display_status():
    draw_text(f"Moves: {moves}", 10, GRID_SIZE * CELL_SIZE + 10)
    mem_display = "\n".join(str(row) for row in memory)
    draw_text("Memory:\n" + mem_display, 10, GRID_SIZE * CELL_SIZE + 40)
    draw_text("Log:\n" + "\n".join(log[-8:]), 250, GRID_SIZE * CELL_SIZE + 40)


# --- Main Game Loop ---
running = True
while running:
    screen.fill(BG_COLOR)
    draw_environment()
    display_status()
    draw_text("Press ENTER for next move or ESC to quit.", 10, HEIGHT - 30)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if not all_cells_clean():
                    clean_cell()
                    move_agent()

    if all_cells_clean() and "Cleaning Complete!" not in log:
        log.append("Cleaning Complete!")

pygame.quit()
sys.exit()
