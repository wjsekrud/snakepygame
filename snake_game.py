import pygame
import os
import sys
import random
from time import sleep

# Game screen global variable
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

# Direction global variable
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Color global variable
WHITE = (255, 255, 255)
ORANGE = (250, 150, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

OBSTACLE_SHAPES = [
    [(0, 0)],  # 1x1 정사각형
    [(0, 0), (1, 0)],  # 1x2 직사각형
    [(0, 0), (0, 1)],  # 2x1 직사각형
    [(0, 0), (1, 0), (0, 1), (1, 1)]  # 2x2 정사각형
]

# Snake Object
class Snake(object):
    def __init__(self, GameRef):
        self.create()
        self.game = GameRef

    # Snake create
    def create(self):
        self.length = 2
        self.positions = [(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # Control snake direction
    def control(self, xy):
        self.direction = xy
        # code here

    # Snake movement
    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (cur[0] + (x * GRID_SIZE)), (cur[1] + (y * GRID_SIZE))

        # If the snake touches its own body, the snake is recreated from the beginning
        if new in self.positions[2:]:
            sleep(1)
            print('snake length: ' + str(self.length))
            self.game.restart()
        # If the snake goes beyond the game screen, the snake is recreated from the beginning
        elif new[0] > SCREEN_WIDTH or new[0] < 0 or new[1] > SCREEN_HEIGHT or new[1] < 0:
            sleep(1)
            print('snake length: ' + str(self.length))
            self.game.restart()
            # code here
        # If the snake moves normally
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop(-1)
        # code here

    # When the snake eats the food
    def eat(self):
        self.length += 1

    # Draw snake
    def draw(self, screen):
        red, green, blue = 50 / (self.length - 1), 150, 150 / (self.length - 1)
        for i, p in enumerate(self.positions):
            color = (100 + red * i, green, blue * i)
            rect = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, rect)


# Class Feed
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    # Create Food
    def create(self, snake_positions=[], obstacle_positions=[[]]):
        w = int(SCREEN_WIDTH / 2)
        h = int(SCREEN_HEIGHT / 2)
        sz = GRID_SIZE
        chk = True

        while chk:
            new_position = [sz * random.randint(int(-w/sz)+1, int(h/sz)-1) + w, sz * random.randint(int(-h/sz)+1, int(h/sz)-1) + h]

            if new_position not in snake_positions:
                chk = self.checkposition(new_position, obstacle_positions)
            else:
                pass
                
    def checkposition(self, new, obstacle_positions=[[]]):
        if obstacle_positions == [[]]:
            self.position = new
            return False
        else:
            tple = (new[0],new[1])
            if tple in obstacle_positions:
                return True
            else:
                self.position = new
        return False


    # Draw Food
    def draw(self, screen):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)

class SpecialFeed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = BLUE
        self.active = False

    def create(self, snake_positions=[], obstacle_positions=[[]]):
        w = int(SCREEN_WIDTH / 2)
        h = int(SCREEN_HEIGHT / 2)
        sz = GRID_SIZE
        
        chk = True

        while chk:
            new_position = [sz * random.randint(int(-w/sz)+1, int(h/sz)-1) + w, sz * random.randint(int(-h/sz)+1, int(h/sz)-1) + h]

            if new_position not in snake_positions:
                chk = self.checkposition(new_position, obstacle_positions)
            else:
                pass
                
    def checkposition(self, new, obstacle_positions=[[]]):
        if obstacle_positions == [[]]:
            self.position = new
            self.active = True
            return False
        else:
            tple = (new[0],new[1])
            if tple in obstacle_positions:
                return True
            else:
                self.position = new
                self.active = True
        return False



    def draw(self, screen):
        if self.active:
            rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color, rect)

