import pygame, os, random
from sprite_groups import*
from effects_particles import*

class Static_Animation(pygame.sprite.Sprite):
	def __init__(self, position, path ,scroll):
		pygame.sprite.Sprite.__init__(self)
		self.path = path
		self.frames = os.listdir(self.path)
		self.frame_count = 0
		self.position = position
		self.scroll = scroll
		self.rect = pygame.Rect(position[0],position[1], 20,30)
	
	def droplet_collision(self,player_rect,game_data,meter,color):
		if player_rect.colliderect(self.rect):
			meter.rect.width += 5
			pulse1 = Pulse_Ease_Out([player_rect.centerx - int(self.scroll[0]),player_rect.centery - int(self.scroll[1])],[5,4,80],((225,225,225)),True)
			pulse2 = Pulse_Ease_Out([player_rect.centerx - int(self.scroll[0]),player_rect.centery - int(self.scroll[1])],[4,2,80],((4,174,184)),True)
			effects.add(pulse1,pulse2)  
			for i in range(50):
				disperse = Static_Particle([self.rect.x - int(self.scroll[0]),self.rect.y - int(self.scroll[1])],[random.randrange(-5,5),
				random.randrange(-4,4)],[random.randint(4,5),0,0.1,0,color[random.randint(0,2)]],[0,game_data.tile_map,game_data.tile_size,10])
				particles.add(disperse)      
			self.kill()

	def update(self,delta_time):    
		self.frame_count += 0.2 * delta_time
		if self.frame_count >= (len(self.frames) - 1):
			self.frame_count = 0

	def draw(self,surface):
		#pygame.draw.rect(surface, 'green', (self.rect.x - int(self.scroll[0]),self.rect.y - int(self.scroll[1]),20,30), 1)
		if self.frame_count <= (len(self.frames) - 1):
			image = pygame.image.load(os.path.join(self.path, self.frames[int(self.frame_count)])).convert()
			image.set_colorkey((0,0,0))
			surface.blit(image, (self.position[0] - int(self.scroll[0]),self.position[1] - int(self.scroll[1])))

