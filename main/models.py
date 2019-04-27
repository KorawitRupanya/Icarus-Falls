from random import randint
from detect import is_hit
import arcade.key

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2
MOVEMENT_SPEED = 4
JUMP_SPEED = 5


KEY_MAP = {
    arcade.key.LEFT: DIR_LEFT,
    arcade.key.RIGHT: DIR_RIGHT, }

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
        self.py = self.y
        self.y += self.vy
        if self.x < -30:
            self.x = self.world.width + 30
        if self.x > self.world.width+30:
            self.x = -30
        if self.y+35 >= self.world.height:
            self.vy = 0
            self.vy -= Player.GRAVITY
        self.vy -= Player.GRAVITY
        if(self.y - 50 < 0):
            self.world.freeze()
        self.direction = self.next_direction
        self.move(self.direction)

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]


class Soil:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0


class Fire:
    def __init__(self, world, x, y, vx, vy):
        self.world = world
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x > self.world.width - 60  \
                or self.x < 60:
            self.vx *= -1
        if self.y > self.world.height - 60 \
                or self.y < 60:
            self.vy *= -1


class Arrow:
    ARROW_SPEED = 5

    def __init__(self, world, x, y):
        self.world = world
        self.x = randint(0, 600)
        self.y = y
        self.vy = 1

    def up_speed(self):
        if(self.world.score % 100 == 0):
            Arrow.ARROW_SPEED += self.vy

    def freeze_arrow(self):
        self.ARROW_SPEED = 0

    def is_position_negative(self):
        if self.y < 0:
            self.y = 0

    def update(self, delta):
        self.y -= Arrow.ARROW_SPEED
        self.up_speed()
        # self.is_position_negative()
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
        self.arrows = []
        self.player = Player(self, width // 2, height // 2)
        self.state = World.STATE_FROZEN
        self.score = 0
        for i in range(self.arrowNumbers):
            self.arrows.append(
                Arrow(self, width - randint(40, 200), height+randint(100, 400)))
        pass
        self.arrow = self.arrows

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.player.check = False
        self.player.update(delta)
        for i in self.arrow:
            if i.hit(self.player):
                self.player.check = True
                self.player.lp -= 1
                i.freeze_arrow()

            elif(self.player.lp < 0):
                self.die()
            else:
                i.update(delta)

        self.score += 1

    def on_key_press(self, key, key_modifiers):
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
