# Import library pygame dan modul pendukung
import pygame
from pygame.locals import *
import sys

# Inisialisasi semua modul pygame
pygame.init()

# Ukuran layar permainan
frame_size_x = 900
frame_size_y = 500

# Set nilai FPS (frame per second)
FPS = 60  # Kecepatan game (60 frame per detik)
velocity = 5
green_hit = pygame.USEREVENT + 1
blue_hit = pygame.USEREVENT + 2

# Ukuran pesawat pemain
ship_width = 55     # Lebar pesawat (55 pixel)
ship_height = 40    # Tinggi pesawat (40 pixel)

# Jumlah maksimal peluru yang bisa ditembak
max_num_of_bullet = 5
bullet_velocity = 7

# Membuat jendela permainan
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

# Menetapkan judul pada jendela game
pygame.display.set_caption("Space Shooter")

# Definisi warna dalam format RGB
white = (255, 255, 255)
black = (0, 0, 0)
green = (110, 194, 54)  # Warna peluru hijau
blue = (23, 54, 235)    # Warna peluru biru
health_font = pygame.font.SysFont('Impact', 40)
winner_font = pygame.font.SysFont('Impact', 100)
border = pygame.Rect((frame_size_x // 2) - 5, 0, 10, frame_size_y)

# Load dan atur gambar latar belakang
background = pygame.transform.scale(
    pygame.image.load('gallery/sprites/background.png'),
    (frame_size_x, frame_size_y)
).convert()

# Load dan atur logo permainan
space_shooter_logo = pygame.image.load('gallery/sprites/space_shooter.png').convert_alpha()
space_shooter_logo = pygame.transform.scale(space_shooter_logo, (300, 150))

# Load dan rotasi pesawat hijau (menghadap kanan)
green_ship_img = pygame.transform.rotate(
    pygame.image.load('gallery/sprites/shipGreen.png').convert_alpha(), 270)

# Load dan rotasi pesawat biru (menghadap kiri)
blue_ship_img = pygame.transform.rotate(
    pygame.image.load('gallery/sprites/shipBlue.png').convert_alpha(), 90)

# Skalakan gambar pesawat agar sesuai ukuran
green_ship = pygame.transform.scale(green_ship_img, (ship_width, ship_height)).convert_alpha()
blue_ship = pygame.transform.scale(blue_ship_img, (ship_width, ship_height)).convert_alpha()

# Load efek suara untuk peluru
bullet_fire_sound = pygame.mixer.Sound('gallery/audio/sfx_fire.ogg')
bullet_hit_sound = pygame.mixer.Sound('gallery/audio/sfx_hit.ogg')
game_end_sound = pygame.mixer.Sound('gallery/audio/sfx_game_over.ogg')

# Fungsi utama permainan
def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += bullet_velocity
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(blue_hit))
            green_bullets.remove(bullet)
            green_bullets.remove(bullet)
        elif bullet.x > frame_size_x:
            green_bullets.remove(bullet)
            for bullet in blue_bullets:
                bullet.x -= bullet_velocity
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"message": "Green ship shot!"}))   
            blue_bullets.remove(bullet)
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)
def blue_movement_handler(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - velocity > border.x + border.width - 5:  #Left
        blue.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and blue.x - velocity + blue.width < frame_size_x - 5:  #Right
        blue.x += velocity
    if keys_pressed[pygame.K_UP] and blue.y - velocity > 0:  #Up
        blue.y -= velocity
    if keys_pressed[pygame.K_DOWN] and blue.y - velocity + blue.height < frame_size_y - 5:  #Down
        blue.y += velocity
def green_movement_handler(keys_pressed, green):
    if keys_pressed[pygame.K_w] and green.y - velocity > 0:  #UP
        green.y -= velocity
    if keys_pressed[pygame.K_a] and green.x - velocity > -5:  #LEFT
        green.x -= velocity
    if keys_pressed[pygame.K_s] and green.y - velocity + green.height < frame_size_y - 5:  #DOWN
        green.y += velocity   
    if keys_pressed[pygame.K_d] and green.x - velocity + green.width < border.x - 5:  #RIGHT
        green.x += velocity
def draw_window(green_rect, blue_rect, green_bullets, blue_bullets, green_health, blue_health):
    window_screen.blit(background, (0, 0))
    pygame.draw.rect(window_screen, black, border)
    green_health_text = health_font.render("Health: " + str(green_health), 1, white)
    blue_health_text = health_font.render("Health: " + str(blue_health), 1, white)
    window_screen.blit(blue_health_text, (720,10))
    window_screen.blit(green_health_text, (10,10))
def draw_winner(text):
    winner_text = winner_font.render(text, 1, white)
    window_screen.blit(winner_text, (frame_size_x // 2 - winner_text.get_width() /2, frame_size_y // 2 - winner_text.get_height() / 2))
    pygame.display.update()
    game_end_sound.play()
    pygame.time.delay(5000)
    
def main():
    clock = pygame.time.Clock()  # Buat clock untuk mengatur kecepatan game
    green_rect = pygame.Rect(100, 100, ship_width, ship_height)  # Posisi awal pesawat hijau
    blue_rect = pygame.Rect(700, 300, ship_width, ship_height)   # Posisi awal pesawat biru
    green_bullets = []  # Daftar peluru yang ditembak oleh pemain hijau
    blue_bullets = []   # Daftar peluru yang ditembak oleh pemain biru
    green_health = 10
    blue_health = 10

    while True:
        clock.tick(FPS)  # Batasi loop per detik agar tetap konsisten

        # Mengecek event dari keyboard/mouse
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()  # Keluar dari pygame
                sys.exit()     # Keluar dari program

            # Kontrol untuk menembak peluru
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < max_num_of_bullet:
                    bullet = pygame.Rect(green_rect.x + green_rect.width, green_rect.y + green_rect.height // 2, 10, 5)
                    green_bullets.append(bullet)
                    bullet_fire_sound.play()
                    bullet_fire_sound.play()  # Suara tembakan pesawat hijau
                if event.key == pygame.K_RCTRL and len(blue_bullets) < max_num_of_bullet:
                    bullet = pygame.Rect(blue_rect.x, blue_rect.y + blue_rect.height // 2,  10, 5)
                    blue_bullets.append(bullet)
                    bullet_fire_sound.play()
                    bullet_fire_sound.play()  # Suara tembakan pesawat biru
                
                if event.type == green_hit:
                    green_health -= 1
                    bullet_hit_sound.play()

                if event.type == blue_hit:
                    blue_health -= 1
                    bullet_hit_sound.play()

        # Gambar latar belakang dan pesawat
        winner_text = ""
        if green_health < 1:
            winner_text = "Blue Wins"

        if blue_health < 1:
            winner_text = "Green Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        print(keys_pressed[pygame.K_LEFT], keys_pressed[pygame.K_RIGHT])
        print(green_bullets, blue_bullets)
        handle_bullets(green_bullets, blue_bullets, green_rect, blue_rect)
        print(green_health, blue_health)
        draw_window(green_rect, blue_rect, green_bullets, blue_bullets) 
        green_movement_handler(keys_pressed, green_rect)
        window_screen.blit(background, (0, 0))
        pygame.draw.rect(window_screen, black, border) 
        window_screen.blit(green_ship, (green_rect.x, green_rect.y))
        window_screen.blit(blue_ship, (blue_rect.x, blue_rect.y))
        for bullet in green_bullets:
            pygame.draw.rect(window_screen, green, bullet)  #green bullets
        for bullet in blue_bullets:
            pygame.draw.rect(window_screen, blue, bullet)
        pygame.display.update()  # Update tampilan layar

# Fungsi tampilan awal sebelum game dimulai
def welcome_screen():
    while True:
        # Tampilkan latar belakang dan logo
        window_screen.blit(background, (0, 0))
        window_screen.blit(space_shooter_logo, (frame_size_x//3, 40))

        # Tampilkan teks "Press Any Key"
        welcome_font = pygame.font.SysFont("impact", 24)
        welcome_text = welcome_font.render("Press Any Key To Begin...", 1, white)
        window_screen.blit(welcome_text, (
            frame_size_x // 2 - welcome_text.get_width() // 2,
            frame_size_y // 2 - welcome_text.get_height() // 2
        ))

        # Cek input keyboard
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("Start the game")
                main()  # Pindah ke game utama jika ada tombol ditekan

        pygame.display.update()  # Update tampilan layar

# Jalankan welcome screen sebagai titik awal
welcome_screen()