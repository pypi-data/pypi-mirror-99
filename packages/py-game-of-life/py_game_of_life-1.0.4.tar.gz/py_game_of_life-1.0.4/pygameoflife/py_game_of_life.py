import random
import sys
import pygame
import os
import time
import copy


# No need for this now, as we glued up the edges
def valid_cell(r, c):
    return 0 <= r < ROWS and 0 <= c < COLUMNS


class Game_Of_Life:
    def __init__(self, screen_width=1000, screen_height=840, cell_size=10, alive_color=(128, 0, 128),
                 dead_color=(0, 0, 0), max_fps=10):
        """
        Initialize the game, and sets defaults setting
        """

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.max_fps = max_fps
        self.rows = int(self.screen_height / self.cell_size)
        self.columns = int(self.screen_width / self.cell_size)
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        self.last_time_updated = 0
        self.paused = False
        pygame.display.flip()

        # self.active_grid = [ [0] * self.columns] * self.rows
        self.active_grid = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.inactive_grid = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.randomize_grid()

    def randomize_grid(self):
        for r in range(self.rows):
            for c in range(self.columns):
                self.active_grid[r][c] = random.randint(0, 1)

        self.clear_screen()
        self.draw_grid()

    def clear_screen(self):
        """
        Basically clears the screen
        """
        self.screen.fill(self.dead_color)

    def update_grid(self):
        """
        this will go through the current generation grid and update the inactive grid, so it will display it
        for the next generation

        """
        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1, 0, 1, -1, 1, -1, 0, 1]

        for r in range(self.rows):
            for c in range(self.columns):
                life = dead = 0
                for i in range(8):
                    # this was we consider the end of each edge is the start of the opposite edge
                    nc = (c + dy[i]) % self.columns
                    nr = (r + dx[i]) % self.rows

                    if self.active_grid[nr][nc]:
                        life += 1
                    else:
                        dead += 1
                if self.active_grid[r][c]:
                    # Apply life cell rules
                    if life == 2 or life == 3:
                        self.inactive_grid[r][c] = 1
                    else:
                        self.inactive_grid[r][c] = 0

                else:
                    # Apply dead Cell rules
                    if life == 3:
                        self.inactive_grid[r][c] = 1
                    else:
                        self.inactive_grid[r][c] = 0

        # deep copy == copy by value not refrence
        self.active_grid = copy.deepcopy(self.inactive_grid)

    def draw_grid(self):
        """
        This one draws the circles that form the shapes on screen
        it draws this according to the active_grid matrix
        """
        self.clear_screen()
        for r in range(self.rows):
            for c in range(self.columns):
                if self.active_grid[r][c]:
                    pygame.draw.circle(self.screen, self.alive_color,
                                       (c * self.cell_size + self.cell_size / 2,
                                        r * self.cell_size + self.cell_size / 2), self.cell_size / 2, 0)
        pygame.display.flip()

    def handle_events(self):
        """
        This one handles the events
        * if event is keypress 's', then toggle game pause
        * if event is keypress 'r', then randomize grid
        * if event is keypress 'q', then quit game
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.unicode == 's':
                if self.paused:
                    self.paused = False
                else:
                    self.paused = True

        if pygame.key.get_pressed()[pygame.K_q]:
            sys.exit()
        elif pygame.key.get_pressed()[pygame.K_r]:
            self.randomize_grid()

        # can't be used with toggling, as your press on the key may toggle it several time,
        # and the probability with toggling it even times so it would be like it didn't toggle
        # using the KEYDOWN event like above is the way to do it

        # elif pygame.key.get_pressed()[pygame.K_s]:
        #     print('paused')
        #     if self.paused:
        #         self.paused=0
        #     else:
        #         self.paused=1

    def run(self):
        """
        THis is the main game loop
        first we display the grid then listen of events
        then we update the grid for the next generation
        lastly, we draw the next generation
        """
        pygame.display.flip()
        while True:
            self.handle_events()

            if self.paused:
                continue

            self.update_grid()
            self.draw_grid()
            self.cap_frame_rate()

    def cap_frame_rate(self):
        """
        It adjusts the screen refresh rate according to the max_fps
        It also insures that we wait desired_wait_time before updates again
        """
        desired_wait_time = (1.0 / self.max_fps) * 1000
        now = pygame.time.get_ticks()
        time_since_last_update = now - self.last_time_updated
        time_to_wait = int(desired_wait_time - time_since_last_update)
        if time_to_wait > 0:
            pygame.time.delay(time_to_wait)
        self.last_time_updated = now