class Obstacle(object):
    def __init__(self, shape):
        self.shape = shape
        self.color = GRAY
        self.positions = []

    def create(self, snake_positions):
        while True:
            w = int(SCREEN_WIDTH / 2)
            h = int(SCREEN_HEIGHT / 2)
            sz = GRID_SIZE
            base_position = [sz * random.randint(int(-w/sz)+1, int(h/sz)-1) + w, sz * random.randint(int(-h/sz)+1, int(h/sz)-1) + h]
            self.positions = [(base_position[0] + offset[0] * GRID_SIZE, base_position[1] + offset[1] * GRID_SIZE) for offset in self.shape]
            
            if not any(abs(pos[0] - snake_pos[0]) <= GRID_SIZE * 5 and abs(pos[1] - snake_pos[1]) <= GRID_SIZE * 5 for pos in self.positions for snake_pos in snake_positions):
                break

    def draw(self, screen):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color, rect)
        
# Game class
class Game(object):
    def __init__(self):
        self.snake = Snake(self)
        self.feed = Feed()
        self.special_feed = SpecialFeed()
        self.obstacles = []
        self.speed = 20
        
    def restart(self):
        self.snake.create()
        self.feed.create()
        self.special_feed.create()
        self.special_feed.active = False
       
        self.obstacles = []

    # Game event handling and control
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.control(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.control(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.control(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.control(RIGHT)
        return False

    # Perform game logic
    def check_collision(self, snake, obstacle):
        for pos in snake.positions:
            for obpos in obstacle.positions:
                if pos[0] == obpos[0] and pos[1] == obpos[1]:
                    return True
        return False

    def run_logic(self):
        self.snake.move()
        self.check_eat(self.snake, self.feed)
        self.check_special_eat(self.snake, self.special_feed)
        self.speed = (20 + self.snake.length) / 4

        # 장애물과 충돌 검사
        for obstacle in self.obstacles:
            if self.check_collision(self.snake, obstacle):
                sleep(1)
                print('snake length: ' + str(self.snake.length))
                self.restart()

        if random.random() < 0.003 and not self.special_feed.active:
            # 장애물 위치 리스트 생성
            obstacle_positions = [pos for obstacle in self.obstacles for pos in obstacle.positions]
            
            self.special_feed.create(self.snake.positions, obstacle_positions)

    # Check if the snake has eaten the food
    def check_eat(self, snake, feed):
        for pos in snake.positions:
            if pos[0] == feed.position[0] and pos[1] == feed.position[1]:
                print("eat")
                snake.eat()
                
                # 랜덤한 크기와 모양의 장애물 추가
                obstacle_shape = random.choice(OBSTACLE_SHAPES)
                obstacle = Obstacle(obstacle_shape)
                obstacle.create(snake.positions)
                self.obstacles.append(obstacle)
                for obs in self.obstacles:
                    obs.create(snake.positions)
                obstacle_positions = [pos for obstacle in self.obstacles for pos in obstacle.positions]
                
                feed.create(snake.positions, obstacle_positions)
                self.check_eat(snake, feed)

    def check_special_eat(self, snake, special_feed):
        if special_feed.active:
            for pos in snake.positions:
                if pos[0] == special_feed.position[0] and pos[1] == special_feed.position[1]:
                    print("special eat")
                    snake.eat()
                    self.special_feed.active = False
                    self.obstacles = []
                    break

        # code here

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Display game information
    def draw_info(self, length, speed, screen):
        info = "Length: " + str(length) + "    " + "Speed: " + str(round(speed, 2))
        font_path = resource_path("assets/NanumGothicCoding-Bold.ttf")
        font = pygame.font.Font(font_path, 26)
        text_obj = font.render(info, 1, GRAY)
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(text_obj, text_rect)

    # Handle game frames
    def display_frame(self, screen):
        screen.fill(WHITE)
        self.draw_info(self.snake.length, self.speed, screen)
        self.snake.draw(screen)
        self.feed.draw(screen)
        self.special_feed.draw(screen)
        for obstacle in self.obstacles:  # 장애물 리스트 그리기
            obstacle.draw(screen)
        screen.blit(screen, (0, 0))

# Set resource path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    # Game initialization and environment setup
    pygame.init()
    pygame.display.set_caption('Snake Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        pygame.display.flip()
        clock.tick(game.speed)

    pygame.quit()


if __name__ == '__main__':
    main()
