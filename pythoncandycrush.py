import pygame
import random
import sys

# Constants
GRID_SIZE = 8
CELL_SIZE = 64
PADDING = 2
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
FPS = 60

# Define candy colors
CANDY_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Purple
    (255, 165, 0)   # Orange
]
NUM_CANDIES = len(CANDY_COLORS)

# Add special candy types
SPECIAL_CANDY = {
    'striped': 'striped',  # Clears a row or column
    'bomb': 'bomb'         # Clears a 3x3 area
}

# Initialize Pygame
def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption('Candy Crush')
    return screen, pygame.time.Clock()

# Modify the grid to include special candies
def create_grid():
    return [[{'type': 'normal', 'color': random.randrange(NUM_CANDIES)} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Draw grid and candies
def draw_grid(screen, grid):
    screen.fill((50, 50, 50))
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            candy = grid[y][x]
            color = CANDY_COLORS[candy['color']]
            rect = pygame.Rect(x*CELL_SIZE+PADDING, y*CELL_SIZE+PADDING,
                               CELL_SIZE-2*PADDING, CELL_SIZE-2*PADDING)
            pygame.draw.rect(screen, color, rect)
            if candy['type'] == SPECIAL_CANDY['striped']:
                pygame.draw.line(screen, (255, 255, 255), rect.topleft, rect.bottomright, 3)
            elif candy['type'] == SPECIAL_CANDY['bomb']:
                pygame.draw.circle(screen, (255, 255, 255), rect.center, CELL_SIZE//4)
    pygame.display.flip()

# Add this function to render the score
def draw_score(screen, score):
    font = pygame.font.Font(None, 36)  # Use a default font with size 36
    text = font.render(f'Score: {score}', True, (255, 255, 255))  # White text
    screen.blit(text, (10, 10))  # Draw the text at the top-left corner

# Swap two candies
def swap(grid, pos1, pos2):
    y1, x1 = pos1
    y2, x2 = pos2
    grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]

# Animate candy swap
def animate_swap(screen, grid, pos1, pos2):
    y1, x1 = pos1
    y2, x2 = pos2
    rect1 = pygame.Rect(x1 * CELL_SIZE + PADDING, y1 * CELL_SIZE + PADDING,
                        CELL_SIZE - 2 * PADDING, CELL_SIZE - 2 * PADDING)
    rect2 = pygame.Rect(x2 * CELL_SIZE + PADDING, y2 * CELL_SIZE + PADDING,
                        CELL_SIZE - 2 * PADDING, CELL_SIZE - 2 * PADDING)
    steps = 10  # Number of animation steps
    for step in range(steps + 1):
        screen.fill((50, 50, 50))  # Clear screen
        draw_grid(screen, grid)  # Draw the grid
        # Interpolate positions
        offset_x = (x2 - x1) * CELL_SIZE * step / steps
        offset_y = (y2 - y1) * CELL_SIZE * step / steps
        pygame.draw.rect(screen, CANDY_COLORS[grid[y1][x1]['color']],
                         rect1.move(offset_x, offset_y))
        pygame.draw.rect(screen, CANDY_COLORS[grid[y2][x2]['color']],
                         rect2.move(-offset_x, -offset_y))
        pygame.display.flip()
        pygame.time.delay(30)

# Find matches (>=3 in row or col)
def find_matches(grid):
    matched = set()
    # Horizontal
    for y in range(GRID_SIZE):
        count = 1
        for x in range(1, GRID_SIZE):
            if grid[y][x] == grid[y][x-1]:
                count += 1
            else:
                if count >= 3:
                    for k in range(count):
                        matched.add((y, x-1-k))
                count = 1
        if count >= 3:
            for k in range(count):
                matched.add((y, GRID_SIZE-1-k))
    # Vertical
    for x in range(GRID_SIZE):
        count = 1
        for y in range(1, GRID_SIZE):
            if grid[y][x] == grid[y-1][x]:
                count += 1
            else:
                if count >= 3:
                    for k in range(count):
                        matched.add((y-1-k, x))
                count = 1
        if count >= 3:
            for k in range(count):
                matched.add((GRID_SIZE-1-k, x))
    return matched

# Remove matched candies and collapse
def remove_matches(grid, matches):
    for y, x in matches:
        grid[y][x] = None
    # Collapse
    for x in range(GRID_SIZE):
        col = [grid[y][x] for y in range(GRID_SIZE) if grid[y][x] is not None]
        missing = GRID_SIZE - len(col)
        new_col = [None] * missing + col
        for y in range(GRID_SIZE):
            grid[y][x] = new_col[y]
    # Refill
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] is None:
                grid[y][x] = {'type': 'normal', 'color': random.randrange(NUM_CANDIES)}

# Animate collapsing candies
def animate_collapse(screen, grid, matches):
    for _ in range(10):  # Example animation loop
        for y, x in matches:
            rect = pygame.Rect(x * CELL_SIZE + PADDING, y * CELL_SIZE + PADDING,
                               CELL_SIZE - 2 * PADDING, CELL_SIZE - 2 * PADDING)
            pygame.draw.rect(screen, (0, 0, 0), rect)  # Fade out effect
        pygame.display.flip()
        pygame.time.delay(50)

# Check adjacency
def is_adjacent(pos1, pos2):
    y1, x1 = pos1
    y2, x2 = pos2
    return abs(y1-y2) + abs(x1-x2) == 1

# Convert pixel to grid pos
def pixel_to_grid(pos):
    x, y = pos
    return (y // CELL_SIZE, x // CELL_SIZE)

# Main loop
def main():
    screen, clock = init_pygame()
    grid = create_grid()
    selected = None
    score = 0

    # Ensure no initial matches
    while True:
        matches = find_matches(grid)
        if not matches:
            break
        remove_matches(grid, matches)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pixel_to_grid(event.pos)
                if 0 <= pos[0] < GRID_SIZE and 0 <= pos[1] < GRID_SIZE:
                    if selected is None:
                        selected = pos
                    else:
                        if is_adjacent(selected, pos):
                            animate_swap(screen, grid, selected, pos)  # Animate swap
                            swap(grid, selected, pos)
                            matches = find_matches(grid)
                            if matches:
                                while matches:
                                    score += len(matches)
                                    animate_collapse(screen, grid, matches)  # Animate collapse
                                    remove_matches(grid, matches)
                                    matches = find_matches(grid)
                            else:
                                animate_swap(screen, grid, pos, selected)  # Animate swap back
                                swap(grid, selected, pos)  # Swap back
                        selected = None
        draw_grid(screen, grid)
        draw_score(screen, score)  # Draw the score on the screen
        pygame.display.set_caption(f'Candy Crush - Score: {score}')
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
