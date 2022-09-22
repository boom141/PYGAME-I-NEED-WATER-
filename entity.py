import pygame, os
from effects_particles import*
from sprite_groups import*
from pygame.locals import *
pygame.init()


class Player(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('animation/player-idle', 'player_idle_right0.png'))
		self.image_copy = self.image
		self.rect = self.image.get_rect(x=position[0], y=position[1])
		self.hit_box = pygame.Rect(self.rect.x,self.rect.y,50,50)
		self.frames = None
		self.frame_count = 0
		self.frame_speed = 0.2
		self.walk_direction = True
		self.landing = False
		self.double_jump = 0
		self.vertical_momentum = 0
		self.momentum_value = 0.5
		self.gravity = 0
		self.state = None
		self.scroll = [0,0]
		self.collision_types = {'top':False,'bottom':False,'right':False,'left':False} 
	
	def collision(self, tile_rects):
		hit_list = []
		for tile in tile_rects:
			if self.rect.colliderect(tile):
				hit_list.append(tile)
		return hit_list
	
	def update(self,delta_time,tile_rects,scroll):
		self.scroll = scroll
		player_move = [0,0]
		self.state = 'idle'
		if pygame.key.get_pressed()[K_d]:
			player_move[0] += 3 * delta_time
			self.walk_direction = False
		if pygame.key.get_pressed()[K_a]:
			player_move[0] -= 3 * delta_time
			self.walk_direction = True
		if pygame.key.get_pressed()[K_SPACE]:
			self.frame_speed = 0
			if self.collision_types['bottom']:
				self.frame_count = 0
				self.double_jump = 0
				self.vertical_momentum = -3
				self.landing = True
			
			elif self.vertical_momentum > 0 and self.double_jump == 0:
				self.frame_count = 0
				self.double_jump = 1
				self.vertical_momentum = -4
				self.landing = True
				landing = Landing([self.rect.x - int(self.scroll[0]),self.rect.y - int(scroll[1])],'animation/landing',[20,-15])
				effects.add(landing)

# player gravity ------------------------------------------------------#
		player_move[1] += self.gravity
		if self.collision_types['bottom']:
			self.gravity = self.vertical_momentum
		else:
			self.gravity = self.vertical_momentum * delta_time
		self.vertical_momentum += self.momentum_value

# player jump ---------------------------------------------------------#
		if self.collision_types['bottom'] == False:
			self.state = 'jump'
			self.momentum_value = 0.5

# player walk ---------------------------------------------------------#
		if self.collision_types['bottom']:
			self.momentum_value = 0
			if player_move[0] != 0: 
				self.state = 'walk'

# player collision ----------------------------------------------------#
		self.collision_types = {'top':False,'bottom':False,'right':False,'left':False} 
		self.rect.x += int(player_move[0] )
		hit_list = self.collision(tile_rects)
		for tile in hit_list:
			if player_move[0] > 0:
				self.rect.right = tile.left
			elif player_move[0] < 0:
				self.rect.left = tile.right
		self.rect.y += int(player_move[1])
		hit_list = self.collision(tile_rects)
		for tile in hit_list:
			if player_move[1] > 0:
				self.rect.bottom = tile.top
				self.collision_types['bottom'] = True
			elif player_move[1]  < 0:
				self.rect.top = tile.bottom
		
# player animation ----------------------------------------------------#
		self.frames = os.listdir(f'animation/player-{self.state}')
		self.frame_count += self.frame_speed * delta_time
		if self.frame_count >= (len(self.frames) - 1):
			if self.vertical_momentum > 0 and self.state == 'jump':
				self.frame_count = (len(self.frames)-1)
			else:
				self.frame_count = 0

		if self.vertical_momentum > 0:
			self.frame_speed = 0.2
			

		self.image = pygame.image.load(os.path.join(f'animation/player-{self.state}', self.frames[int(self.frame_count)])).convert()
		self.image_copy = pygame.transform.flip(self.image, self.walk_direction, False)
		self.image_copy.set_colorkey((0,0,0))

# landing effect ------------------------------------------------------#
		if self.landing and self.collision_types['bottom']:
			landing = Landing([self.rect.x - int(self.scroll[0]),self.rect.y - int(scroll[1])],'animation/landing',[20,-15])
			effects.add(landing)
			self.landing = False
	
	def draw(self,surface):
		#pygame.draw.rect(surface, 'green', (self.rect.x- int(scroll[0]),self.rect.y - int(scroll[1]),self.image.get_width(),self.image.get_height()),1)
		surface.blit(self.image_copy, (self.rect.x - int(self.scroll[0]),self.rect.y + 3 - int(self.scroll[1])))
		

class Meter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.water_meter = pygame.image.load(os.path.join('misc', 'water_meter.png')).convert()
		self.image1 = pygame.transform.scale(self.water_meter,(105,15))
		self.image1.set_colorkey((0,0,0))
		self.rect = pygame.Rect(5,5,self.image1.get_width(),self.image1.get_height()-2)
		self.color = ((56,136,156))
		self.delay = 10
		self.seconds = 0
		self.reset = 30
		self.decrease_value = 0.1

	def update(self,dt):
		if self.decrease_value > 0.1:
			self.reset -= 1

		if self.seconds >= self.delay:
			self.rect.width -= self.decrease_value * dt
			self.seconds = 0

		if self.reset <= 0:
			self.reset = 30
			self.decrease_value = 0.1	

		self.seconds += 0.5 * dt
		
	def draw(self,surface):
		pygame.draw.rect(surface, self.color, self.rect)
		surface.blit(self.image1,(5,3))