def is_hit(player_x, player_y, arrow_x, arrow_y):
    if arrow_y - 60 <= player_y + 20:
        if arrow_y - 60 <= player_y - 20:
            return False
        if player_x - 20 <= arrow_x + 20 and arrow_x - 20 <= player_x + 20:
            return True
    return False
