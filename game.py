# Pymunk for physics
# PIL for image manipulation
# Sockets for multiplayer
# Perlin-noise for random worlds

# Pygame template
import pygame
import random


# Settings
WIN_WIDTH = 1280
WIN_HEIGHT = 720
TITLE = "My Game"
FPS = 60
DEBUG = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Intialize
pygame.init()
pygame.mixer.init() # For sound or music
display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags=pygame.SCALED, vsync=1)

pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Create a surface (Surfaces are placed in *display_surface* with blit (block image transfer) method)
# test_surf = pygame.Surface((50, 50))
# test_surf.fill(BLUE)
# test_rect = test_surf.get_rect(center=(WIDTH/2, HEIGHT/2))

def laser_update(laser_list, speed=300):
    for laser_rect in laser_list:
        laser_rect.y -= round(speed * dt)
        display_surface.blit(laser_surf, laser_rect)

        if laser_rect.bottom < 0:
            laser_list.remove(laser_rect)

def display_score():
    score_text = f'Score: {pygame.time.get_ticks() // 1000}'
    text_surf = font.render(score_text, True, 'white')
    text_rect = text_surf.get_rect(midbottom=(WIN_WIDTH/2, WIN_HEIGHT - 20))
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(20, 10), 2, 2)
    display_surface.blit(text_surf, text_rect)

def laser_timer(can_shoot, duration=500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot

def display_meteor(meteor_list, speed=200):
    for meteor_tuple in meteor_list:
        #meteor_rect.y += round(speed * dt)
        #direction = pygame.math.Vector2(1, 2)
        meteor_rect = meteor_tuple[0]
        direction = meteor_tuple[1]
        meteor_rect.center += direction * speed * dt
        display_surface.blit(meteor_surf, meteor_rect)

    new_meteor_list = []
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if meteor_rect.top < WIN_HEIGHT:
            new_meteor_list.append(meteor_tuple)

    return new_meteor_list

bg_surf = pygame.image.load('./graphics/background.png').convert()

ship_surf = pygame.image.load('./graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
rot = 1

laser_surf = pygame.image.load("./graphics/laser.png").convert_alpha()
laser_list = []
laser_rect = laser_surf.get_rect(midbottom=ship_rect.midtop)

# Laser timer
can_shoot = True
shoot_time = None

# Import text
font = pygame.font.Font('./graphics/subatomic.ttf', 50)

# Meteor
meteor_surf = pygame.image.load('./graphics/meteor.png').convert_alpha()
meteor_list = []

# Meteor Timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

# Sound
laser_sound = pygame.mixer.Sound('./sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')
bg_music = pygame.mixer.Sound('./sounds/music.wav')
bg_music.play(-1)

# Game Loop
running = True
while running:
    # Keep loop running at the right speed
    dt = clock.tick(FPS) / 1000
    # clock.tick_busy_loop(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_timer:
            x = random.randint(100, WIN_WIDTH - 100)
            direction = pygame.math.Vector2( random.uniform(-0.5, 0.5) ,1)
            meteor_rect = meteor_surf.get_rect(midbottom=(x, 0))
            meteor_list.append((meteor_rect, direction))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and can_shoot: # 0.5 seconds delay before we can shoot again
                laser_rect = laser_surf.get_rect(midbottom=ship_rect.midbottom)
                laser_list.append(laser_rect)
                laser_sound.play()
                # timer
                can_shoot = False
                shoot_time = pygame.time.get_ticks()

        # if event.type == pygame.MOUSEMOTION:
        #     print(event.pos) # Mouse position
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         print("LEFT")
    
    ship_rect.center = pygame.mouse.get_pos()

    # Update Game Logic
    # ship_rect.y -= 5
    # if ship_rect.y <= 0:
    #     ship_rect.y = 0

    # Rotation logic
    # old_rect = ship_rect
    # rot += 1
    # if rot == 360:
    #     rot = 1
    # new_ship_surf = pygame.transform.rotate(ship_surf, rot)
    # ship_rect = new_ship_surf.get_rect()
    # ship_rect.center = old_rect.center

    # laser_rect.midbottom = ship_rect.midtop
    # laser_rect.y -= round(200 * dt)
    pygame.time.get_ticks()

    # meteor ship collision
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            #running = False
            pass

    # laser meteor collision
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            if laser_rect.colliderect(meteor_rect):
                explosion_sound.play()
                meteor_list.remove(meteor_tuple)
                laser_list.remove(laser_rect)

    # Draw / Render
    # display_surface.fill('teal')
    display_surface.blit(bg_surf, (0, 0))

    # display_surface.blit(test_surf, (WIDTH/2, HEIGHT/2))
    display_score()
    
    laser_update(laser_list)
    
    can_shoot = laser_timer(can_shoot, 400)
    
    display_surface.blit(ship_surf, ship_rect)
    meteor_list = display_meteor(meteor_list)
    
    if DEBUG:
        # pygame.draw.rect(ship_surf, 'red', (0, 0, ship_rect.width, ship_rect.height), 1)
        pygame.draw.rect(display_surface, 'red', ship_rect, 1)
        # pygame.draw.rect(display_surface, 'red', laser_rect, 1)
        for laser_rect in laser_list:
            pygame.draw.rect(display_surface, 'red', laser_rect, 1)
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            pygame.draw.rect(display_surface, 'red', meteor_rect, 1)

    # *after* drawing everything flip the display
    pygame.display.update() # or pygame.display.update()
    

pygame.quit()
print(laser_list, meteor_list)

