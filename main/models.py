from random import randint
from detect import is_hit, fire_hit
import arcade.key
import math
import pygame

pygame.mixer.init()

# Sound effect initialise
century = pygame.mixer.Sound(
    '.././soundEffect/C.wav')
derp = pygame.mixer.Sound('.././soundEffect/Derp Sound Effect.wav')
no_one = pygame.mixer.Sound('.././soundEffect/No One Has Ever Done That.wav')
nope = pygame.mixer.Sound('.././soundEffect/Nope Sound Effect.wav')
sad = pygame.mixer.Sound('.././soundEffect/Sad Violin Airhorn.wav')
wow = pygame.mixer.Sound('.././soundEffect/WOW.wav')
hot = pygame.mixer.Sound('.././soundEffect/HOT HOT HOT HOT.wav')

music = pygame.mixer.music.load('.././soundEffect/music.mp3')
pygame.mixer.music.play(-1)

# moving attribute
DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2

# moving speed attribute
MOVEMENT_SPEED = 4
JUMP_SPEED = 5

# map the keys with the attribute
KEY_MAP = {
    arcade.key.LEFT: DIR_LEFT,
    arcade.key.RIGHT: DIR_RIGHT, }

# offsets for moving keys
DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_RIGHT: (1, 0),
               DIR_LEFT: (-1, 0)}


class Player:
    GRAVITY = 0.10
    JUMPING_VELOCITY = 0.05

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = Player.JUMPING_VELOCITY
        self.next_direction = DIR_STILL
        self.direction = DIR_STILL
        self.py = 0
        self.check = False
        self.lp = 100

    def update(self, delta):
        if self.lp > 0:
            self.py = self.y
            self.y += self.vy
            if self.x < -30:
                self.x = self.world.width + 30
            if self.x > self.world.width+30:
                self.x = -30
            if self.y+35 >= self.world.height:
                self.vy *= -5
            self.vy -= Player.GRAVITY
            if self.y <= 85:
                self.lp = -1
                self.check = True
                derp.play()
            else:
                self.direction = self.next_direction
                self.move(self.direction)
            self.world.score += 1

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]


class BottomFire:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y


class Fire:
    FIRE_SPEED = 2

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.plus_speed = 0.1
        self.change_x = 0
        self.change_y = 0
        self.hit = False

    def update(self, delta):
        if self.world.player.lp > 0:
            if self.x <= 30 or self.y >= self.world.height - 49 or self.x >= self.world.width - 30:
                self.change_x *= -1
                self.change_y *= -1

            self.x += self.change_x
            self.y += self.change_y

            if randint(0, 100) == 0:
                start_x = self.x
                start_y = self.y

                dest_x = self.world.player.x
                dest_y = self.world.player.y

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                self.change_x = math.cos(angle) * Fire.FIRE_SPEED
                self.change_y = math.sin(angle) * Fire.FIRE_SPEED

    def fire_hit(self, player):
        if self.hit == False:
            self.hit = fire_hit(player.x, player.y,
                                self.x, self.y)
            return self.hit
        else:
            return False


class Arrow:

    def __init__(self, world, x, y):
        self.world = world
        self.x = randint(0, 600)
        self.y = y
        self.speed = 5
        self.vy = 0.1

    def up_speed(self):
        if self.world.score % 100 == 0:
            self.speed += self.vy

    def update(self, delta):
        self.y -= self.speed
        self.up_speed()
        if self.y < -179:
            self.y = self.world.height+179
            self.x = randint(0, 600)
        pass

    def hit(self, player):
        return is_hit(player.x, player.y,
                      self.x, self.y)


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arrowNumbers = 5
        self.fireNumbers = 2
        self.arrows = []
        self.player = Player(self, width // 2, height // 2)
        self.fires = []
        self.state = World.STATE_FROZEN
        self.score = 0
        self.bottomfire = []

        for i in range(self.arrowNumbers):
            self.arrows.append(
                Arrow(self, width - randint(40, 200), height+randint(100, 400)))
        pass
        self.arrow = self.arrows

        for i in range(self.fireNumbers):
            self.fires.append(
                Fire(self, width//2, -50)
            )
        self.fire = self.fires

        self.generate_bottom_fire()

    def generate_bottom_fire(self):
        self.bottomfire.append(BottomFire(self, 30, 30))
        self.bottomfire.append(BottomFire(self, 90, 30))
        self.bottomfire.append(BottomFire(self, 150, 30))
        self.bottomfire.append(BottomFire(self, 210, 30))
        self.bottomfire.append(BottomFire(self, 270, 30))
        self.bottomfire.append(BottomFire(self, 330, 30))
        self.bottomfire.append(BottomFire(self, 390, 30))
        self.bottomfire.append(BottomFire(self, 450, 30))
        self.bottomfire.append(BottomFire(self, 510, 30))
        self.bottomfire.append(BottomFire(self, 570, 30))

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.player.check = False
        self.player.update(delta)

        for i in self.fires:
            if i.fire_hit(self.player):
                self.player.check = True
                self.player.lp = -1
                hot.play()

            else:
                i.update(delta)

        if(self.score % 500 == 0):
            self.arrowNumbers += 1
            self.arrows.append(
                Arrow(self, self.width - randint(40, 200), self.height+randint(100, 400)))

        for i in self.arrow:
            if i.hit(self.player):
                self.player.check = True
                self.player.lp -= 1
                nope.play()
            elif self.player.lp < 0:
                # self.die()
                self.player.lp = -1
                nope.stop()
            else:
                i.update(delta)

    def on_key_press(self, key, key_modifiers):
        if self.player.lp > 0:
            if key == arcade.key.UP:
                self.player.vy = JUMP_SPEED
            if key in KEY_MAP:
                self.player.next_direction = KEY_MAP[key]

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN

    def is_started(self):
        return self.state == World.STATE_STARTED

    def die(self):
        self.state = World.STATE_DEAD

    def is_dead(self):
        return self.state == World.STATE_DEAD
