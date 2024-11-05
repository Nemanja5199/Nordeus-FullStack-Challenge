





def getTilePos(self, mouse_pos):
    x, y = mouse_pos
    row = y // TILESIZE
    col = x // TILESIZE
    return row, col