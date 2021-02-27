import copy

import pygame
from abc import ABC, abstractmethod

from pygame.time import Clock


class Board(ABC):
    def __init__(self, width, height, cell_size=30, left_shift=10, top_shift=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.left_shift = left_shift
        self.top_shift = top_shift

        self.board = [[0] * self.width for _ in range(self.height)]

    def set_view(self, cell_size=30, left_shift=10, top_shift=10):
        self.cell_size = cell_size
        self.left_shift = left_shift
        self.top_shift = top_shift

    def render(self, screen):
        color = "white"
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, color, (j * self.cell_size + self.left_shift,
                                                 i * self.cell_size + self.top_shift,
                                                 self.cell_size, self.cell_size), 1)

    def get_cell(self, pos):
        x_index = (pos[0] - self.left_shift) // self.cell_size
        y_index = (pos[1] - self.top_shift) // self.cell_size

        if 0 <= x_index < self.width and 0 <= y_index < self.height:
            return x_index, y_index
        return None

    @abstractmethod
    def on_click(self, cell):
        pass

    def click(self, pos):
        cell = self.get_cell(pos)
        if cell:
            self.on_click(cell)


class Life(Board, ABC):

    LIFE_NEIGH = 3
    MANY_NEIGH = 4
    LESS_NEIGH = 2

    def __init__(self, width, height, cell_size=30, left_shift=10, top_shift=10):
        super().__init__(width, height, cell_size, left_shift, top_shift)

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def render(self, screen):
        super(Life, self).render(screen)
        for i in range(self.height):
            for j in range(self.width):
                if self.board[j][i]:
                    pygame.draw.rect(screen, "green", (i * self.cell_size + self.left_shift,
                                                       j * self.cell_size + self.top_shift,
                                                       self.cell_size, self.cell_size), 0)

    def next_move(self):
        temp_board = copy.deepcopy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        s += self.board[y + dy][x + dx]
                s -= self.board[y][x]
                if s == Life.LIFE_NEIGH:
                    temp_board[y][x] = 1
                if s > Life.MANY_NEIGH or s < Life.LESS_NEIGH:
                    temp_board[y][x] = 0
        self.board = copy.deepcopy(temp_board)


def main():
    pygame.init()
    size = (500, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Игра «Жизнь»")

    board = Life(10, 10)
    run = True
    time_on = False
    fps = 10
    clock = Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                board.click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                time_on = not time_on
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_WHEELUP:
                fps += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_WHEELDOWN:
                fps -= 1
        screen.fill("black")
        board.render(screen)
        if time_on:
            board.next_move()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
