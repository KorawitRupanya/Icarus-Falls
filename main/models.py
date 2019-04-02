from random import randint
import arcade.key

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2
MOVEMENT_SPEED = 4
JUMP_SPEED = 15

KEY_MAP = {
    arcade.key.LEFT: DIR_LEFT,
    arcade.key.RIGHT: DIR_RIGHT, }

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_RIGHT: (1, 0),
               DIR_LEFT: (-1, 0)}


class Player:
    GRAVITY = 1
    STARTING_VELOCITY = 15
    JUMPING_VELOCITY = 15

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = Player.STARTING_VELOCITY
        self.next_direction = DIR_STILL
        self.direction = DIR_STILL
        self.py = 0

    def update(self, delta):
        self.py = self.y
        self.y += self.vy
        self.vy -= Player.GRAVITY
        self.direction = self.next_direction
        self.move(self.direction)

    def togkob(self):
        return self.y == 0 or self.y == 600

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]


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

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return

        self.player.update(delta)
        if(self.player.togkob()):
            self.die()

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
