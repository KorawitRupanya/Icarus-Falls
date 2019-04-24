import arcade
from models import World, Player, Arrow

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

TEXTURE_UP = 0
TEXTURE_DOWN = 1
TEXTURE_HURT_UP = 2
TEXTURE_HURT_DOWN = 3


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


class Window(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.start()
        self.background = arcade.load_texture(
            ".././images/Back ground/hell.jpg")
        self.arrow_sprite = [ArrowSprite(model=self.world.arrow[0]), ArrowSprite(model=self.world.arrow[1]),
                             ArrowSprite(model=self.world.arrow[2]), ArrowSprite(
                                 model=self.world.arrow[3]),
                             ArrowSprite(model=self.world.arrow[4])]

    def start(self):
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dot_sprite = PlayerSprite(
            model=self.world.player)

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_started():
            self.world.start()

        self.world.on_key_press(key, key_modifiers)

    def draw_background(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def update(self, delta):
        self.world.update(delta)
        if self.world.is_dead():
            self.start()

    def on_draw(self):
        arcade.start_render()

        self.draw_background()
        for arrow in self.arrow_sprite:
            arrow.draw()
        arcade.draw_text(str(self.world.score),
                         self.width - 30, self.height - 30,
                         arcade.color.BLACK, 20)
        self.dot_sprite.draw()


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
