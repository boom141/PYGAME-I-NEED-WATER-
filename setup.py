import pygame, sys, time
from pygame.locals import *
pygame.init() # initiates pygam\

clock = pygame.time.Clock() # initialize fps

fps = 60

pygame.display.set_caption('Pygame: I NEED WATER!') # initialize game title

WINDOW_SIZE = (500,500) # initialize window size

window = pygame.display.set_mode(WINDOW_SIZE,0,24) # initiate the window

display = pygame.Surface((250,250)) # used as the surface for rendering, which is scaled

last_time = time.time() # initialize delta time

