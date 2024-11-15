import pygame
import random
import serial
import time
import csv
import os
import pandas as pd
from datetime import datetime

pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Monstres & Cie Game")

# Connexion à l'Arduino
try:
    arduino = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=1)
    time.sleep(2)
    arduino_connected = True
    print("Arduino connecté.")
except serial.SerialException:
    arduino = None
    arduino_connected = False
    print("Erreur de connexion à l'Arduino.")

# Chargement de la musique
pygame.mixer.init()
pygame.mixer.music.load("son.mp3")

# Couleurs et images
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background_img = pygame.image.load('background.jpg')
character_img = pygame.image.load('player.png')
character_img = pygame.transform.scale(character_img, (100, 160))
character_x = 100
character_y = 440
character_width, character_height = character_img.get_size()

menu_background_img = pygame.image.load('menu.jpg')

# Obstacles
obstacle_images = [
    pygame.image.load('m.png'),
    pygame.image.load('m1.png'),
    pygame.image.load('m2.png'),
    pygame.image.load('m3.png'),
    pygame.image.load('m4.png'),
    pygame.image.load('m5.png'),
    pygame.image.load('m6.png'),
    pygame.image.load('m7.png'),
    pygame.image.load('m8.png'),
    pygame.image.load('m9.png'),
    pygame.image.load('m10.png'),
    pygame.image.load('m11.png'),
    pygame.image.load('m12.png'),
    pygame.image.load('m13.png')
]
for i in range(len(obstacle_images)):
    obstacle_images[i] = pygame.transform.scale(obstacle_images[i], (100, 100))

# Variables de jeu
is_jumping = False
jump_speed = 20
gravity = 1
character_velocity_y = 0
obstacle_speed = 5
obstacles = []
score = 0
font = pygame.font.Font(None, 36)
game_over = False
game_paused = False
menu = True
leaderboard = False

# Collecte des informations du joueur
def get_player_info():
    pseudo = input("Entrez votre pseudo : ")
    sexe = input("Entrez votre sexe (H/F) : ")
    age = input("Entrez votre âge : ")
    dominant_hand = input("Êtes-vous droitier ou gaucher ? (D/G) : ")
    return pseudo, sexe, age, dominant_hand

# Sauvegarde des données dans un fichier CSV
def save_game_data(pseudo, sexe, age, dominant_hand, score, duration):
    filename = f"{pseudo}_data.csv"
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([pseudo, sexe, age, dominant_hand, score, duration])

# Générer un nouvel obstacle
def spawn_obstacle():
    obstacle_x = 800
    obstacle_y = random.choice([300, 350, 400, 450])
    obstacle_img = random.choice(obstacle_images)
    obstacles.append({'rect': pygame.Rect(obstacle_x, obstacle_y, 100, 100), 'img': obstacle_img})

# Réinitialiser le jeu
def reset_game():
    global score, character_y, obstacles, game_over, is_jumping, character_velocity_y, start_time
    score = 0
    character_y = 440
    obstacles.clear()
    spawn_obstacle()
    game_over = False
    is_jumping = False
    character_velocity_y = 0
    start_time = datetime.now()

# Fonction pour lire les données de l'Arduino
def read_arduino():
    if arduino and arduino.in_waiting > 0:
        line = arduino.readline().decode('utf-8').strip()
        return line
    return None

# Afficher le menu
def draw_menu():
    screen.blit(menu_background_img, (0, 0))
    arduino_status = font.render("Arduino connected" if arduino_connected else "Arduino not connected", True, WHITE)
    screen.blit(arduino_status, (270, 560))
    pygame.display.update()

# Lire les fichiers CSV pour créer le leaderboard
def get_leaderboard():
    player_scores = []
    files = [f for f in os.listdir() if f.endswith("_data.csv")]
    for file in files:
        try:
            data = pd.read_csv(file, names=["Pseudo", "Sexe", "Age", "Main Dominante", "Score", "Durée"])
            best_score = data["Score"].max()
            player_name = data["Pseudo"][0]
            player_scores.append((player_name, best_score))
        except Exception as e:
            print(f"Erreur avec le fichier {file}: {e}")

    # Trier les joueurs par score décroissant
    player_scores.sort(key=lambda x: x[1], reverse=True)
    return player_scores

