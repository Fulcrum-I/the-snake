from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self) -> None:
        """Задать начальную позицию и цвет игрового объекта."""
        self.position: tuple[int, int] = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.body_color: tuple[int, int, int] | None = None

    def draw(self) -> None:
        """Отрисовать игровой объект. Реализуется в дочерних классах."""
        raise NotImplementedError

    def draw_cell(
        self,
        position: tuple[int, int],
        color: tuple[int, int, int]
    ) -> None:
        """Отрисовать клетку заданного цвета."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, появляющееся в случайной клетке игрового поля."""

    def __init__(
        self,
        occupied_positions: list[tuple[int, int]] | None = None
    ) -> None:
        """Создать яблоко и разместить его на игровом поле."""
        super().__init__()
        self.body_color: tuple[int, int, int] = APPLE_COLOR
        self.randomize_position(occupied_positions or [])

    def randomize_position(
        self,
        occupied_positions: list[tuple[int, int]]
    ) -> None:
        """Перемещение яблока в случайные координаты."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in occupied_positions:
                break

    def draw(self) -> None:
        """Отрисовать яблоко."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Змейка с управляемым движением и изменяемой длиной."""

    length: int
    positions: list[tuple[int, int]]
    direction: tuple[int, int]
    next_direction: tuple[int, int] | None
    last: tuple[int, int] | None

    def __init__(self) -> None:
        """Создать змейку с начальными параметрами."""
        super().__init__()
        self.body_color: tuple[int, int, int] = SNAKE_COLOR
        self.reset()
        self.direction = RIGHT

    def get_head_position(self) -> tuple[int, int]:
        """Получить координаты головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Переместить змейку на одну клетку с учётом границ поля."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_x = (x + (dx * GRID_SIZE)) % SCREEN_WIDTH
        new_y = (y + (dy * GRID_SIZE)) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self) -> None:
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовать змейку."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions[1:]:
            self.draw_cell(position, self.body_color)

        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position(), self.body_color)

    def reset(self) -> None:
        """Сброс змейки при поражении."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object: Snake) -> None:
    """Обработать нажатия клавиш и изменение направления объекта.

    Args:
        game_object: Змейка, направление которой нужно обновить.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Инициализировать игру и запустить основной игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head_position = snake.get_head_position()
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if head_position in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
