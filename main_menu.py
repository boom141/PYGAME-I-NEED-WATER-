from setup import*
from game_loop import game_loop, level_transition


def draw_text(text,font,size,surface,position):
    font = pygame.font.Font(f'fonts/{font}', size)
    text = font.render(text,False,'white')
    surface.blit(text, (position[0],position[1]))


while 1: # game loop
# fill the screen --------------------------------------------------------#  
    window.fill((25, 25, 25))

    draw_text('I NEED WATER!', 'Minecraft.ttf', 30, window, [128,150])
    draw_text('(Demo Level)', 'Minecraft.ttf', 15, window, [190,200])
    draw_text('press "S" to start the game', 'Minecraft.ttf', 20, window, [100,430])
    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game_loop()

    
    pygame.display.update()
    clock.tick(fps)


