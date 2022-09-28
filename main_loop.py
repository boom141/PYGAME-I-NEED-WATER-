import os
from setup import*
from map_loader import*
from sprite_groups import*
from static_animation import*
from entity import*
from sprite_groups import*


class Game_Data:
	def __init__(self):
		self.tile_size = 16
		self.tile_map = {}
		self.tile_rects = []
		self.spawn_point = map_loader.spawn_point
		self.true_scroll = [0,0]
		self.scroll = [0,0]
		self.image1 = pygame.image.load(os.path.join('bg_image/bg_first_layer.png')).convert()
		self.image2 = pygame.image.load(os.path.join('bg_image/bg_second_layer.png')).convert()
		self.image3 = pygame.image.load(os.path.join('bg_image/bg_third_layer.png')).convert()
	
	
	def Render_Background(self,surface):
		self.img3_copy = self.image3.copy()
		self.img3_copy.set_colorkey((0,0,0))
		surface.blit(self.img3_copy, ((map_loader.edges[0] - self.scroll[0]) / 3.5, map_loader.edges[2] + 20 - self.scroll[1]))
		self.img2_copy = self.image2.copy()
		self.img2_copy.set_colorkey((0,0,0))
		surface.blit(self.img2_copy, ((map_loader.edges[0] - self.scroll[0]) / 3, map_loader.edges[2] + 20 - self.scroll[1]))
		self.img1_copy = self.image1.copy()
		self.img1_copy.set_colorkey((0,0,0))
		surface.blit(self.img1_copy, ((map_loader.edges[0] - 100 - self.scroll[0]) / 2, map_loader.edges[2] + 30 - self.scroll[1]))
	
	
	def Render(self,surface):
		self.tile_map = {}
		self.tile_rects = []
		for data in map_loader.tiles:
			image = pygame.image.load(os.path.join(f'environment/{data[1]}', data[2])).convert()
			image.set_colorkey((0,0,0))
			rect = surface.blit(image, (data[3] - self.scroll[0],data[4] - self.scroll[1]))
			if data[1] != 'decoration':
				self.tile_rects.append(pygame.Rect(data[3],data[4],self.tile_size,self.tile_size))
				self.tile_map[f'{int(rect.x / self.tile_size)}:{int(rect.y / self.tile_size)}'] = 0
	def Render_Entity(self):
		for entity in map_loader.entities:
			if entity[1] == 'foliage':
				tree = Static_Animation([entity[3],entity[4]], 'animation/half-tree')
				foliage.add(tree)
			if entity[1] == 'entity' and entity[2] == '2.png':
				collectible = Static_Animation([entity[3],entity[4]], 'animation/droplet')
				collectibles.add(collectible)
			if entity[1] == 'entity' and entity[2] == '1.png':
				enemy = Enemy([entity[3],entity[4]])
				enemies.add(enemy)
	

map_loader.Load('map1.json')
game_data = Game_Data()
game_data.Render_Entity()
player = Player([game_data.spawn_point[0],game_data.spawn_point[1] - 30])
meter = Meter()

while 1: # game loop
# framerate independence -------------------------------------------------#
	delta_time = time.time() - last_time
	delta_time *= fps
	last_time = time.time()

# fill the screen --------------------------------------------------------#  
	display.fill((25, 25, 25))

# camera ----------------------------------------------------------------#
	game_data.true_scroll[0] += (player.rect.x-game_data.scroll[0]-128)/3# divide 20 is for fancy moving of camera position
	game_data.true_scroll[1] += (player.rect.y-game_data.scroll[1]-115)/3
	game_data.scroll = game_data.true_scroll.copy()
	game_data.scroll[0] = int(game_data.true_scroll[0])
	game_data.scroll[1] = int(game_data.true_scroll[1])
	

# map edeges ------------------------------------------------------------#
	if player.rect.left < 320:
		player.rect.left = 320
	if player.rect.right > 860:
		player.rect.right = 860

	if game_data.true_scroll[0] < 348:
		game_data.true_scroll[0] = 348
	if game_data.true_scroll[0] > 590:
		game_data.true_scroll[0] = 590
	if game_data.true_scroll[1] < map_loader.edges[2]:
		game_data.true_scroll[1] = map_loader.edges[2]
	


# render map ----------------------------------------------------------------#
	game_data.Render_Background(display)

	for tree in foliage:
		tree.update(delta_time)
		tree.draw(display,game_data.scroll)

	game_data.Render(display) 

# render entity -------------------------------------------------------------# 	
	player.update(delta_time, game_data.tile_rects, game_data.scroll)
	player.draw(display)

	for enemy in enemies:
		enemy.update(delta_time,game_data,player)
		enemy.draw(display,game_data.scroll)

# render collectibles -------------------------------------------------------#
	for collectible in collectibles:
		collectible.droplet_collision(player.rect,game_data,meter,[(255,255,255),(4,174,184),(56,136,156)])
		collectible.update(delta_time)
		collectible.draw(display,game_data.scroll)

# render effects and particles ----------------------------------------------#
	for effect in effects:
		effect.update(delta_time)
		effect.draw(display)
	
	for particle in particles:
		particle.update(delta_time)
		particle.draw(display)

	for projectile in projectiles:
		projectile.update(delta_time)
		projectile.draw(display)
		projectile.collision(player,meter)

# render meter --------------------------------------------------------------#
	meter.update(delta_time)
	meter.draw(display)

	for event in pygame.event.get(): # event loop
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	
	window.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
	pygame.display.update()
	clock.tick(fps)
