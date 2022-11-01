import pygame
import random

BLOCK_SIZE = 10
SCREEN_SIZE = 300
# draw rect or draw line?
def draw_grid():
    block_size = BLOCK_SIZE
    for x in range(0, screen_width, block_size):
        for y in range(0, screen_height, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


class Snake:
    def __init__(self):
        self.snake_body = []
        self.snake_len = 3
        self.block_size = BLOCK_SIZE
        self.direction = None
        self.body_len = len(self.snake_body)

        self.digest_count = []
        self.digest_position = []

        self.moves = 0
        self.direction = "right"

    def init_snake(self):
        for i in range(self.snake_len, -1, -1):
            self.snake_body.append([i, 0])
        block_size = self.block_size
        head = pygame.Rect(self.snake_body[0][0] * block_size, self.snake_body[0][1] * block_size, block_size,
                           block_size)
        pygame.draw.rect(screen, (255, 0, 0), head)
        for i in self.snake_body[1:]:
            rect = pygame.Rect(i[0] * block_size, i[1] * block_size, block_size, block_size)
            pygame.draw.rect(screen, (200, 0, 255), rect)

    def update_snake(self):
        block_size = self.block_size
        head = pygame.Rect(self.snake_body[0][0] * block_size, self.snake_body[0][1] * block_size, block_size,
                           block_size)
        pygame.draw.rect(screen, (255, 0, 0), head)

        for i in self.snake_body[1:]:
            rect = pygame.Rect(i[0] * block_size, i[1] * block_size, block_size, block_size)
            pygame.draw.rect(screen, (200, 0, 255), rect)

    def move_right(self):
        self.snake_body.pop()
        head = self.snake_body[0]
        self.moves += 1
        self.snake_body.insert(0, [head[0] + 1, head[1]])

    def move_left(self):
        self.snake_body.pop()
        head = self.snake_body[0]
        self.moves += 1
        self.snake_body.insert(0, [head[0] - 1, head[1]])

    def move_up(self):
        self.snake_body.pop()
        head = self.snake_body[0]
        self.moves += 1
        self.snake_body.insert(0, [head[0], head[1] - 1])

    def move_down(self):
        self.snake_body.pop()
        head = self.snake_body[0]
        self.moves += 1
        self.snake_body.insert(0, [head[0], head[1] + 1])

    def get_body_position(self):
        return self.snake_body

    def get_position(self):
        head = self.snake_body[0]
        return head

    def eat(self, food_position):
        self.digest_count.append(len(self.snake_body))
        self.digest_position.append(food_position)

    def digest(self):
        if self.digest_count:
            for i in range(len(self.digest_count)):
                self.digest_count[i] -= 1

                if self.digest_count[0] == 0:
                    self.snake_body.append(self.digest_position[0])

                    del self.digest_count[0]
                    del self.digest_position[0]
                    break

    def slim(self):
        if len(self.snake_body) >= 12:
            self.snake_body = self.snake_body[:int(len(self.snake_body)/3)]

            del self.digest_count[0]
            del self.digest_position[0]


class Food:
    def __init__(self):
        self.block_size = BLOCK_SIZE
        self.x = None
        self.y = None

    def generate_new_pos(self):
        block_size = self.block_size

        # return [random.randint(0, int(screen_width / block_size) - 1),
        #         random.randint(0, int(screen_height / block_size) - 1)]

        return [
            random.randint(0, 1),
            random.randint(0, int(screen_width / block_size) - 1)]

    def update(self, exist_grids):
        block_size = self.block_size

        if self.x is None:
            new_position = self.generate_new_pos()
            while new_position in exist_grids:
                new_position = self.generate_new_pos()

            self.x = new_position[0]
            self.y = new_position[1]

        rect = pygame.Rect(self.x * block_size, self.y * block_size, block_size, block_size)
        pygame.draw.rect(screen, (0, 255, 0), rect)

    def eaten(self):
        self.x = None
        self.y = None

    def get_position(self):
        return [self.x, self.y]


def main():
    global screen_width, screen_height, screen
    snake = Snake()
    food = Food()

    screen_width = SCREEN_SIZE
    screen_height = SCREEN_SIZE

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))

    screen.fill((0, 0, 0))
    pygame.display.set_caption(f"Snake {str(len(snake.snake_body))}")

    clock = pygame.time.Clock()
    clock.tick(100)

    running = True
    snake.init_snake()
    while running:
        snake_moves_pre = snake.moves
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            snake.direction = 'left'
            print('moving left', random.randint(0, int(SCREEN_SIZE/BLOCK_SIZE)-1))
            # snake.move_left()
        elif keys[pygame.K_RIGHT]:
            snake.direction = 'right'
            print('moving right', random.randint(0, int(SCREEN_SIZE/BLOCK_SIZE)-1))
            # snake.move_right()
        elif keys[pygame.K_UP]:
            snake.direction = 'up'
            print('moving up', random.randint(0, int(SCREEN_SIZE/BLOCK_SIZE)-1))
            # snake.move_up()
        elif keys[pygame.K_DOWN]:
            snake.direction = 'down'
            print('moving down', random.randint(0, int(SCREEN_SIZE/BLOCK_SIZE)-1))
            # snake.move_down()

        if snake.direction == 'left':
            snake.move_left()
        if snake.direction == 'right':
            snake.move_right()
        if snake.direction == 'up':
            snake.move_up()
        if snake.direction == 'down':
            snake.move_down()

        screen.fill((0, 0, 0))

        exist_grids = snake.get_body_position()

        draw_grid()

        food.update(exist_grids)
        snake_moves_cur = snake.moves
        if snake_moves_cur != snake_moves_pre:
            snake.digest()

        if snake.get_position() == food.get_position():
            snake.eat(food.get_position())
            food.eaten()
            snake.slim()
            print('eaten')
        snake.update_snake()
        if snake.get_position()[0] < 0 or snake.get_position()[0] >= int(SCREEN_SIZE/BLOCK_SIZE) or snake.get_position()[1] < 0 or \
                snake.get_position()[1] >= int(SCREEN_SIZE/BLOCK_SIZE):
            running = False

        pygame.display.update()


if __name__ == '__main__':
    main()