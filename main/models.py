# from coldetect import check_player_pillar_collision
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


# class PillarPair:
    # PILLAR_SPEED = 5

    # def __init__(self, world, x, y):
    #     self.world = world
    #     self.x = x
    #     self.y = y

    # def update(self, delta):
    #     self.x -= PillarPair.PILLAR_SPEED
    #     if self.x < -40:
    #         self.x = self.world.width+40
    #         self.random_position_y()
    #     pass

    # def hit(self, player):
    #     return check_player_pillar_collision(player.x, player.y,
    #                                          self.x, self.y)

    # def random_position_y(self):
    #     self.y = randint(100, 450)


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # self.pillar_pairs = [PillarPair(
        #     self, width - 100, height // 2), PillarPair(self, width + 350, height // 2)]

        self.player = Player(self, width // 2, height // 2)
        self.state = World.STATE_FROZEN
        self.score = 0

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return

        self.player.update(delta)
        if(self.player.togkob()):
            self.die()

        # for pillar_pair in self.pillar_pairs:
        #     pillar_pair.update(delta)

        #     if pillar_pair.x == self.player.x:
        #         self.score += 1

        #     if pillar_pair.hit(self.player):
        #         self.die()

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
