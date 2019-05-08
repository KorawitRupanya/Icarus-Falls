import math


def is_hit(player_x, player_y, arrow_x, arrow_y):
    if arrow_y - 60 <= player_y + 50:
        if arrow_y - 60 <= player_y - 35:
            return False
        if player_x - 20 <= arrow_x + 20 and arrow_x - 20 <= player_x + 20:
            check = True
            return True
    return False


def fire_hit(player_x, player_y, fire_x, fire_y):
    a = player_x - fire_x
    b = player_y - fire_y
    c = math.sqrt(((a**2)+(b**2)))
    if c < 60:
        return True
    return False
