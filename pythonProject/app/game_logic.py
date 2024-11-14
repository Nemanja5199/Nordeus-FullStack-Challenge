from settings import *


class GameLogic:
    def __init__(self, height_matrix):
        self.height_matrix = height_matrix
        self.rows = len(height_matrix)
        self.cols = len(height_matrix[0])
        self.highlighted_tiles = set()
        self.islands = {}
        self.lives = NORMAL_LIVES
        self.score = 0
        self.lives_streak=0
        self.consecutive_correct = 0
        self.is_hard_mode = False
        self.time_remaining = None
        self.largest_streak = 0

        # Initialize islands
        self.find_all_islands()
        self.highest_num, self.highest_avg = self.get_highest_average_island()
        # print("\nGame Started - Find the island with highest average height!")
        # self.print_islands_info()

    def find_all_islands(self):
        checked_tiles = set()
        island_number = 1

        for row in range(self.rows):
            for col in range(self.cols):
                if (self.height_matrix[row][col] > 0 and
                        (row, col) not in checked_tiles):
                    island_tiles, average = self.calculate_island_info(row, col)
                    checked_tiles.update(island_tiles)
                    self.islands[island_number] = {
                        'tiles': island_tiles,
                        'average_height': average
                    }
                    island_number += 1

    def calculate_island_info(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols or self.height_matrix[row][col] == 0:
            return set(), 0

        island_tiles = set()
        stack = [(row, col)]
        sum_of_heights = 0
        tile_count = 0

        while stack:
            current_row, current_col = stack.pop()

            if (current_row, current_col) in island_tiles:
                continue

            if (0 <= current_row < self.rows and
                    0 <= current_col < self.cols and
                    self.height_matrix[current_row][current_col] > 0):

                island_tiles.add((current_row, current_col))
                sum_of_heights += self.height_matrix[current_row][current_col]
                tile_count += 1

                directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                for dr, dc in directions:
                    stack.append((current_row + dr, current_col + dc))

        average = sum_of_heights / tile_count if tile_count > 0 else 0
        return island_tiles, average

    def update_hover(self, row, col):
        self.highlighted_tiles = set()  # Clear previous highlight
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.height_matrix[row][col] > 0:
                for island_num, info in self.islands.items():
                    if (row, col) in info['tiles']:
                        self.highlighted_tiles = info['tiles']
                        break



    def get_island_at_position(self, row, col):
        for island_num, info in self.islands.items():
            if (row, col) in info['tiles']:
                return island_num, info
        return None, None

    def print_islands_info(self):
        print("\nIslands Information:")
        for number, info in self.islands.items():
            print(f"Island #{number}")
            print(f"  Average Height: {info['average_height']:.2f}")
            print(f"  Number of Tiles: {len(info['tiles'])}")
            print()

    def get_highest_average_island(self):
        if not self.islands:
            return None, 0

        highest_num = max(self.islands.keys(),
                          key=lambda x: self.islands[x]['average_height'])
        return highest_num, self.islands[highest_num]['average_height']

    def check_guess(self, row, col):
        island_num, island_info = self.get_island_at_position(row, col)
        if island_num is not None:
            highest_num, highest_avg = self.get_highest_average_island()
            was_correct = island_num == highest_num
            # print(f"\nClicked Island #{island_num}")
            # print(f"Average Height: {island_info['average_height']:.2f}")

            if was_correct:
                print("Correct! This is the highest island!")
                # Increment the score and streak in the correct guess handler, not here

                return True, False
            else:
                print(f"Wrong! Island #{highest_num} was higher with average {highest_avg:.2f}")
                game_over = self.handle_wrong_guess()
                return False, game_over
        return False, False

    def handle_correct_guess(self):

        # Check if the game is in Hard Mode
        if not self.is_hard_mode:
            # Just increment the score in Normal Mode
            self.score += 1
            self.consecutive_correct += 1
            self.largest_streak = max(self.largest_streak, self.consecutive_correct)
            return 0

        # Hard Mode logic
        self.score += 1
        self.consecutive_correct += 1
        self.lives_streak+=1
        self.largest_streak = max(self.largest_streak, self.consecutive_correct)

        print(f"Lives streak:{self.lives_streak}")

        if self.lives < 3:  # Only if not at max lives
            if self.lives_streak == 5:
                self.lives += 1
                print(f"\nStreak of 5! Extra life earned! Lives: {self.lives}")
                self.lives_streak = 0
            else:
                print(f"\nStreak: {self.lives_streak}/5 for extra life")

        return TIME_BONUS

    def handle_wrong_guess(self):
        self.lives -= 1
        self.largest_streak = max(self.largest_streak, self.consecutive_correct)
        self.consecutive_correct = 0
        self.lives_streak=0

        if self.is_hard_mode:
            print(f"Streak reset! Lives remaining: {self.lives}")
        else:
            print(f"\nWrong guess! Lives remaining: {self.lives}")
        return self.lives <= 0

    def set_game_mode(self, is_hard_mode):
        self.is_hard_mode = is_hard_mode
        self.lives = HARD_LIVES if is_hard_mode else NORMAL_LIVES
        self.time_remaining = HARD_MODE_TIME if is_hard_mode else None
        self.consecutive_correct = 0
        self.largest_streak = 0
        self.score = 0
        print(f"\nGame mode set to: {'Hard' if is_hard_mode else 'Normal'}")
        print(f"Lives: {self.lives}")
        if is_hard_mode:
            print(f"Time remaining: {self.time_remaining}")
            print("Get 5 correct guesses in a row for an extra life!")

    def get_game_state(self):
        return {
            'lives': self.lives,
            'score': self.score,
            'largest_streak': self.largest_streak,
            'consecutive_correct': self.consecutive_correct,
            'lives_streak': self.lives_streak,
            'is_hard_mode': self.is_hard_mode,
            'time_remaining': self.time_remaining
        }