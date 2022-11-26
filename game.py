import pygame
from random import randint
from constants import *

"""
This module contains a basic implementation of Conway's Game of Life
using pygame.
"""


class Game:
    """
    Contains the implementation of Conway's Game of Life.
    """

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.frame_rate = FRAME_RATE
        self.generation = 0
        self.is_paused = True
        self.next_update = False
        self.previous_generation = False
        self.exit_status = False
        self.is_left_click_pressed = False
        self.is_right_click_pressed = False
        self.active_cells = set()
        self.generation_stack = []

    def draw_grid(self):
        """
        Draws the grid on the display surface.
        """

        # drawing the horizontal lines
        for i in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(self.display_surface,
                             LINE_COLOR,
                             (0, i),
                             (WIDTH, i))

        pygame.draw.line(self.display_surface,
                         LINE_COLOR,
                         (0, HEIGHT - 1),
                         (WIDTH, HEIGHT - 1))

        # drawing the vertical lines
        for j in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(self.display_surface,
                             LINE_COLOR,
                             (j, 0),
                             (j, HEIGHT))

        pygame.draw.line(self.display_surface,
                         LINE_COLOR,
                         (WIDTH - 1, 0),
                         (WIDTH - 1, HEIGHT))

    def draw_states(self):
        """
        Draws the states(ALIVE or DEAD) in the grid(display surface).
        """

        for cell in self.active_cells:
            pygame.draw.rect(self.display_surface,
                             LINE_COLOR,
                             pygame.Rect(pygame.math.Vector2(cell) * TILE_SIZE,
                                         (TILE_SIZE, TILE_SIZE)))

    def render_game_screen(self):
        """
        Renders all the graphical components on the screen.
        """

        self.display_surface.fill(BG_COLOR)
        self.draw_grid()
        self.draw_states()

        pygame.display.update()

    def get_cell(self, position):
        """
        Returns the coordinates of the current cell with respect to the origin.
        """

        return position[0] // TILE_SIZE, position[1] // TILE_SIZE

    def activate(self, cell):
        """
        Activates the current cell.
        """

        self.active_cells.add(tuple(cell))

    def deactivate(self, cell):
        """
        Deactivates the current cell.
        """

        if tuple(cell) in self.active_cells:
            self.active_cells.remove(tuple(cell))

    def toggle(self, cell):
        """
        Toggles the state of the cell.
        """

        if tuple(cell) in self.active_cells:
            self.deactivate(cell)
        else:
            self.activate(cell)

    def event_manager(self):
        """
        Manages all the events/actions of the game loop.
        """

        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        self.is_paused = not self.is_paused
                    if pygame.key.get_pressed()[pygame.K_r]:
                        active_cells = set()
                        for i in range(HEIGHT // TILE_SIZE):
                            for j in range(WIDTH // TILE_SIZE):
                                if randint(0, 1):
                                    active_cells.add((j, i))
                        self.active_cells = active_cells
                    if pygame.key.get_pressed()[pygame.K_e]:
                        self.active_cells = set((j, i) for i in range(HEIGHT // TILE_SIZE) for j in range(WIDTH // TILE_SIZE))
                    if pygame.key.get_pressed()[pygame.K_k]:
                        self.active_cells.clear()
                    if pygame.key.get_pressed()[pygame.K_t]:
                        active_cells = set()
                        for i in range(HEIGHT // TILE_SIZE):
                            for j in range(WIDTH // TILE_SIZE):
                                if (j, i) not in self.active_cells:
                                    active_cells.add((j, i))
                        self.active_cells = active_cells
                    if self.is_paused:
                        if pygame.key.get_pressed()[pygame.K_n]:
                            self.produce_new_generation()
                            self.next_update = True
                        if pygame.key.get_pressed()[pygame.K_p]:
                            self.produce_old_generation()
                            self.previous_generation = True
                    else:
                        if pygame.key.get_pressed()[pygame.K_PLUS] or pygame.key.get_pressed()[pygame.K_KP_PLUS]:
                            self.frame_rate = min(MAX_FRAME_RATE, self.frame_rate + 1)
                        if pygame.key.get_pressed()[pygame.K_MINUS] or pygame.key.get_pressed()[pygame.K_KP_MINUS]:
                            self.frame_rate = max(MIN_FRAME_RATE, self.frame_rate - 1)
                case pygame.MOUSEBUTTONDOWN:
                    if self.is_paused:
                        if pygame.mouse.get_pressed()[0]:
                            self.is_left_click_pressed = True
                            self.activate(self.get_cell(pygame.mouse.get_pos()))
                        elif pygame.mouse.get_pressed()[2]:
                            self.is_right_click_pressed = True
                            self.toggle(self.get_cell(pygame.mouse.get_pos()))
                case pygame.QUIT:
                    self.exit_status = True
                    self.is_paused = True
                case _:
                    if self.is_left_click_pressed:
                        self.activate(self.get_cell(pygame.mouse.get_pos()))
                    if self.is_right_click_pressed:
                        self.toggle(self.get_cell(pygame.mouse.get_pos()))
                    if not pygame.mouse.get_pressed()[0]:
                        self.is_left_click_pressed = False
                    if not pygame.mouse.get_pressed()[2]:
                        self.is_right_click_pressed = False

    def neighbors(self, x, y) -> int:
        """
        Returns the number of neighbors of cell who are ALIVE.
        """

        count = 0
        delta = [-1, 0, +1]

        for dx in delta:
            for dy in delta:
                if dx or dy:
                    if (x + dx, y + dy) in self.active_cells:
                        count += 1

        return count

    def produce_new_generation(self):
        """
        Produces the next generation in Conway's Game of Life.
        """

        for i in range(HEIGHT // TILE_SIZE):
            for j in range(WIDTH // TILE_SIZE):
                neighbors = self.neighbors(j, i)
                if (j, i) in self.active_cells:
                    if neighbors < 2 or neighbors > 3:
                        self.active_cells.remove((j, i))
                else:
                    if neighbors == 3:
                        self.active_cells.add((j, i))

    def store_old_generation(self):
        """
        Stores the current generation in the generation stack.
        """

        self.generation_stack.append(self.active_cells.copy())

        if GENERATION_STACK_SIZE != -1 and len(self.generation_stack) > GENERATION_STACK_SIZE:
            self.generation_stack.pop(0)

    def produce_old_generation(self):
        """
        Produces the previous generation of the current generation.
        """

        if len(self.generation_stack) > 1:
            self.generation_stack.pop()
            self.active_cells = self.generation_stack.pop()

    def update_game_screen(self):
        """
        Updates the game screen based on whether the game is paused(in automatic mode)
        or played in manual mode.
        """

        if self.next_update:
            pygame.display.update()
            self.next_update = False
            self.generation += 1
            self.store_old_generation()
        elif self.previous_generation:
            pygame.display.update()
            self.previous_generation = False
            if len(self.generation_stack) > 1:
                self.generation -= 1
        elif not self.is_paused:
            pygame.display.update()
            self.generation += 1
            self.produce_new_generation()
            self.store_old_generation()

    def play(self):
        """
        Call this method to get the game of life started.
        """

        self.render_game_screen()

        while self.exit_status is False:
            pygame.display.set_caption(f"Conway's Game of Life (Generation : {self.generation})")
            self.render_game_screen()
            self.event_manager()
            self.update_game_screen()
            self.clock.tick(self.frame_rate)
        pygame.quit()
        exit(0)


if __name__ == "__main__":
    Game().play()
