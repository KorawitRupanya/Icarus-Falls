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

    def update(self, delta):
        self.py = self.y
        self.y += self.vy
        self.vy -= Player.GRAVITY
        self.direction = self.next_direction
        self.move(self.direction)

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]


class Arrow:
    ARROW_SPEED = 5

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0.2

    def up_speed(self):
        Arrow.ARROW_SPEED += self.vy

    def is_position_negative(self):
        if self.y < 0:
            self.y = 0

    def update(self, delta):
        self.y -= Arrow.ARROW_SPEED
        # self.is_position_negative()
        if self.y < -179:
            self.y = self.world.height+179
            self.random_position()
        pass

    def hit(self, player):
        return is_hit(player.x, player.y,
                      self.x, self.y)

    def random_position(self):
        self.x = randint(50, 400)


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.player = Player(self, width // 2, height // 2)
        self.state = World.STATE_FROZEN
        self.score = 0
        self.arrow = [Arrow(self, width - 40, height), Arrow(self, width - 60, height + 100),
                      Arrow(self, width - 200, height +
                            200), Arrow(self, width - 100, height + 300),
                      Arrow(self, width - 200, height + 400)]

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.player.check = False
        self.player.update(delta)

        for i in self.arrow:
            i.update(delta)
            if i.hit(self.player):
                self.player.check = True
                self.freeze()

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
