import pygame as pg
import os
from sys import exit
from random import randint

pg.init()
pg.font.init()

WIDTH = 650
HEIGHT = 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Title')
#pg.display.set_icon()

FPS = 60

clock = pg.time.Clock()

background_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "aim_game", "sprites", "background.png")).convert()

score = 0
score_font = pg.font.SysFont("Calibri", 30)
score_surf = score_font.render(f"Score: {score}", False, "black")

pg.mouse.set_visible(False)

class Target(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "aim_game", "sprites", "target.png")).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.x = x_pos
        self.rect.y = y_pos

target_group = pg.sprite.Group()

for _ in range(50):
    x = randint(0, WIDTH)
    y = randint(0, HEIGHT)

    target = Target(x, y)
    target_group.add(target)

class Crosshair(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "aim_game", "sprites", "crosshair.png")).convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH//2, HEIGHT//2))

    def mouse_track(self):
        self.rect.center = pg.mouse.get_pos()

    def collision(self, target_group):
        global score, score_surf
        if pg.mouse.get_pressed()[0]:
            print(pg.mouse.get_pressed())
            if pg.sprite.spritecollide(crosshair.sprite, target_group, True):
                score += 100
                score_surf = score_font.render(f"Score: {score}", False, "black")

    def update(self):
        self.mouse_track()
        self.collision(target_group)

crosshair = pg.sprite.GroupSingle(Crosshair())

gameplay = True
won = False


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    if gameplay:
        screen.blit(background_surf, (0,0))
        target_group.draw(screen)
        crosshair.draw(screen)
        crosshair.update()
        screen.blit(score_surf, (0,0))

    if not bool(target_group):
        gameplay = False
        won = True

    if won:
        key = pg.key.get_pressed()
        screen.fill("grey")
        text_font = pg.font.SysFont("Calibri", 30)
        text_surf = text_font.render("Escape to quit", False, "black")
        screen.blit(score_surf, (300, 100))
        screen.blit(text_surf, (300, HEIGHT//2))
        if key[pg.K_ESCAPE]:
            pg.quit()
            exit()


    pg.display.update()
    clock.tick(FPS)