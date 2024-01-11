from random import randint
import time
import os

# TODO: ADD REPLIT GITIGNORE FILE

BLACK = '\033[40m'
GRAY = '\033[48;5;235m'
WHITE = '\033[48;5;245m'
FIRE0 = '\033[48;5;25m'
BRIGHT_FIRE0 = '\033[48;5;27m'
FIRE1 = '\033[48;5;208m'
BRIGHT_FIRE1 = '\033[48;5;214m'
FIRE2 = '\033[41m'
BRIGHT_FIRE2 = '\033[0;101m'
RESET = '\033[0m'

terminal_dimensions = os.get_terminal_size()
GRID_WIDTH = terminal_dimensions[0] // 4
GRID_HEIGHT = (terminal_dimensions[1] // 2) - 2
_new_grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
NUM_PARTICLES = 500
PARTICLES_DELETION_RATE = 1
TRAIL_LENGTH = 10
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
        for x in range(GRID_WIDTH):
            print(f'{grid[y][x]}  {RESET}', end='')
        print()
    print('\033[H\033[A')


def render(particles, trails, furrows):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Render furrows
    for furrow in furrows:
        for position in furrow:
            x, y, c = position
            grid[y][x] = GRAY

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

os.system('cls')

# for _ in range(TRAIL_LENGTH):
#     particles, trails = update(particles, trails)
    
os.system('cls')

while True:
  particles, trails, furrows = update(particles, trails, furrows)
  render(particles, trails, furrows)
  time.sleep(0.01)