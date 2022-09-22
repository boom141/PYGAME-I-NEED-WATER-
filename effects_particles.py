import pygame,os


class Pulse_Ease_Out(pygame.sprite.Sprite):
	def __init__(self,position,option,color,value):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.radius = 0
		self.radius_value = option[0]
		self.width = option[1]
		self.duration = option[2]
		self.color = color
		self.play_animation = value

	def update(self,dt):
		if self.play_animation:
			if self.radius > self.duration - 20:
				self.radius_value = 0.5

		self.radius += self.radius_value * dt
		if self.radius > self.duration:
			self.kill()

	def draw(self,surface):
		pygame.draw.circle(surface, self.color,(self.position[0],self.position[1]),int(self.radius),self.width)

class Static_Particle(pygame.sprite.Sprite):
	def __init__(self,position,direction,options,physics): # options are [duration,gravity,seconds,width,color], physics are [bounce,tile_map,tile_size]
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.direction = direction
		self.options = options
		self.physics = physics
		self.gravity = 0
	def update(self,dt): 
			self.position[0] += self.direction[0] * dt
			loc_str = f'{int(self.position[0] / self.physics[2])}:{int(self.position[1] / self.physics[2])}'
			if self.physics[0] > 0:
				if loc_str in self.physics[1]:
					self.direction[0] = -self.physics[0] * self.direction[0]
					self.direction[1] *= 0.95
					self.position[0] += self.direction[0] * 2
			self.position[1] += self.direction[1] * dt
			loc_str = f'{int(self.position[0] / self.physics[2])}:{int(self.position[1] / self.physics[2])}'
			if self.physics[0] > 0:
				if loc_str in self.physics[1]:
					self.direction[1] = -self.physics[0] * self.direction[1]
					self.direction[0] *= 0.95
					self.position[1] += self.direction[1] * 2
			self.options[0] -= self.options[2]
			self.direction[1] += self.gravity
			self.gravity += self.options[1]
			if self.options[0] <= 0:
				self.kill()
	
	def draw(self,surface):
		pygame.draw.circle(surface, self.options[4], [self.position[0], self.position[1] + self.physics[3]], self.options[0], self.options[3])



class Landing(pygame.sprite.Sprite):
    def __init__(self, position, path, offset):
        pygame.sprite.Sprite.__init__(self)
        self.path = path
        self.frames = os.listdir(self.path)
        self.frame_count = 0
        self.position = position
        self.offset = offset

    def update(self,delta_time):    
        self.frame_count += 0.2 * delta_time
        if self.frame_count >= (len(self.frames) - 1):
            self.kill()

    def draw(self,surface):
        if self.frame_count <= (len(self.frames) - 1):
            image = pygame.image.load(os.path.join(self.path, self.frames[int(self.frame_count)])).convert()
            image_copy = image.copy()
            image_copy = pygame.transform.scale(image,(90,30))
            image_copy.set_colorkey((0,0,0))
            surface.blit(image_copy, (self.position[0] - self.offset[0],self.position[1] - self.offset[1]))
