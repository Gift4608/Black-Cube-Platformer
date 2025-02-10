import time
import pygame
pygame.init()
screen_w = 200
screen_h = 100
files_dir = '/data/data/org.gift.bcp/files/app/'
screen = pygame.display.set_mode((screen_w, screen_h), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption('Black Cube Platformer')
pygame.display.set_icon(pygame.image.load(files_dir + 'images/BCPL.png').convert_alpha())
font = pygame.font.Font(files_dir + 'fonts/tiny5.ttf', 15)


clock = pygame.time.Clock()
fps = 30
fingers = {}

level_name = '0'
levels_count = 5
level_hitboxes = [
    [], 
    [], 
    [], 
    []
]

blocks = [
    pygame.image.load(files_dir + 'images/blocks/block1.png').convert_alpha(), 
    pygame.image.load(files_dir + 'images/blocks/block2.png').convert_alpha()
]

items = [
    pygame.image.load(files_dir + 'images/items/coin.png').convert_alpha(), 
    pygame.image.load(files_dir + 'images/items/flag.png').convert_alpha()
]

player = [
    pygame.image.load(files_dir + 'images/player/p1.png').convert_alpha(), 
    pygame.image.load(files_dir + 'images/player/p2.png').convert_alpha(), 
    pygame.image.load(files_dir + 'images/player/pd.png').convert_alpha()
]
player_dir = 0
player_state = 0
player_x = 95
player_y = 45
player_xv = 0
player_yv = 0
player_can_jump = False
player_image = 0
player_rect = None
player_collide = False
player_walk_speed = 2
player_jump_height = 5

enemy = [
    pygame.image.load(files_dir + 'images/enemy/e1.png').convert_alpha(), 
    pygame.image.load(files_dir + 'images/enemy/e2.png').convert_alpha(), 
    pygame.image.load(files_dir + 'images/enemy/ed.png').convert_alpha()
]

ui = [
    [
        pygame.image.load(files_dir + 'images/ui/b1.png').convert_alpha(), 
        pygame.image.load(files_dir + 'images/ui/b2.png').convert_alpha(), 
        pygame.image.load(files_dir + 'images/ui/b3.png').convert_alpha()
    ], 
    [
        pygame.image.load(files_dir + 'images/ui/b1p.png').convert_alpha(), 
        pygame.image.load(files_dir + 'images/ui/b2p.png').convert_alpha(), 
        pygame.image.load(files_dir + 'images/ui/b3p.png').convert_alpha()
    ], 
    [
        pygame.image.load(files_dir + 'images/ui/play.png').convert_alpha(), 
        pygame.image.load(files_dir + 'images/ui/play_p.png').convert_alpha()
        
    ], 
    [
        pygame.image.load(files_dir + 'images/ui/retry.png').convert_alpha(), 
        pygame.image.load(files_dir + 'images/ui/retry_p.png').convert_alpha()
    ], 
    [
        pygame.image.load(files_dir + 'images/ui/next.png').convert_alpha(), 
        pygame.image.load(files_dir + 'images/ui/next_p.png').convert_alpha()
    ], 
    [
        pygame.image.load(files_dir + 'images/ui/menu.png').convert_alpha(), 
        pygame.image.load(files_dir + 'images/ui/menu_p.png').convert_alpha()
    ]
]
b1_pos = (35, screen_h - 25)
b2_pos = (10, screen_h - 25)
b3_pos = (screen_w - 30, screen_h - 25)
b1_rect = ui[0][0].get_rect(topleft=b1_pos)
b2_rect = ui[0][1].get_rect(topleft=b2_pos)
b3_rect = ui[0][2].get_rect(topleft=b3_pos)
b1_pressed = False
b2_pressed = False
b3_pressed = False
play_pos = (screen_w / 2 - 20, screen_h / 2 - 10 + 10)
play_rect = ui[2][0].get_rect(topleft=play_pos)
play_pressed = False
play_old_pressed = play_pressed
logo_text = font.render('Black Cube Platformer', False, (0, 0, 0))
retry_pos = (screen_w / 2 - 22.5, screen_h / 2 - 10 + 10)
retry_rect = ui[3][0].get_rect(topleft=retry_pos)
retry_pressed = False
retry_old_pressed = retry_pressed
loose_text = font.render('You Dead!', False, (0, 0, 0))
next_pos = (screen_w / 2 - 20, screen_h / 2 - 10 + 10)
next_rect = ui[4][0].get_rect(topleft=retry_pos)
next_pressed = False
next_old_pressed = next_pressed
win_text = font.render('You Win!', False, (0, 0, 0))
select_level_text = []
for i in range(levels_count):
    select_level_text.append(font.render(str(i + 1), False, (0, 0, 0)))
menu_pos = None
menu_rect = None
menu_pressed = False
menu_old_pressed = menu_pressed

select_level_text_pos = []
for i in range(levels_count):
    select_level_text_pos.append(((i + 1) * 20, 20))


select_level_text_rect = []
for i in range(levels_count):
    select_level_text_rect.append(select_level_text[i].get_rect(topleft=select_level_text_pos[i]))
    



coins = 0
coins_text = font.render('COINS : ' + str(coins), False, (0, 0, 0))

sounds = [
    pygame.mixer.Sound(files_dir + 'sounds/music.mp3'), 
    pygame.mixer.Sound(files_dir + 'sounds/click.mp3'), 
    pygame.mixer.Sound(files_dir + 'sounds/coin.mp3'), 
    pygame.mixer.Sound(files_dir + 'sounds/loose.mp3')
]




cam_x = 0
cam_y = 0

def reset_game():
    global player_dir, player_state, player_x, player_y, player_xv, player_yv, player_can_jump, player_image, player_rect, player_collide, b1_pressed, b2_pressed, b3_pressed, coins, coins_text, cam_x, cam_y, level_name, level_file_name, loaded_level
    player_dir = 0
    player_state = 0
    player_x = 95
    player_y = 45
    player_xv = 0
    player_yv = 0
    player_can_jump = False
    player_image = 0
    player_rect = None
    player_collide = False
    b1_pressed = False
    b2_pressed = False
    b3_pressed = False
    coins = 0
    coins_text = font.render('COINS : ' + str(coins), False, (0, 0, 0))
    cam_x = 0
    cam_y = 0
    level_file_name = level_name + '.txt'
    loaded_level = None
    try:
        with open(files_dir + 'levels/' + level_file_name, 'r') as file_level:
            loaded_level = file_level.read().split('\n')
    except FileNotFoundError:
        loaded_level = []

sounds[0].play(-1)


scene = 0
scene_transfer = 0
scene_timer = 0
scene_0_transfer = 0.125
scene_1_transfer = 0.125
scene_2_transfer = 0.125
scene_3_transfer = 1
scene_4_transfer = 1


run = True
while run:
    clock.tick(fps)
    if scene == 0:
        screen.fill((255, 255, 255))
        screen.blit(logo_text, (screen_w / 2 - logo_text.get_width() / 2, 10))
        screen.blit(ui[2][play_pressed], play_pos)
        if scene_timer == 0:
            play_old_pressed = play_pressed
            play_pressed = False
            for finger, pos in fingers.items():
                if play_rect.collidepoint(pos):
                    play_pressed = True
            if play_old_pressed and not play_pressed:
                sounds[1].play()
        if play_old_pressed and not play_pressed:
            if scene_timer == 0:
                scene_timer = time.time()
                scene_transfer = 1
            if scene_transfer == 1:
                if time.time() - scene_timer >= scene_1_transfer:
                    scene = 1
                    scene_timer = 0
    
    elif scene == 1:

        screen.fill((255, 255, 255))
        menu_pos = (5, screen_h - 25)
        menu_rect = ui[5][0].get_rect(topleft=menu_pos)
        screen.blit(ui[5][menu_pressed], menu_pos)
        if scene_timer == 0:
            menu_old_pressed = menu_pressed
            menu_pressed = False
            for finger, pos in fingers.items():
                if menu_rect.collidepoint(pos):
                    menu_pressed = True
            if menu_old_pressed and not menu_pressed:
                sounds[1].play()
                scene_timer = time.time()
                scene_transfer = 0
        
        
        for i in range(levels_count):
            screen.blit(select_level_text[i], select_level_text_pos[i])
            if scene_timer == 0:
                for finger, pos in fingers.items():
                    if select_level_text_rect[i].collidepoint(pos):
                        sounds[1].play()
                        select_level_text.pop(i)
                        select_level_text.insert(i, font.render(str(i + 1), False, (125, 125, 125)))
                        level_name = str(i + 1)
                        scene_timer = time.time()
                        scene_transfer = 2
        if scene_transfer == 2:
            if scene_timer != 0:
                if time.time() - scene_timer >= scene_2_transfer:
                    select_level_text.clear()
                    for i in range(levels_count):
                        select_level_text.append(font.render(str(i + 1), False, (0, 0, 0)))
                    scene_timer = 0
                    reset_game()
                    scene = 2
        if scene_transfer == 0:
            if scene_timer != 0:
                if time.time() - scene_timer >= scene_0_transfer:
                    select_level_text.clear()
                    for i in range(levels_count):
                        select_level_text.append(font.render(str(i + 1), False, (0, 0, 0)))
                    scene_timer = 0
                    scene = 0
                
                    
    elif scene == 2:
        
        coins_text = font.render('COINS : ' + str(coins), False, (0, 0, 0))
        
        b1_pressed = False
        b2_pressed = False
        b3_pressed = False
        for finger, pos in fingers.items():
            if b1_rect.collidepoint(pos):
                b1_pressed = True
            if b2_rect.collidepoint(pos):
                b2_pressed = True
            if b3_rect.collidepoint(pos):
                b3_pressed = True
        
        screen.fill((255, 255, 255))
    
        cam_x = player_x - 95
        cam_y = player_y - 45
    
        level_hitboxes[0].clear()
        level_hitboxes[1].clear()
        level_hitboxes[2].clear()
        level_hitboxes[3].clear()
    
        element_splited = None
        object_surf = None
        for idx, element in enumerate(loaded_level):
            element_splited = element.split(', ')
            if element_splited[0] == '0':
                if int(element_splited[1]) == 0:
                    screen.blit(blocks[0], (int(element_splited[2]) - cam_x, int(element_splited[3]) - cam_y))
                    level_hitboxes[0].append(blocks[0].get_rect(topleft=(int(element_splited[2]) - cam_x, int(element_splited[3]) - cam_y)))
                elif int(element_splited[1]) == 1:
                    screen.blit(blocks[1], (int(element_splited[2]) - cam_x, int(element_splited[3]) - cam_y))
                    level_hitboxes[1].append(blocks[1].get_rect(topleft=(int(element_splited[2]) - cam_x, int(element_splited[3]) - cam_y)))
                elif int(element_splited[1]) == 2:
                    screen.blit(items[0], (int(element_splited[2]) + 4 - cam_x, int(element_splited[3]) + 4 - cam_y))
                    level_hitboxes[2].append([items[0].get_rect(topleft=(int(element_splited[2]) + 4 - cam_x, int(element_splited[3]) + 4 - cam_y)), idx, int(element_splited[1])])
                elif int(element_splited[1]) == 3:
                    screen.blit(items[1], (int(element_splited[2]) + 4 - cam_x, int(element_splited[3]) - cam_y))
                    level_hitboxes[2].append([items[1].get_rect(topleft=(int(element_splited[2]) + 4 - cam_x, int(element_splited[3]) - cam_y)), idx, int(element_splited[1])])
                elif int(element_splited[1]) == 4:
                    object_surf = font.render(element_splited[4], False, (0, 0, 0))
                    screen.blit(object_surf, (int(element_splited[2]) - object_surf.get_width() / 2 - cam_x, int(element_splited[3]) - cam_y))
        
        if player_state == 0:
            if player_dir == 0:
                player_image = 0
            elif player_dir == 1:
                player_image = 1
        elif player_state == 2:
            player_image = 2
        
        screen.blit(player[player_image], (player_x - cam_x, player_y - cam_y))
        
        if b1_pressed and not b2_pressed:
            player_xv = -player_walk_speed
            player_dir = 0
        elif b2_pressed and not b1_pressed:
            player_xv = player_walk_speed
            player_dir = 1
        if b3_pressed and player_can_jump:
            player_yv = player_jump_height
            
        
        if player_state == 0:
            player_y -= player_yv
            player_rect = player[0].get_rect(topleft=(player_x - cam_x, player_y - cam_y))
            player_collide = False
            for hitbox in level_hitboxes[0]:
                if player_rect.colliderect(hitbox):
                    player_collide = True
            for hitbox in level_hitboxes[1]:
                if player_rect.colliderect(hitbox):
                    player_collide = True
                    player_state = 2
                    scene_transfer = 3
                    sounds[3].play()
                    
            if not player_collide:
                player_yv = max(-10, player_yv - 0.5)
                player_can_jump = False
            else:
                while player_collide:
                    player_y += -0.5 if player_yv < 0 else 0.5
                    player_rect = player[0].get_rect(topleft=(player_x - cam_x, player_y - cam_y))
                    player_collide = False
                    for hitbox in level_hitboxes[0]:
                        if player_rect.colliderect(hitbox):
                            player_collide = True
                    for hitbox in level_hitboxes[1]:
                        if player_rect.colliderect(hitbox):
                            player_collide = True
                            player_state = 2
                            scene_transfer = 3
                            sounds[3].play()
                            
                            
                
                if player_yv < 0:
                    player_yv = 0
                    player_can_jump = True
                elif player_yv >= 0:
                    player_yv = -0.5
                    player_can_jump = False
                
            
            player_x -= player_xv
            
            player_rect = player[0].get_rect(topleft=(player_x - cam_x, player_y - cam_y))
            
            player_collide = False
            for hitbox in level_hitboxes[0]:
                if player_rect.colliderect(hitbox):
                    player_collide = True
            for hitbox in level_hitboxes[1]:
                if player_rect.colliderect(hitbox):
                    player_collide = True
                    player_state = 2
                    scene_transfer = 3
                    sounds[3].play()
                    
            if not player_collide:
                player_xv *= 0.5
            else:
                player_x += player_xv / 3
                
                for i in range(2):
                    player_rect = player[0].get_rect(topleft=(player_x - cam_x, player_y - cam_y))
                    player_collide = False
                    for hitbox in level_hitboxes[0]:
                        if player_rect.colliderect(hitbox):
                            player_collide = True
                    for hitbox in level_hitboxes[1]:
                        if player_rect.colliderect(hitbox):
                            player_collide = True
                            player_state = 2
                            scene_transfer = 3
                            sounds[3].play()
                            
                    if not player_collide:
                        pass
                    else:
                        player_x += player_xv / 3
                        
                player_xv = 0
            
            
            if player_y >= 300:
                player_state = 2
                scene_transfer = 3
                sounds[3].play()
            
            player_rect = player[0].get_rect(topleft=(player_x - cam_x, player_y - cam_y))
            for item in level_hitboxes[2]:
                if player_rect.colliderect(item[0]):
                    if item[2] == 2:
                        loaded_level.pop(item[1])
                        coins += 1
                        sounds[2].play()
                        break
                    elif item[2] == 3:
                        player_state = 1
                        scene_transfer = 4
                        break
            
        screen.blit(ui[b1_pressed][0], b1_pos)
        screen.blit(ui[b2_pressed][1], b2_pos)
        screen.blit(ui[b3_pressed][2], b3_pos)
        screen.blit(coins_text, (screen_w - 5 - coins_text.get_width(), 5))
        if player_state == 2 and scene_transfer == 3 and scene_timer == 0:
            scene_timer = time.time()
        elif player_state == 2 and scene_transfer == 3 and scene_timer != 0:
            if time.time() - scene_timer >= scene_3_transfer:
                scene_timer = 0
                scene = 3
        
        if player_state == 1 and scene_transfer == 4 and scene_timer == 0:
            scene_timer = time.time()
        elif player_state == 1 and scene_transfer == 4 and scene_timer != 0:
            if time.time() - scene_timer >= scene_4_transfer:
                scene_timer = 0
                scene = 4
        
    elif scene == 3:
        screen.fill((255, 255, 255))
        screen.blit(loose_text, (screen_w / 2 - loose_text.get_width() / 2, 10))
        menu_pos = (screen_w / 2 - 20, screen_h / 2 - 10 + 35)
        menu_rect = ui[5][0].get_rect(topleft=menu_pos)
        screen.blit(ui[5][menu_pressed], menu_pos)
        if scene_timer == 0:
            menu_old_pressed = menu_pressed
            menu_pressed = False
            for finger, pos in fingers.items():
                if menu_rect.collidepoint(pos):
                    menu_pressed = True
            if menu_old_pressed and not menu_pressed:
                sounds[1].play()
                scene_timer = time.time()
                scene_transfer = 0
        
        screen.blit(ui[3][retry_pressed], retry_pos)
        
        if scene_timer == 0:
            retry_old_pressed = retry_pressed
            retry_pressed = False
            for finger, pos in fingers.items():
                if retry_rect.collidepoint(pos):
                    retry_pressed = True
            if retry_old_pressed and not retry_pressed:
                sounds[1].play()
                scene_timer = time.time()
                scene_transfer = 2
            
            
        if scene_transfer == 2:
            if time.time() - scene_timer >= scene_2_transfer:
                reset_game()
                scene = 2
                scene_timer = 0
        if scene_transfer == 0:
            if time.time() - scene_timer >= scene_0_transfer:
                scene = 0
                scene_timer = 0
    elif scene == 4:
        screen.fill((255, 255, 255))
        screen.blit(win_text, (screen_w / 2 - win_text.get_width() / 2, 10))
        menu_pos = (screen_w / 2 - 20, screen_h / 2 - 10 + 35)
        menu_rect = ui[5][0].get_rect(topleft=menu_pos)
        screen.blit(ui[5][menu_pressed], menu_pos)
        if scene_timer == 0:
            menu_old_pressed = menu_pressed
            menu_pressed = False
            for finger, pos in fingers.items():
                if menu_rect.collidepoint(pos):
                    menu_pressed = True
            if menu_old_pressed and not menu_pressed:
                sounds[1].play()
                scene_timer = time.time()
                scene_transfer = 0
        
        screen.blit(ui[4][next_pressed], next_pos)
        
        if scene_timer == 0:
            next_old_pressed = next_pressed
            next_pressed = False
            for finger, pos in fingers.items():
                if next_rect.collidepoint(pos):
                    next_pressed = True
            if next_old_pressed and not next_pressed:
                sounds[1].play()
                scene_timer = time.time()
                if int(level_name) < levels_count:
                    level_name = str(int(level_name) + 1)                
                    scene_transfer = 2
                else:
                    scene_transfer = 1
            
            
        if scene_transfer == 2:
            if time.time() - scene_timer >= scene_2_transfer:
                reset_game()
                scene = 2
                scene_timer = 0
        if scene_transfer == 0:
            if time.time() - scene_timer >= scene_0_transfer:
                scene = 0
                scene_timer = 0
        if scene_transfer == 1:
            if time.time() - scene_timer >= scene_1_transfer:
                scene = 1
                scene_timer = 0
        
        
        
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            break
        if event.type == pygame.FINGERDOWN:
            fingers[event.finger_id] = (event.x * screen_w, event.y * screen_h)
        if event.type == pygame.FINGERUP:
            fingers.pop(event.finger_id, None)