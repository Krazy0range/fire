from random import randint
import time
import os

BLACK = '\033[40m'
GRAY = '\033[48;5;235m'
WHITE = '\033[48;5;237m'
FIRE0 = '\033[48;5;25m'
BRIGHT_FIRE0 = '\033[48;5;27m'
FIRE1 = '\033[48;5;208m'
BRIGHT_FIRE1 = '\033[48;5;214m'
FIRE2 = '\033[48;5;1m'
BRIGHT_FIRE2 = '\033[48;5;196m'
RESET = '\033[0m'

TILING = 1
terminal_dimensions = os.get_terminal_size()
WIDTH_DIVISOR = 1.5
HEIGHT_DIVISOR = 1.5
GRID_WIDTH = int(terminal_dimensions[0] // (2 * TILING) // WIDTH_DIVISOR)
GRID_HEIGHT = int(terminal_dimensions[1] // HEIGHT_DIVISOR) - 2
_new_grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
NUM_PARTICLES = 250
PARTICLES_DELETION_RATE = 1
TRAIL_LENGTH = 20
FURROW_LENGTH = 50

def new_grid():
  return _new_grid.copy()


def new_particle():
  x = randint(0, GRID_WIDTH - 1)
  y = GRID_HEIGHT 
#   y = randint(0, GRID_HEIGHT - 1)
  c = 0
  return (x, y, c)


def new_particles():
  particles = []
  for _ in range(NUM_PARTICLES):
    particle = new_particle()
    particles.append(particle)
  return particles


def new_trails(particles):
  return [[] for _ in particles]

def new_furrows(particles):
    return [[] for _ in particles]

def check_position(position):
  _position = position.copy()
  if _position[0] < 0:
    _position[0] = GRID_WIDTH - 1
  if _position[0] > GRID_WIDTH - 1:
    _position[0] = 0
  if _position[1] < 0:
    _position[1] = GRID_HEIGHT - 1
  if _position[1] > GRID_HEIGHT - 1:
    _position[1] = 0

  return _position


def print_grid(grid):
    for y in range(GRID_HEIGHT):
        for _ in range(TILING):
            for x in range(GRID_WIDTH):
                print(f'{grid[y][x]}  {RESET}', end='')
        print()
    print('\033[H\033[A')


def set_grid_block(grid, x, y, color):
    for _x in range(x - 1, x + 2):
        for _y in range(y - 1, y + 2):
            if _y >= 0 and _y < GRID_HEIGHT and _x >= 0 and _x < GRID_WIDTH:
                grid[_y][_x] = color
    return grid


def render(particles, trails, furrows):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Render furrows
    for furrow in furrows:
        for position in furrow:
            x, y, c = position
            grid = set_grid_block(grid, x, y, GRAY)

    # Render trails
    for trail in trails:
        for index, position in enumerate(trail):
            x, y, c = position
            color = BLACK
            if index == 1:
                if c == 0:
                    color = BRIGHT_FIRE0
                elif c == 1:
                    color = BRIGHT_FIRE1
                elif c == 2:
                    color = BRIGHT_FIRE2
            elif index <= TRAIL_LENGTH // 2:
                if c == 0:
                    color = FIRE0
                elif c == 1:
                    color = FIRE1
                elif c == 2:
                    color = FIRE2
            elif index <= TRAIL_LENGTH:
                color = WHITE

            # if color == WHITE:
            #     grid = set_grid_block(grid, x, y, color)
            # else:
            grid[y][x] = color

    # Render particles
    for particle in particles:
        x, y, c = particle
        color = BLACK
        if c == 0:
            color = BRIGHT_FIRE0
        elif c == 1:
            color = BRIGHT_FIRE1
        elif c == 2:
            color = BRIGHT_FIRE2
        grid[y][x] = color

    # Render grid
    print_grid(grid)


def update(particles, trails, furrows):
    for _ in range(PARTICLES_DELETION_RATE):
        del particles[len(particles) - 1]
        particles.insert(0, new_particle())
    
    # Update particle positions
    for index, particle in enumerate(particles):
        x, y, c = particle
        _x = x + randint(-1, 1)
        _y = y - 1
        _x, _y = check_position([_x, _y])
        if randint(0, _y) < 3:
            _y = GRID_HEIGHT - 1
            c = 0
        if c == 0 and randint(0, _y) < 15:
            c = 1
        if c == 1 and randint(0, _y) < 5:
            c = 2
        particles[index] = (_x, _y, c)

    # Update trails
    for index in range(len(particles)):
        particle = particles[index]
        trail = trails[index]
        furrow = furrows[index]
        trail.insert(0, particle)
        if len(trail) > TRAIL_LENGTH:
            last = trail.pop(len(trail) - 1)
            furrow.insert(0, last)

    # # Update furrows
    for index in range(len(particles)):
        furrow = furrows[index]
        if len(furrow) > FURROW_LENGTH:
            furrow.pop(len(furrow) - 1)

    return particles, trails, furrows


particles = new_particles()
trails = new_trails(particles)
furrows = new_furrows(particles)

os.system('clear')

# for _ in range(TRAIL_LENGTH):
#     particles, trails = update(particles, trails)
    
os.system('clear')

while True:
  particles, trails, furrows = update(particles, trails, furrows)
  render(particles, trails, furrows)
  time.sleep(0.1)