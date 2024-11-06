class GameLogic:
    def __init__(self, height_matrix):
        self.height_matrix = height_matrix
        self.rows = len(height_matrix)
        self.cols = len(height_matrix[0])
        self.highlighted_tiles = set()

    def find_island_at_position(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols or self.height_matrix[row][col] == 0:
            return set()

        island_tiles = set()
        stack = [(row, col)]

        while stack:
            current_row, current_col = stack.pop()

            if (current_row, current_col) in island_tiles:
                continue

            # If it's a valid land tile
            if (0 <= current_row < self.rows and 0 <= current_col < self.cols and
                    self.height_matrix[current_row][current_col] > 0):

                island_tiles.add((current_row, current_col))


                directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                for dr, dc in directions:
                    stack.append((current_row + dr, current_col + dc))

        return island_tiles

    def update_hover(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.height_matrix[row][col] > 0:
                self.highlighted_tiles = self.find_island_at_position(row, col)
            else:
                self.highlighted_tiles = set()