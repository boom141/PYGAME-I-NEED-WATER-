import os
from setup import*
from map_loader import*



class Game_Data:
	def __init__(self):
		self.map_data = map_loader.Load('map0.json')
		self.tile_size = 16
		self.tile_map = {}
		self.tile_rects = []
		self.spawn_point = [400,200]
		self.scroll = [0,0]

	def Render(self,key,surface):
		for list in self.map_data[key]: 
			for data in list:
				if data != [-1]:
					image = pygame.image.load(os.path.join(f'environment/{data[1]}', data[2]))
					image.set_colorkey((0,0,0))
					surface.blit(image, (data[3] - self.spawn_point[0],data[4] - self.spawn_point[1]))
					self.tile_rects.append(pygame.Rect(data[3] - self.spawn_point[0],data[4] - self.spawn_point[1],self.tile_size,self.tile_size))

game_data = Game_Data()

while True: # game loop
# framerate independence -------------------------------------------------#
	delta_time = time.time() - last_time
	delta_time *= 60
	last_time = time.time()
# fill the screen --------------------------------------------------------#  
	display.fill((25,25,25))

#draw map ----------------------------------------------------------------#
	for key in game_data.map_data:
		if key != 'ENTITY':
			game_data.Render(key,display)

	for event in pygame.event.get(): # event loop
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	
	window.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
	pygame.display.update()
	clock.tick(60)
