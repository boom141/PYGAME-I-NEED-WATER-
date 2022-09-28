import os, random
from setup import*
from effects_particles import*
from sprite_groups import*
from sound_music import*

class Player(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('animation/player-idle', 'player_idle_right0.png'))
		self.image_copy = self.image
		self.rect = self.image.get_rect(x=position[0], y=position[1])
		self.hit_box = None
		self.frames = None
		self.frame_count = 0
		self.frame_speed = 0.2
		self.walk_direction = True
		self.landing = False
		self.landing_value = -1
		self.hit = False
		self.double_jump = -1
		self.vertical_momentum = 0
		self.horizontal_momentum = 0
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
			if self.free_fall < 6 and self.double_jump == -1:
				Sfx_Sound('sfx/jump.wav').play_sound(0)
				pulse = Pulse_Ease_Out([self.rect.centerx - scroll[0], self.rect.centery + 10 - scroll[1]],[5,1,20],((255,255,255)),True)
				effects.add(pulse)
				self.vertical_momentum = -2.5
				self.double_jump = 0 
			elif self.free_fall > 6 and self.double_jump == 0:
				Sfx_Sound('sfx/jump.wav').play_sound(0)
				pulse = Pulse_Ease_Out([self.rect.centerx - scroll[0], self.rect.centery + 10 - scroll[1]],[5,1,20],((255,255,255)),True)
				effects.add(pulse)
				self.vertical_momentum = -3
				self.double_jump = 1

# player states -------------------------------------------------------#
		if self.hit == False:
			self.state = 'idle'
			if self.free_fall > 2:
				self.state = 'jump'
			elif player_move[0] > 0 or player_move[0] < 0:
				self.state = 'walk'
		else:
			self.state = 'hit-jump' # more room to improve
	
# player gravity ------------------------------------------------------#
		player_move[0] += self.horizontal_momentum 
		player_move[1] += self.vertical_momentum * delta_time
		self.vertical_momentum += self.momentum_value
		if self.vertical_momentum > 3:
			self.vertical_momentum = 3

# collision state ------------------------------------------------------#
		collisions = self.player_movement(player_move,tile_rects)
		
		self.hit_box = self.rect.copy()
		self.hit_box.width = 10
		self.hit_box.x = self.hit_box.x + 15

		if collisions['bottom']:
			self.free_fall = 0
			self.vertical_momentum = 0
			self.horizontal_momentum = 0
			self.double_jump = -1
		else:
			self.free_fall += 1

		if self.free_fall > 1:
			self.landing = True

# player animation ----------------------------------------------------#
		self.frames = os.listdir(f'animation/player-{self.state}')
		self.frame_count += self.frame_speed * delta_time
		if self.frame_count >= (len(self.frames) - 1):
			self.hit = False
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
		if collisions['bottom'] and self.landing:
			Sfx_Sound('sfx/landing.wav').play_sound(0)
			landing = Landing([self.rect.x - self.scroll[0],self.rect.y - self.scroll[1]],'animation/landing',[20,-15])
			effects.add(landing)
			self.landing = False
	
	def draw(self,surface):
		# pygame.draw.rect(surface, 'green', (self.hit_box.x- self.scroll[0],self.hit_box.y - self.scroll[1],self.hit_box.width,self.hit_box.height),1)
		surface.blit(self.image_copy, (self.rect.x - self.scroll[0],self.rect.y + 3 - self.scroll[1]))


class Enemy(pygame.sprite.Sprite):
	def __init__(self,position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('animation/enemy-idle', 'idle_left0.png'))
		self.image_copy = self.image
		self.rect = self.image.get_rect(x=position[0], y=position[1])
		self.border = pygame.Rect(self.rect.x - 16,self.rect.y,64,self.image_copy.get_height())
		self.hit_box = None
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

	def shoot(self,player,game_data):
		if self.hit_box.colliderect(player.hit_box):
			self.state = 'attack'
			
			if player.rect.right > self.hit_box.left and player.rect.right > self.hit_box.right:
				self.walk_direction = True
			elif player.rect.right > self.hit_box.left:
				self.walk_direction = False

			if self.frame_count == 0:
				sounds = [Sfx_Sound('sfx/player_hit.wav'),Sfx_Sound('sfx/enemy_attack.wav')]
				for sound in sounds:
					sound.play_sound(0)
				projectile = Projectile([self.rect.centerx - game_data.scroll[0],self.rect.centery - game_data.scroll[1]],
				[4,-2] if self.walk_direction else [-4,-2],game_data,0.1,3)
				projectiles.add(projectile)

			

	def move(self,delta_time,game_data,player):
