import pygame
from pygame.locals import *
import sys

pygame.init()
frame_size_x = 900
frame_size_y = 500
FPS = 60
ship_width = 55
ship_height = 40
max_num_of_bullet = 5
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

pygame.display.set_caption("Space Shooter")

white = (255, 255, 255)  # RGB Code for White
black = (0, 0, 0)  # RGB Code for Black
green = (110, 194, 54)  # RGB Code for Green Bullet
blue = (23, 54, 235)  # RGB Code for Blue Bullet

background = pygame.transform.scale(pygame.image.load('gallery/sprites/background.png'),(frame_size_x, frame_size_y)).convert()
space_shooter_logo = pygame.image.load('gallery/sprites/space_shooter.png').convert_alpha()
space_shooter_logo = pygame.transform.scale(space_shooter_logo, (300, 150))
bullet_fire_sound = pygame.mixer.Sound('gallery/audio/sfx_fire.ogg')
def welcome_screen():
    while True:
        window_screen.blit(background, (0, 0))  
        window_screen.blit(space_shooter_logo, (frame_size_x // 3, 40))  
        welcome_font = pygame.font.SysFont("impact", 24)
        welcome_text = welcome_font.render("Press Any Key To Begin...", 1, white)
        window_screen.blit(welcome_text, (frame_size_x // 2 - welcome_text.get_width() // 2, frame_size_y // 2 - welcome_text.get_height() // 2))  
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("Start the game")
pygame.display.update()
welcome_screen()    