import pygame
import os
import sys
import random
from time import sleep
import heapq

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
BLACK = (0, 0, 0)

OBSTACLE_SHAPES = [
    [(0, 0)],  # 1x1 정사각형
    [(0, 0), (1, 0)],  # 1x2 직사각형
    [(0, 0), (0, 1)],  # 2x1 직사각형
    [(0, 0), (1, 0), (0, 1), (1, 1)]  # 2x2 정사각형
]

# Snake Object
class Snake(object):
    def __init__(self, gameRef):
        self.game = gameRef
        self.create()
        

    # Snake create
    def create(self):
        self.path = []
        self.automove = False
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
            self.game.game_over = True
            return
        # If the snake goes beyond the game screen, the snake is recreated from the beginning
        elif new[0] > SCREEN_WIDTH or new[0] < 0 or new[1] > SCREEN_HEIGHT or new[1] < 0:
            sleep(1)
            print('snake length: ' + str(self.length))
            self.game.game_over = True
            return
            # code here
        # If the snake moves normally
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop(-1)
            return
        # code here
    
    def autocontrol(self):

        if self.path == []:
            return
        
        head = self.positions[0]
        next_pos = self.path.pop(0)

        # 스네이크의 현재 위치와 목표 위치 비교
        if head[0] < next_pos[1] * GRID_SIZE:
            self.control(RIGHT)
        elif head[0] > next_pos[1] * GRID_SIZE:
            self.control(LEFT)
        elif head[1] < next_pos[0] * GRID_SIZE:
            self.control(DOWN)
        elif head[1] > next_pos[0] * GRID_SIZE:
            self.control(UP)

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

    def dijkstra(self, grid, start, end):
        rows, cols = len(grid), len(grid[0])
        dist = [[float('inf')] * cols for _ in range(rows)]
        prev = [[None] * cols for _ in range(rows)]
        dist[start[0]][start[1]] = 0
        pq = [(0, start)]
        
        while pq:
            d, (r, c) = heapq.heappop(pq)
            if (r, c) == end:
                self.path = []
                while (r, c) != start:
                    self.path.append((r, c))
                    r, c = prev[r][c]
                self.path.append(start)
                self.path.reverse()
                self.path = self.path[1:]
                return d, self.path
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:

                    if (nc * GRID_SIZE, nr * GRID_SIZE) in self.positions:
                        if self.length - self.positions.index((nc * GRID_SIZE, nr * GRID_SIZE)) - 1 >= d:
                            continue
                    
                    new_dist = d + 1
                    if new_dist < dist[nr][nc]:
                        dist[nr][nc] = new_dist
                        prev[nr][nc] = (r, c)
                        heapq.heappush(pq, (new_dist, (nr, nc)))
        
        return float('inf'), []
    
    def calculate_max_score(self, game):
        grid = [[0] * int(GRID_WIDTH) for _ in range(int(GRID_HEIGHT))]
        if game.obstacles != [[]]:
            for obstacle in game.obstacles:
                for pos in obstacle.positions:
                    try:
                        #print(pos)
                        grid[int(pos[1] / GRID_SIZE)][int(pos[0] / GRID_SIZE)] = 1
                    except:
                        print("err!")
        
        for pos in self.positions[1:]:
            grid[int(pos[1] / GRID_SIZE)][int(pos[0] / GRID_SIZE)] = 1
                    
        
        start = (int(self.positions[0][1] / GRID_SIZE), int(self.positions[0][0] / GRID_SIZE))
        end = (int(game.feed.position[1] / GRID_SIZE), int(game.feed.position[0] / GRID_SIZE))
        
        min_distance, path = self.dijkstra(grid, start, end)

        print(min_distance,  min_distance // 10 , min_distance // 10 * 10, 100 - (min_distance // 10) * 10)
        
        max_score = 100 - (min_distance // 10) * 10
        
        return min_distance, max_score, path


# Class Feed
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.create()

    # Create Food
    def create(self, snake_positions=[], obstacle_positions=[[]]):
        self.color = ORANGE
        self.score = 100
        self.frame = 0
        self.remainingtime = 10

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
    
    def passframe(self):
        self.frame += 1
        if self.frame >= 10:
            self.rot()
            self.frame = 0
        return

    def rot(self):
        self.score = self.score - 10
        rotiter = (100 - self.score) // 10
        red, green, blue = max(250- 10 * rotiter,100), 150, min(15 * rotiter, 100)
        self.color = [red, green, blue]


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
            
            if not any(abs(pos[0] - snake_pos[0]) <= GRID_SIZE * 2 and abs(pos[1] - snake_pos[1]) <= GRID_SIZE * 2 for pos in self.positions for snake_pos in snake_positions):
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
        self.score = 0
        self.min_distance, self.max_increment, self.path = self.snake.calculate_max_score(self)
        self.max_score = 0

        self.game_over = False
        self.player_name = "___"
        self.flipflop = 20

        self.autorun = False

    def restart(self):
        self.player_name = "___"
        self.game_over = False
        self.flipflop = 20

        self.snake.create()
        self.feed.create()
        self.special_feed.create()
        self.special_feed.active = False
       
        self.obstacles = []
        self.score = 0
        self.min_distance, self.max_increment, self.path = self.snake.calculate_max_score(self)
        self.max_score = 0




    # Game event handling and control
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN and self.autorun == False:
                if event.key == pygame.K_UP:
                    self.snake.control(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.control(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.control(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.control(RIGHT)
                if event.key == pygame.K_ESCAPE:
                    return True
            elif event.type == pygame.KEYDOWN and self.autorun == True:
                if event.key == pygame.K_LCTRL:
                    self.game_over = True
                    self.autorun = False
                elif event.key == pygame.K_ESCAPE:
                    return True
        return False

    # Perform game logic
    def check_collision(self, snake, obstacle):
        for pos in snake.positions:
            for obpos in obstacle.positions:
                if pos[0] == obpos[0] and pos[1] == obpos[1]:
                    return True
        return False

    def run_logic(self):
        if not self.game_over:
            if self.autorun == True:
                self.snake.autocontrol()
            self.snake.move()
            self.check_eat(self.snake, self.feed)
            self.check_special_eat(self.snake, self.special_feed)
            self.speed = (20 + self.snake.length) / 4
            self.feed.passframe()

            # 장애물과 충돌 검사
            for obstacle in self.obstacles:
                if self.check_collision(self.snake, obstacle):
                    sleep(1)
                    print('snake length: ' + str(self.snake.length))
                    self.game_over = True

            if random.random() < 0.003 and not self.special_feed.active:
                # 장애물 위치 리스트 생성
                obstacle_positions = [pos for obstacle in self.obstacles for pos in obstacle.positions]
                
                self.special_feed.create(self.snake.positions, obstacle_positions)

    def spawnObstacles(self):
        obstacle_shape = random.choice(OBSTACLE_SHAPES)
        obstacle = Obstacle(obstacle_shape)
        obstacle.create(self.snake.positions)
        self.obstacles.append(obstacle)
        for obs in self.obstacles:
            obs.create(self.snake.positions)
        return  [pos for obstacle in self.obstacles for pos in obstacle.positions]

    def spawnThings(self):
        Obspos = self.spawnObstacles()
        self.feed.create(self.snake.positions, Obspos)

    # Check if the snake has eaten the food
    def check_eat(self, snake, feed):
        cnt = 0
        for pos in snake.positions:
            if pos[0] == feed.position[0] and pos[1] == feed.position[1]:
                
                #print("eat")
                snake.eat()
                self.score += feed.score
                print(self.max_increment)
                self.max_score += self.max_increment
                
                # 랜덤한 크기와 모양의 장애물 추가

                while True:
                    self.spawnThings()
                    _, self.max_increment, self.path = snake.calculate_max_score(self)
                    cnt += 1
                    if cnt > 10:
                        self.game_over = True
                        break
                    if self.path != []:
                        break

                self.check_eat(snake, feed)

    def check_special_eat(self, snake, special_feed):
        if special_feed.active:
            for pos in snake.positions:
                if pos[0] == special_feed.position[0] and pos[1] == special_feed.position[1]:
                    #print("special eat")
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
        try:
            info = f"length: {str(length)}  Speed: {str(round(speed, 2))}   Score: {str(self.score)}/{str(self.max_score)}, {str(int(self.score/max((self.max_score,1)) * 100))}%"
        except:
            print(f"error occured, Len{length}, spd{speed}, scr{self.score}, mxsrc{self.max_score}")
        font_path = resource_path("assets/NanumGothicCoding-Bold.ttf")
        font = pygame.font.Font(font_path, 26)
        text_obj = font.render(info, 2, BLACK)
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 20
        screen.blit(text_obj, text_rect)

    def draw_dijkstrapath(self, screen):
        for r, c in self.path:
            pos = (c * GRID_SIZE, r * GRID_SIZE)
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (230, 230, 255), rect)

    # Handle game frames
    def display_frame(self, screen):
        screen.fill(WHITE)
        self.draw_dijkstrapath(screen)
        self.snake.draw(screen)
        self.feed.draw(screen)
        self.special_feed.draw(screen)
        for obstacle in self.obstacles:  # 장애물 리스트 그리기
            obstacle.draw(screen)
        self.draw_info(self.snake.length, self.speed, screen)

        #print(self.flipflop)
        if self.game_over and self.flipflop > 0:
            self.draw_game_over(screen)
            self.draw_player_name(screen)
            self.draw_rankings(screen)
            self.flipflop -= 1
        elif self.game_over:
            self.flipflop += 20

        screen.blit(screen, (0, 0))

    def draw_game_over(self, screen):
        font_path = resource_path("assets/ARCADE_N.ttf")
        font = pygame.font.Font(font_path, 36) 
        text = font.render("Game Over", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180)
        screen.blit(text, text_rect)

        font = pygame.font.Font(font_path, 24)
        text = font.render(f"SCORE: {self.score}, {self.snake.length}CM", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        screen.blit(text, text_rect)

    def draw_player_name(self, screen):
        font_path = resource_path("assets/ARCADE_N.ttf")
        font = pygame.font.Font(font_path, 24)
        text = font.render("Enter your name: " + self.player_name, True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 -70)
        screen.blit(text, text_rect)

    def draw_rankings(self, screen):
        font_path = resource_path("assets/ARCADE_N.ttf")
        font = pygame.font.Font(font_path, 24)
        rankings = self.load_scores()
        
        x = SCREEN_WIDTH // 2 - 325
        y = SCREEN_HEIGHT // 2 + 10
        
        for i, (name, score, len, performance) in enumerate(rankings[:5], start=1):
            text = font.render(f"{i}. {name}: {score}({performance}%),  {len}cm", True, BLACK)
            screen.blit(text, (x, y))
            y += 30

    def save_score(self):
        with open("scores.txt", "a") as file:
            file.write(f"{self.player_name} {self.score} {self.snake.length} {round(self.score/max(self.max_score,1),1) * 100}\n")

    def load_scores(self):
        scores = []
        if os.path.exists("scores.txt"):
            with open("scores.txt", "r") as file:
                for line in file:
                    name, score, length, performance = line.strip().split()
                    scores.append((name, int(score), length, performance))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

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
        
        if game.game_over:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                        done = True

                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        unicode = str(event.unicode).upper()
                        game.player_name += unicode
                        if len(game.player_name) > 3:
                            game.player_name = game.player_name[1:]

                    elif event.key == pygame.K_ESCAPE:
                        done = True  
                    elif event.key == pygame.K_RETURN:
                        game.autorun = False
                        game.save_score()
                        game.restart()
                    
                    elif event.key == pygame.K_LCTRL:
                        game.save_score()
                        game.autorun = True
                        game.restart()
        else:
            done = game.process_events()
            game.run_logic()

        game.display_frame(screen)
        pygame.display.flip()
        clock.tick(game.speed)

    pygame.quit()


if __name__ == '__main__':
    main()
