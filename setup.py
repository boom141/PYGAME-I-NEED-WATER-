import pygame, sys, time
from pygame.locals import *
pygame.init() # initiates pygam\

clock = pygame.time.Clock() # initialize fps

pygame.display.set_caption('Pygame: I NEED WATER!') # initialize game title

WINDOW_SIZE = (500,500) # initialize window size

window = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((250,250)) # used as the surface for rendering, which is scaled

last_time = time.time() # initialize delta time

scroll = [0,0] # initialize camera