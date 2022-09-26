import pygame, os, random
from sprite_groups import*
from effects_particles import*

class Static_Animation(pygame.sprite.Sprite):
	def __init__(self, position, path ):
		pygame.sprite.Sprite.__init__(self)
		self.path = path
		self.frames = os.listdir(self.path)
		self.frame_count = 0
		self.position = position
		self.rect = pygame.Rect(position[0],position[1], 20,30)
	
	def droplet_collision(self,player_rect,game_data,meter,color):
		if player_rect.colliderect(self.rect):
			meter.rect.width += 10
			pulse1 = Pulse_Ease_Out([player_rect.centerx - game_data.scroll[0],player_rect.centery - game_data.scroll[1]],[5,4,60],((245,237,186)),True)
			pulse2 = Pulse_Ease_Out([player_rect.centerx - 3 - game_data.scroll[0],player_rect.centery - game_data.scroll[1]],[5,2,60],((52,133,157)),True)
			effects.add(pulse2,pulse1)  
			for i in range(80):
				disperse = Static_Particle([self.rect.x - game_data.scroll[0],self.rect.y - game_data.scroll[1]],[random.randrange(-5,9),
				random.randrange(-4,8)],[random.randint(4,6),0,0.3,random.randint(0,1),color[random.randint(0,2)]],[0,game_data.tile_map,game_data.tile_size,10])
				particles.add(disperse)      
			self.kill()

	def update(self,delta_time):    
		self.frame_count += 0.2 * delta_time
		if self.frame_count >= (len(self.frames) - 1):
			self.frame_count = 0

	def draw(self,surface,scroll):
		#pygame.draw.rect(surface, 'green', (self.rect.x - int(self.scroll[0]),self.rect.y - int(self.scroll[1]),20,30), 1)
		if self.frame_count <= (len(self.frames) - 1):
			image = pygame.image.load(os.path.join(self.path, self.frames[int(self.frame_count)])).convert()
			image.set_colorkey((0,0,0))
			surface.blit(image, (self.position[0] - scroll[0],self.position[1] - scroll[1]))

