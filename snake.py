import pygame, sys, random
from pygame.math import Vector2

pygame.init()

# -------------------- COLORS --------------------
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
RED = (200, 50, 50)
BLACK = (0, 0, 0)

# -------------------- GRID SETTINGS --------------------
cell_size = 30
number_of_cells = 25
total_cells = number_of_cells * number_of_cells

# -------------------- SCREEN SETUP --------------------
screen = pygame.display.set_mode(
    (cell_size * number_of_cells, cell_size * number_of_cells)
)
pygame.display.set_caption("Retro Snake")
clock = pygame.time.Clock()

# -------------------- FONTS --------------------
font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60)
mid_font = pygame.font.SysFont("arial", 36)

# -------------------- BASE CLASS --------------------
class GameObject:
    def __init__(self, position=None):
        self.position = position if position else self.random_position()

    def random_position(self):
        return Vector2(
            random.randint(0, number_of_cells - 1),
            random.randint(0, number_of_cells - 1)
        )

    def draw(self):
        pass

# -------------------- FOOD CLASS --------------------
class Food(GameObject):
    def draw(self):
        rect = pygame.Rect(
            self.position.x * cell_size,
            self.position.y * cell_size,
            cell_size,
            cell_size
        )
        pygame.draw.rect(screen, RED, rect)

# -------------------- SNAKE CLASS --------------------
class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.grow = False
        self.can_turn = True

    def draw(self):
        for block in self.body:
            rect = pygame.Rect(
                block.x * cell_size,
                block.y * cell_size,
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, DARK_GREEN, rect)

    def move(self):
        new_head = self.body[0] + self.direction
        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body = [new_head] + self.body[:-1]

        self.can_turn = True

    def add_block(self):
        self.grow = True

# -------------------- GAME FUNCTIONS --------------------
def new_game():
    return Snake(), [Food()], 0, False, False

def spawn_food():
    foods.append(Food())

def draw_hud():
    score_text = font.render(f"Score: {score}", True, BLACK)
    top_text = font.render(f"Top Score: {top_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(top_text, (10, 40))

def draw_menu(title):
    screen.fill(GREEN)
    title_text = big_font.render(title, True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    top_text = font.render(f"Top Score: {top_score}", True, BLACK)
    restart_text = mid_font.render("Press ENTER to play again", True, BLACK)
    quit_text = font.render("Press ESC to quit", True, BLACK)

    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 150))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 240))
    screen.blit(top_text, (screen.get_width() // 2 - top_text.get_width() // 2, 280))
    screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 360))
    screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 400))
    pygame.display.update()

# -------------------- INITIALIZE GAME --------------------
snake, foods, score, game_over, game_won = new_game()
top_score = 0

MOVE_SNAKE = pygame.USEREVENT
pygame.time.set_timer(MOVE_SNAKE, 150)

# -------------------- MAIN GAME LOOP --------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOVE_SNAKE and not game_over and not game_won:
            snake.move()
            head = snake.body[0]

            if head.x < 0 or head.x >= number_of_cells or head.y < 0 or head.y >= number_of_cells:
                game_over = True

            if head in snake.body[1:]:
                game_over = True

            for food in foods[:]:
                if head == food.position:
                    foods.remove(food)
                    snake.add_block()
                    score += 1
                    top_score = max(top_score, score)
                    spawn_food()
                    if score % 10 == 0:
                        spawn_food()

            if len(snake.body) >= total_cells:
                game_won = True

        if event.type == pygame.KEYDOWN:
            if not game_over and not game_won and snake.can_turn:
                if event.key == pygame.K_UP and snake.direction.y != 1:
                    snake.direction = Vector2(0, -1)
                    snake.can_turn = False
                elif event.key == pygame.K_DOWN and snake.direction.y != -1:
                    snake.direction = Vector2(0, 1)
                    snake.can_turn = False
                elif event.key == pygame.K_LEFT and snake.direction.x != 1:
                    snake.direction = Vector2(-1, 0)
                    snake.can_turn = False
                elif event.key == pygame.K_RIGHT and snake.direction.x != -1:
                    snake.direction = Vector2(1, 0)
                    snake.can_turn = False
            else:
                if event.key == pygame.K_RETURN:
                    snake, foods, score, game_over, game_won = new_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    if game_over:
        draw_menu("GAME OVER")
    elif game_won:
        draw_menu("YOU WIN")
    else:
        screen.fill(GREEN)
        for food in foods:
            food.draw()
        snake.draw()
        draw_hud()
        pygame.display.update()

    clock.tick(60)

