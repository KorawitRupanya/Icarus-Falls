import arcade
import pygame
import subprocess
from models import World, Player, Arrow, Fire

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Icarus Fall The Game"

TEXTURE_UP = 0
TEXTURE_DOWN = 1
TEXTURE_HURT_UP = 2
TEXTURE_HURT_DOWN = 3

FIRE_1 = 0
FIRE_2 = 1


class PlayerSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        texture = arcade.load_texture(
            ".././images/character_sprites/kitty1.png")
        self.textures.append(texture)
        texture = arcade.load_texture(
            ".././images/character_sprites/kitty2.png")
        self.textures.append(texture)
        texture = arcade.load_texture(
            ".././images/character_sprites/kittyBurn1.png")
        self.textures.append(texture)
        texture = arcade.load_texture(
            ".././images/character_sprites/kittyBurn2.png")
        self.textures.append(texture)
        self.set_texture(TEXTURE_UP)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        if self.model.py > self.model.y:
            if self.model.check:
                self.set_texture(TEXTURE_HURT_UP)
            else:
                self.set_texture(TEXTURE_UP)
        else:
            if self.model.check:
                self.set_texture(TEXTURE_HURT_DOWN)
            else:
                self.set_texture(TEXTURE_DOWN)
        super().draw()


class ArrowSprite(arcade.Sprite):
    def __init__(self, model):
        self.model = model
        self.arrow_sprite = arcade.Sprite(
            '.././images/Object_sprites/arrow.png')

    def draw(self):
        self.arrow_sprite.set_position(self.model.x, self.model.y)
        self.arrow_sprite.draw()


class BottomFire(arcade.Sprite):
    FIRE_IMAGE = ["fire1.png", "fire2.png"]
    IS_FIRE_ONE = 0

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        texture = arcade.load_texture(
            '.././images/Object_sprites/fire1.png')
        self.textures.append(texture)
        texture = arcade.load_texture(
            '.././images/Object_sprites/fire2.png')
        self.textures.append(texture)
        self.set_texture(FIRE_1)
        self.IS_FIRE_ONE = 0

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        if self.IS_FIRE_ONE > 40:
            self.IS_FIRE_ONE = 0
        if self.IS_FIRE_ONE <= 20:
            self.set_texture(FIRE_2)
        else:
            self.set_texture(FIRE_1)
        self.IS_FIRE_ONE += 1
        super().draw()


class FireSprite(arcade.Sprite):
    FIRE_IMAGE = ["fire1.png", "fire2.png"]
    IS_FIRE_ONE = 0

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        texture = arcade.load_texture(
            '.././images/Object_sprites/fire1.png')
        self.textures.append(texture)
        texture = arcade.load_texture(
            '.././images/Object_sprites/fire2.png')
        self.textures.append(texture)
        self.set_texture(FIRE_1)
        self.IS_FIRE_ONE = 0

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        if self.IS_FIRE_ONE > 40:
            self.IS_FIRE_ONE = 0
        if self.IS_FIRE_ONE <= 20:
            self.set_texture(FIRE_2)
        else:
            self.set_texture(FIRE_1)
        self.IS_FIRE_ONE += 1
        super().draw()


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.start()

        self.menu = {'score': arcade.load_texture(".././images/Back ground/loser-score-board.png"),
                     'play': arcade.load_texture(".././images/Back ground/replay.png"),
                     'credit': arcade.load_texture(".././images/Back ground/credit.png"),
                     'quit': arcade.load_texture(".././images/Back ground/QuitButton.png")}

    def start(self):
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.offset = 0
        self.arrows = []
        self.fires = []
        self.numArrow = 5
        self.bottomFires = []
        self.background = arcade.load_texture(
            ".././images/Back ground/sky.jpg")

        for i in range(self.numArrow):
            self.arrows.append(ArrowSprite(model=self.world.arrow[i]))
        self.arrow_sprite = self.arrows

        for n in range(self.world.fireNumbers):
            self.fires.append(FireSprite(model=self.world.fire[n]))
        self.fire_sprite = self.fires

        for i in range(10):
            self.bottomFires.append(BottomFire(model=self.world.bottomfire[i]))
        self.bottomfires_sprite = self.bottomFires

        self.player_sprite = PlayerSprite(
            model=self.world.player)

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_started():
            self.world.start()

        self.world.on_key_press(key, key_modifiers)

    def draw_background(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.offset,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2 + self.offset)-SCREEN_HEIGHT,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def draw_lp(self):
        arcade.draw_rectangle_filled(
            (self.width - 120) + (100 - self.world.player.lp), 30, self.world.player.lp * 2, 20, arcade.color.CHERRY)

    def update(self, delta):
        self.world.update(delta)
        if self.world.is_dead():
            self.world.freeze()

        if self.world.is_started():
            self.offset -= 1
            self.offset %= SCREEN_HEIGHT

        if (self.world.arrowNumbers != self.numArrow):
            self.arrows.append(ArrowSprite(model=self.world.arrow[-1]))
            self.numArrow = self.world.arrowNumbers

    def on_draw(self):
        arcade.start_render()

        self.draw_background()

        for arrow in self.arrow_sprite:
            arrow.draw()

        for fire in self.fire_sprite:
            fire.draw()

        for bf in self.bottomfires_sprite:
            bf.draw()

        arcade.draw_text(str(int(self.world.score)),
                         25, self.height - 40,
                         arcade.color.BLACK, 20)

        arcade.draw_text("LP",
                         self.width - 35, 45, arcade.color.BLACK, 10)

        self.player_sprite.draw()

        self.draw_lp()

        if self.world.player.lp == -1:
            texture = self.menu['score']
            arcade.draw_texture_rectangle(
                self.width//2, self.height//2+200, texture.width, texture.height, texture, 0)
            arcade.draw_text(str(int(self.world.score)),
                             self.width//2-80, 475,
                             arcade.color.WHITE, 100)
            texture = self.menu['play']
            arcade.draw_texture_rectangle(
                self.width//2, self.height//2, texture.width, texture.height, texture, 0)
            texture = self.menu['credit']
            arcade.draw_texture_rectangle(
                self.width//2, self.height//2-200, texture.width, texture.height, texture, 0)
            texture = self.menu['quit']
            arcade.draw_texture_rectangle(
                self.width-60, self.height-55, texture.width, texture.height, texture, 0)

    def replay(self, x, y):
        if self.world.player.lp == -1:
            if self.width//2-205 <= x <= self.width//2+205 and self.height//2-70 <= y <= self.height//2+70:
                self.start()
                self.world.start()

    def credit(self, x, y):
        if self.world.player.lp == -1:
            if ((self.height//2)-200) - (95) <= y <= ((self.height//2)-200) + (95)and self.width//2-95 <= x <= self.width//2+95:
                print('credit')

    def quit_game(self, x, y):
        if self.world.player.lp == -1:
            if self.height-80 <= y <= self.height-20 and self.width-108 <= x <= self.width + 28:
                exit()

    def on_mouse_press(self, x, y, button, modifiers):
        self.replay(x, y)
        self.credit(x, y)
        self.quit_game(x, y)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
