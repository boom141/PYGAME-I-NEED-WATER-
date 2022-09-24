import pygame, os, random
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
		self.double_jump = -1
		self.vertical_momentum = 0
		self.momentum_value = 0.3
		self.free_fall = 0
		self.state = None
		self.scroll = [0,0]

	def collision(self,tile_rects):
# player collision ----------------------------------------------------#
		hit_list = []
		for tile in tile_rects:
			if self.rect.colliderect(tile):
				hit_list.append(tile)
		return hit_list
	

	def player_movement(self,move,tile_rects):
# player movement ----------------------------------------------------#
		collision_types = {'top':False,'bottom':False,'right':False,'left':False} 
		self.rect.x += move[0]
		hit_list = self.collision(tile_rects)
		for tile in hit_list:
			if move[0] > 0:
				self.rect.right = tile.left
			elif move[0] < 0:
				self.rect.left = tile.right
		self.rect.y += move[1]
		hit_list = self.collision(tile_rects)
		for tile in hit_list:
			if move[1] > 0:
				self.rect.bottom = tile.top
				collision_types['bottom'] = True
			elif move[1]  < 0:
				self.rect.top = tile.bottom
		
		return collision_types

	def update(self,delta_time,tile_rects,scroll):
		self.scroll = scroll
# player controller ------------------------------------------------------#
		player_move = [0,0]
		if pygame.key.get_pressed()[K_d]:
			player_move[0] += 3 * delta_time
			self.walk_direction = False
		if pygame.key.get_pressed()[K_a]:
			player_move[0] -= 3 * delta_time
			self.walk_direction = True
		if pygame.key.get_pressed()[K_SPACE]:
			if self.free_fall < 6:
				self.vertical_momentum = -2.5
				self.double_jump = 0 
			elif self.free_fall > 0 and self.double_jump == 0:
				self.vertical_momentum = -3
				self.double_jump = 1

# player states -------------------------------------------------------#
		self.state = 'idle'
		if self.free_fall > 2:
			self.state = 'jump'
		elif player_move[0] > 0 or player_move[0] < 0:
			self.state = 'walk'
		
# player gravity ------------------------------------------------------#
		player_move[1] += self.vertical_momentum * delta_time
		self.vertical_momentum += self.momentum_value
		if self.vertical_momentum > 3:
			self.vertical_momentum = 3

# collision state ------------------------------------------------------#
		collisions = self.player_movement(player_move,tile_rects)

		if collisions['bottom']:
			self.free_fall = 0
			self.vertical_momentum = 0
			self.double_jump = -1
		else:
			self.free_fall += 1

# player animation ----------------------------------------------------#
		self.frames = os.listdir(f'animation/player-{self.state}')
		self.frame_count += self.frame_speed * delta_time
		if self.frame_count >= (len(self.frames) - 1):
			if self.state == 'jump':
				self.frame_count = (len(self.frames) - 1)
			else:
				self.frame_count = 0

		if self.vertical_momentum < 0:
			self.frame_count = 0
			
		self.image = pygame.image.load(os.path.join(f'animation/player-{self.state}', self.frames[int(self.frame_count)])).convert()
		self.image_copy = pygame.transform.flip(self.image, self.walk_direction, False)
		self.image_copy = pygame.transform.scale(self.image_copy, (40,30))
		self.image_copy.set_colorkey((0,0,0))

# landing effect ------------------------------------------------------#
		# if self.landing and self.collision_types['bottom']:
		# 	landing = Landing([self.rect.x - self.scroll[0],self.rect.y - self.scroll[1]],'animation/landing',[20,-15])
		# 	effects.add(landing)
		# 	self.landing = False
	
	def draw(self,surface):
		#pygame.draw.rect(surface, 'green', (self.rect.x- int(scroll[0]),self.rect.y - int(scroll[1]),self.image.get_width(),self.image.get_height()),1)
		surface.blit(self.image_copy, (self.rect.x - self.scroll[0],self.rect.y + 3 - self.scroll[1]))


class Enemy(pygame.sprite.Sprite):
	def __init__(self,position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('animation/enemy-idle', 'idle_left0.png'))
		self.image_copy = self.image
		self.rect = self.image.get_rect(x=position[0], y=position[1])
		self.border = pygame.Rect(self.rect.x - 16,self.rect.y,64,self.image_copy.get_height())
		self.frames = None
		self.frame_count = 0
		self.walk_countdown = 0
		self.idle_countdown = 0
		self.idling = False
		self.walk_direction = True
		self.vertical_momentum = 0
		self.state = None
	

	def collision_test(self,enemy_rect,tile_rects):
		hit_list = []
		for tile in tile_rects:
			if tile.colliderect(enemy_rect):
				hit_list.append(tile)
		return hit_list
	
	def move(self,delta_time,game_data):
# enemy movements and state  ---------------------------------------------------------------------#	
		if self.idling == False and random.randint(1,200) == 1:
			self.idling = True
			self.idle_countdown = 50

		move = [0,0]
		if self.idling == False: 
			if self.walk_direction:
				move[0] += 0.5 * delta_time
			else:
				move[0] -= 0.5 * delta_time
			move[1] += self.vertical_momentum * delta_time
			self.vertical_momentum += 0.3
			if self.vertical_momentum > 3:
				self.vertical_momentum = 3

			if move[0] > 0 or move[0] < 0:
				self.state = 'walk'
				self.walk_countdown += 1

		else:
			self.idle_countdown -= 1
			self.state = 'idle'
		
		if self.idle_countdown <= 0:
			self.idling = False

# enemy collsision ---------------------------------------------------------------------#
		collision_types = {'top':False,'bottom':False,'right':False,'left':False} 
		self.rect.x += move[0]
		self.rect.y += move[1]
		hit_list = self.collision_test(self.rect,game_data.tile_rects)
		for tile in hit_list:
			if move[1] > 0:
				self.rect.bottom = tile.top
				collision_types['bottom'] = True
			elif move[1] < 0:
				self.rect.top = tile.bottom

		if self.rect.right > self.border.right:
			self.walk_direction = False
		if self.rect.left < self.border.left:
			self.walk_direction = True

		if collision_types['bottom']:
			self.vertical_momentum = 0

	def update(self,delta_time,game_data):

		self.move(delta_time,game_data)

		self.frames = os.listdir(f'animation/enemy-{self.state}')
		self.frame_count += 0.2 * delta_time
		if self.frame_count >= (len(self.frames) - 1):
			self.frame_count = 0
		
		if self.frame_count <= (len(self.frames) - 1):
			self.image = pygame.image.load(os.path.join(f'animation/enemy-{self.state}', self.frames[int(self.frame_count)]))
			self.image_copy = self.image.copy()
			self.image_copy = pygame.transform.flip(self.image, self.walk_direction, False)
			self.image_copy = pygame.transform.scale(self.image_copy, (45,30))
			self.image_copy.set_colorkey((0,0,0))

	def draw(self,surface,scroll):
		surface.blit(self.image_copy, (self.rect.x - scroll[0],self.rect.y + 6 - scroll[1]))
		# pygame.draw.rect(surface, 'green',(self.rect.x - scroll[0],self.rect.y + 6 - scroll[1], self.image_copy.get_width(), self.image_copy.get_height()), 1)

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