# enemy movement and state -----------------------------------------------------------------#	
		if self.idling == False and random.randint(1,200) == 1 and self.state != 'attack':
			self.idling = True
			self.idle_countdown = 50

		move = [0,0]
		if self.idling == False and self.state != 'attack': 
			if self.walk_direction:
				move[0] += 0.5 * delta_time
			else:
				move[0] -= 0.5 * delta_time
			

			if move[0] > 0 or move[0] < 0:
				self.state = 'walk'
				self.walk_countdown += 1

		else:
			self.idle_countdown -= 1
			self.state = 'idle'
		
		if self.idle_countdown <= 0:
			self.idling = False

		move[1] += self.vertical_momentum * delta_time
		self.vertical_momentum += 0.3
		if self.vertical_momentum > 3:
			self.vertical_momentum = 3
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

# enemy border -------------------------------------------------------------------------#
		self.rect.width = 30
		if self.rect.right > self.border.right:
			self.walk_direction = False
		if self.rect.left < self.border.left:
			self.walk_direction = True

# hit box ------------------------------------------------------------------------------#
		self.hit_box = self.rect.copy()
		self.hit_box.x = self.rect.x - 25
		self.hit_box.y = self.rect.y
		self.hit_box.width = 100

		self.shoot(player,game_data)
		
		if collision_types['bottom']:
			self.vertical_momentum = 0

	def update(self,delta_time,game_data,player):

		self.move(delta_time,game_data,player)

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
		surface.blit(self.image_copy, (self.rect.x - scroll[0],self.rect.y - 10 - scroll[1]))
		#pygame.draw.rect(surface, 'green',(self.hit_box.x - scroll[0],self.hit_box.y + 6 - scroll[1], self.hit_box.width, self.image_copy.get_height()), 1)

class Meter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.water_meter = pygame.image.load(os.path.join('misc', 'water_meter.png')).convert()
		self.image1 = pygame.transform.scale(self.water_meter,(105,15))
		self.image1.set_colorkey((0,0,0))
		self.rect = pygame.Rect(7,5,self.image1.get_width()-2,self.image1.get_height()-2)
		self.color = ((56,136,156))
		self.delay = 10
		self.seconds = 0
		self.reset = 30
		self.decrease_value = 0.1

	def update(self,dt):

		if self.rect.width >= self.image1.get_width()-2:
			self.rect.width = self.image1.get_width()-2

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


class Projectile(pygame.sprite.Sprite):
	def __init__(self,position,direction,game_data,gravity_value,radius_value):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.direction = direction
		self.game_data = game_data
		self.gravity_value = gravity_value
		self.gravity = 0
		self.hit_box = None
		self.projectile = None
		self.radius_value = radius_value
		self.color = [(147,48,59),(31,14,28),(210,100,113)]

	def collision(self,player,meter):
		if player.hit_box.right > self.projectile.right:
			meter.rect.width -= 5
			player.hit = True
			player.vertical_momentum = -2
			player.horizontal_momentum = 2 if player.walk_direction else -2
			pulse1 = Pulse_Ease_Out([self.position[0], self.position[1]],[5,4,40],((31,14,28)),True)
			pulse2 = Pulse_Ease_Out([self.position[0], self.position[1]],[4,2,40],((245,237,186)),True)
			effects.add(pulse1,pulse2)
			for i in range(20):
				scatter = Static_Particle([self.position[0], self.position[1]],[random.randrange(-3,3),random.randrange(-3,3)],
				[random.randint(3,4),0,0.1,random.randint(0,1),self.color[random.randint(0,2)]],[0,self.game_data.tile_map,self.game_data.tile_size])
				effects.add(scatter)
			self.kill()
		elif self.position[1] > 800:
			self.kill()
	
	def update(self,delta_time):
		self.position[0] += self.direction[0] * delta_time
		self.position[1] += self.direction[1] 
		
		self.direction[1] += self.gravity * delta_time
		self.gravity += self.gravity_value
		
	def draw(self,surface):
		self.projectile = pygame.draw.circle(surface, self.color[random.randint(0,2)], (self.position[0],self.position[1]), self.radius_value)
		for i in range(30):
			trail = Static_Particle([self.projectile.centerx,self.projectile.centery],[0,0],[self.radius_value,0,0.5,0,self.color[random.randint(0,2)]],[0,self.game_data.tile_map,self.game_data.tile_size])
			effects.add(trail)