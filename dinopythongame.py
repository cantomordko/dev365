import os
import sys
import pygame
import random
from pygame import *

pygame.init()

screen_size_display = (width_screen, height_screen) = (600, 150)
FPS = 60
gravity = 0.6

black_color = (0, 0, 0)
white_color = (255, 255, 255)
bg_color = (235, 235, 235)

highest_scores = 0

screen_layout_display = pygame.display.set_mode(screen_size_display)
time_clock = pygame.time.Clock()
pygame.display.set_caption("Dino Run")


def load_image(name, sx=-1, sy=-1, colorkey=None):
    fullname = os.path.join('resources', name)
    img = pygame.image.load(fullname)
    img = img.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)

    if sx != -1 or sy != -1:
        img = pygame.transform.scale(img, (sx, sy))

    return img, img.get_rect()


def load_sprite_sheet(s_name, namex, namey, scx=-1, scy=-1, c_key=None):
    fullname = os.path.join('resources', s_name)
    sh = pygame.image.load(fullname)
    sh = sh.convert()

    sh_rect = sh.get_rect()

    sprites = []

    sx = sh_rect.width / namex
    sy = sh_rect.height / namey

    for i in range(0, namey):
        for j in range(0, namex):
            rect = pygame.Rect((j * sx, i * sy, sx, sy))
            img = pygame.Surface(rect.size)
            img = img.convert()
            img.blit(sh, (0, 0), rect)

            if c_key is not None:
                if c_key == -1:
                    c_key = img.get_at((0, 0))
                img.set_colorkey(c_key, RLEACCEL)

            if scx != -1 or scy != -1:
                img = pygame.transform.scale(img, (scx, scy))

            sprites.append(img)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


def gameover_display_message(rbtn_image, gmo_image):
    rbtn_rect = rbtn_image.get_rect()
    rbtn_rect.centerx = width_screen / 2
    rbtn_rect.top = height_screen * 0.52

    gmo_rect = gmo_image.get_rect()
    gmo_rect.centerx = width_screen / 2
    gmo_rect.centery = height_screen * 0.35

    screen_layout_display.blit(rbtn_image, rbtn_rect)
    screen_layout_display.blit(gmo_image, gmo_rect)


def extractDigits(num):
    if num > -1:
        d = []
        while num // 10 != 0:
            d.append(num % 10)
            num = num // 10

        d.append(num % 10)
        while len(d) < 5:
            d.append(0)
        d.reverse()
        return d


class Dino:
    def __init__(self, sx=-1, sy=-1):
        self.imgs, self.rect = load_sprite_sheet('dino.png', 5, 1, sx, sy, -1)
        self.imgs1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, sy, -1)
        self.rect.bottom = int(0.98 * height_screen)
        self.rect.left = width_screen / 15
        self.image = self.imgs[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.jumping = False
        self.dead = False
        self.ducking = False
        self.blinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5

        self.stand_position_width = self.rect.width
        self.duck_position_width = self.rect1.width

    def draw(self):
        screen_layout_display.blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98 * height_screen):
            self.rect.bottom = int(0.98 * height_screen)
            self.jumping = False

    def update(self):
        if self.jumping:
            self.movement[1] = self.movement[1] + gravity

        if self.jumping:
            self.index = 0
        elif self.blinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.ducking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.dead:
            self.index = 4

        if not self.ducking:
            self.image = self.imgs[self.index]
            self.rect.width = self.stand_position_width
        else:
            self.image = self.imgs1[(self.index) % 2]
            self.rect.width = self.duck_position_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.dead and self.counter % 7 == 6 and not self.blinking:
            self.score += 1

        self.counter = (self.counter + 1)


# Pozostałe klasy i funkcje pozostają bez zmian, ale wszystkie odniesienia do dźwięków zostały usunięte.
# Na przykład w klasie `Dino` usunięto odtwarzanie dźwięku w momencie zdobycia punktów.

def introduction_screen():
    intro = True
    while intro:
        screen_layout_display.fill(bg_color)
        font = pygame.font.Font(None, 36)
        text = font.render("Press any key to start", True, black_color)
        text_rect = text.get_rect(center=(width_screen / 2, height_screen / 2))
        screen_layout_display.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                intro = False

    return False

def gameplay():
    global highest_scores
    game_running = True
    dino = Dino(44, 47)  # Rozmiar dinozaura
    ground = pygame.Surface((width_screen, height_screen))  # Powierzchnia dla ziemi
    clock = pygame.time.Clock()

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dino.jumping:
                    dino.jumping = True
                    dino.movement[1] = -dino.jumpSpeed
                if event.key == pygame.K_DOWN:
                    dino.ducking = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.ducking = False

        dino.update()

        # Rysowanie tła i dinozaura
        screen_layout_display.fill(bg_color)
        dino.draw()

        # Aktualizacja ekranu
        pygame.display.update()
        clock.tick(FPS)

def main():
    isGameQuit = introduction_screen()
    if not isGameQuit:
        gameplay()


main()