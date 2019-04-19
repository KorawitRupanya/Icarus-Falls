def is_hit(player_x, player_y, coin_x, coin_y):
    if coin_y - 20 <= player_y + 20:
        if coin_y + 20 <= player_y - 20:
            return False
        if player_x - 20 <= coin_x +20 and coin_x - 20 <= player_x + 20:
            return True
    return False
