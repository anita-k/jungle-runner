import pygame
from sys import exit
from random import randint, choice

game_width = 1500
game_height = 864
ground_level = game_height - 128


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        player_walk_3 = pygame.image.load('graphics/player/player_walk_3.png').convert_alpha()
        player_walk_4 = pygame.image.load('graphics/player/player_walk_4.png').convert_alpha()
        player_walk_5 = pygame.image.load('graphics/player/player_walk_5.png').convert_alpha()
        player_walk_6 = pygame.image.load('graphics/player/player_walk_6.png').convert_alpha()
        player_walk_7 = pygame.image.load('graphics/player/player_walk_7.png').convert_alpha()
        player_walk_8 = pygame.image.load('graphics/player/player_walk_8.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6,
                            player_walk_7, player_walk_8]

        self.has_landed = False

        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(280, ground_level))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

        self.land_sound = pygame.mixer.Sound('audio/thud.mp3')
        self.land_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= ground_level:
            self.gravity = -20
            self.jump_sound.play()
            steps_sound.set_volume(0)
            self.has_landed = False

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            if not self.has_landed:
                self.has_landed = True
                self.land_sound.play()
                steps_sound.set_volume(0.5)

    def animation_state(self):
        if self.rect.bottom < ground_level:
            self.image = self.player_jump
        else:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()

        if enemy_type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = ground_level - 150
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = ground_level

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(game_width + 100, game_width + 300), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 8
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(game_width / 2, 40))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/asd.ttf', 50)
title_font = pygame.font.Font('font/asd.ttf', 140)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.mp3')
bg_music.set_volume(0.4)
steps_sound = pygame.mixer.Sound('audio/steps.mp3')
steps_sound.set_volume(0.5)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

background_surface = pygame.image.load('graphics/background.png').convert()
background_rect = background_surface.get_rect(topleft=(0, 0))
background_rect_2 = background_surface.get_rect(topleft=(game_width, 0))

ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

ground_surface_2 = pygame.image.load('graphics/ground.png').convert_alpha()

ground_rect = ground_surface.get_rect(topleft=(0, ground_level))
ground_rect_2 = ground_surface_2.get_rect(topleft=(game_width, ground_level))

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(game_width / 2, game_height / 2))

game_name = title_font.render('Jungle Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(game_width / 2, game_height / 2 - 250))

game_message = test_font.render('Press space to start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(game_width / 2, (game_height / 2) + 200))

restart_message = test_font.render('Press space to play again', False, (111, 196, 169))
restart_message_rect = restart_message.get_rect(center=(game_width / 2, game_height / 2 + 250))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                bg_music.play(loops=-1)
                steps_sound.play(loops=-1)
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        background_rect.x -= 2
        if background_rect.right <= 0:
            background_rect.left = game_width
        screen.blit(background_surface, background_rect)
        background_rect_2.x -= 2
        if background_rect_2.right <= 0:
            background_rect_2.left = game_width
        screen.blit(background_surface, background_rect_2)

        ground_rect.x -= 6
        if ground_rect.right <= 0:
            ground_rect.left = game_width

        screen.blit(ground_surface, ground_rect)

        ground_rect_2.x -= 6
        if ground_rect_2.right <= 0:
            ground_rect_2.left = game_width

        screen.blit(ground_surface_2, ground_rect_2)

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        bg_music.stop()
        steps_sound.stop()
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(game_width / 2, game_height / 2 + 200))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(restart_message, restart_message_rect)

    pygame.display.update()
    clock.tick(60)