# Dessiner la page Leaderboard
def draw_leaderboard():
    screen.fill(BLACK)
    title_text = font.render("Leaderboard", True, WHITE)
    screen.blit(title_text, (300, 50))

    leaderboard_data = get_leaderboard()

    for idx, (name, score) in enumerate(leaderboard_data[:10], start=1):
        text = font.render(f"{idx}. {name}: {score} points", True, WHITE)
        screen.blit(text, (100, 100 + idx * 40))

    return_text = font.render("Press B to return to menu", True, WHITE)
    screen.blit(return_text, (200, 550))
    pygame.display.update()

# Dessiner l'écran de pause
def draw_pause_screen():
    pause_text = font.render("Paused", True, WHITE)
    return_text = font.render("Press B to return to menu", True, WHITE)
    screen.blit(pause_text, (350, 250))
    screen.blit(return_text, (200, 300))
    pygame.display.update()

# Dessiner l'écran de fin de jeu
def draw_game_over_screen():
    game_over_text = font.render("GAME OVER", True, WHITE)
    restart_text = font.render("Press R to play again", True, WHITE)
    return_text = font.render("Press B to return to menu", True, WHITE)
    screen.blit(game_over_text, (300, 250))
    screen.blit(restart_text, (200, 300))
    screen.blit(return_text, (200, 350))
    pygame.display.update()

# Boucle principale
running = True
pseudo, sexe, age, dominant_hand = get_player_info()
duration = 0
reset_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    reset_game()
                    menu = False
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_l:
                    leaderboard = True
                    menu = False
        
        elif leaderboard:
            draw_leaderboard()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                leaderboard = False
                menu = True
        
        elif game_over:
            if duration == 0:
                pygame.mixer.music.stop()
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                save_game_data(pseudo, sexe, age, dominant_hand, score, duration)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_over = False
                    pygame.mixer.music.play(-1)
                    duration = 0
                elif event.key == pygame.K_b:
                    game_over = False
                    menu = True
                    duration = 0
        
        elif game_paused:
            pygame.mixer.music.pause()  # Met la musique en pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    game_paused = False
                    menu = True
                elif event.key == pygame.K_p:
                    game_paused = False
                    pygame.mixer.music.unpause()  # Reprend la musique

        else:
            if arduino_connected:
                arduino_input = read_arduino()
                if arduino_input:
                    try:
                        pot_value = int(arduino_input)
                        character_y = 440 - (pot_value / 1023) * 300
                    except ValueError:
                        pass
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not game_over:
                        character_velocity_y = -jump_speed
                        is_jumping = True
                    elif event.key == pygame.K_p:
                        game_paused = True

    if menu:
        draw_menu()
    elif leaderboard:
        draw_leaderboard()
    elif game_paused:
        draw_pause_screen()
    elif game_over:
        draw_game_over_screen()
    else:
        character_velocity_y += gravity
        character_y += character_velocity_y
        if character_y >= 440:
            character_y = 440
            character_velocity_y = 0

        for obstacle in obstacles:
            obstacle['rect'].x -= obstacle_speed
            if obstacle['rect'].x + obstacle['rect'].width < 0:
                obstacles.remove(obstacle)
                score += 1
                spawn_obstacle()

        character_rect = pygame.Rect(character_x, int(character_y), character_width, character_height)
        for obstacle in obstacles:
            if character_rect.colliderect(obstacle['rect']):
                game_over = True

        screen.blit(background_img, (0, 0))
        screen.blit(character_img, (character_x, int(character_y)))
        for obstacle in obstacles:
            screen.blit(obstacle['img'], obstacle['rect'].topleft)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (670, 30))
        pause_text = font.render("Pause (P)", True, WHITE)
        screen.blit(pause_text, (30, 30))

        pygame.display.update()
        clock.tick(60)

pygame.quit()