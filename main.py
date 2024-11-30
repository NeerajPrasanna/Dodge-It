import pygame as pg
import random as rand

pg.init()
screen = pg.display.set_mode((1366, 768))
pg.display.set_caption("Dodge the Obstacles")
clock = pg.time.Clock()

player_img = pg.image.load("bob.png")
font_large = pg.font.Font(None, 74)
font_small = pg.font.Font(None, 48)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

player_x, player_y = 100, 500
player_velocity = 0

obstacle_list = []
obstacle_speed = 10
min_width, max_width = 40, 80
min_height, max_height = 20, 60

current_score = 0
best_score = 0


def add_obstacle():
    obstacle_width = rand.randint(min_width, max_width)
    obstacle_height = rand.randint(min_height, max_height)
    obstacle_y = rand.randint(0, 768 - obstacle_height)
    obstacle_list.append(pg.Rect(1366, obstacle_y, obstacle_width, obstacle_height))


def move_obstacles():
    for obstacle in obstacle_list[:]:
        obstacle.x -= obstacle_speed
        if obstacle.x < -max_width:
            obstacle_list.remove(obstacle)


def draw_score():
    score_display = font_large.render(f"Score: {current_score}", True, black)
    screen.blit(score_display, (20, 20))


def draw_player(y_pos):
    screen.blit(player_img, (player_x, y_pos))


def landing_screen():
    while True:
        screen.fill(white)
        screen.blit(font_large.render("Dodge It", True, black), (400, 150))
        screen.blit(font_small.render("Rules:", True, black), (400, 250))
        screen.blit(font_small.render("Up Arrow - Move Up", True, black), (400, 300))
        screen.blit(font_small.render("Down Arrow - Move Down", True, black), (400, 350))
        screen.blit(font_small.render("S - Stop Moving", True, black), (400, 400))
        screen.blit(font_small.render("Q - Quit", True, black), (400, 450))
        screen.blit(font_small.render("Press Space to Start", True, green), (400, 550))
        screen.blit(font_small.render("A small game by Neeraj Prasanna", True, blue), (400, 700))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                return


def game_over_screen():
    global best_score, current_score
    if current_score > best_score:
        best_score = current_score
    while True:
        screen.fill(white)
        screen.blit(font_large.render("Game Over", True, red), (500, 150))
        screen.blit(font_small.render(f"Your Score: {current_score}", True, black), (500, 300))
        screen.blit(font_small.render(f"High Score: {best_score}", True, black), (500, 350))
        screen.blit(font_small.render("Press R to Restart or Q to Quit", True, green), (400, 500))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    return
                if event.key == pg.K_q:
                    pg.quit()
                    exit()


while True:
    landing_screen()
    player_y = 500
    player_velocity = 0
    current_score = 0
    obstacle_list.clear()

    game_running = True
    while game_running:
        screen.fill(white)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    player_velocity = -5
                if event.key == pg.K_DOWN:
                    player_velocity = 5
                if event.key == pg.K_q:
                    pg.quit()
                    exit()
                if event.key == pg.K_s:
                    player_velocity = 0

        player_y += player_velocity

        if player_y < 0:
            player_y = 768
        if player_y > 768:
            player_y = 0

        draw_player(player_y)

        if rand.randint(1, 50) == 1:
            add_obstacle()

        move_obstacles()

        for obstacle in obstacle_list:
            pg.draw.rect(screen, blue, obstacle)
            if obstacle.colliderect(pg.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())):
                game_running = False
            if obstacle.x <= player_x:
                current_score += 1

        draw_score()
        pg.display.update()
        clock.tick(60)

    game_over_screen()
