import arcade
from models import World, Player

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


class PlayerSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        # if self.model.py > self.model.y:
        #     self.texture_id = ("./../images/character_sprites/qTBAk6eEc.png")
        # else:
        #     self.texture_id = (
        #         "./../images/character_sprites/4498da5568c62377df6e9bb32794d8d1--angel-wings-drawings-of.png")
        super().draw()


class Window(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

        self.start()

    def start(self):
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dot_sprite = PlayerSprite(
            ".././images/1.png", model=self.world.player)

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_started():
            self.world.start()

        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)
        if self.world.is_dead():
            self.start()

    def on_draw(self):
        arcade.start_render()

        self.dot_sprite.draw()
        # for pillar_pair_sprite in self.pillar_pair_sprites:
        #     pillar_pair_sprite.draw()

        arcade.draw_text(str(self.world.score),
                         self.width - 30, self.height - 30,
                         arcade.color.BLACK, 20)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
