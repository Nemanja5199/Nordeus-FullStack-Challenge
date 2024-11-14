
TILESIZE = 16
ROWS = 30
COLS = 30
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLS
HEADER_HEIGHT = 50
BAR_WIDTH=80
FPS = 70
TITLE = "How high up ?"
BEACH_SIZE = TILESIZE // 4

FONT="../fonts/pixelated.ttf"



BGCOLOUR = (40, 40, 40)
BLACK = (0, 0, 0)
DARKBLUE = (0, 0, 139)
WHITE = (255, 255, 255)
HEADER_COLOR = (50, 50, 50)
BAR_COLOR= (50, 50, 50)
FONT_SIZE = 36
BEACH_COLOR =(238, 214, 175)



MAX_HEIGHT = 1000


NORMAL_LIVES = 3
HARD_LIVES = 2
HARD_MODE_TIME = 20
TIME_BONUS = 5




GAME_STATE_HOME = "HOME"
GAME_STATE_PLAYING = "PLAYING"
GAME_STATE_GAME_OVER = "GAME_OVER"
GAME_STATE_OPTIONS = "OPTIONS"
GAME_STATE_LEADERBOARD = "LEADER_BOARD"


MUSIC_VOLUME = 0.1
MUSIC_PATHS = {
    'menu': '../music/menu.mp3',
    'game': [
        '../music/song3.mp3',
        '../music/menu.mp3',
        '../music/song2.mp3',
        '../music/song1.mp3'
    ]
}


SOUND_EFFECTS_VOLUME = 0.7
SOUND_EFFECTS = {
    'button': '../sound effects/button.mp3',
    'correct': '../sound effects/correct island.mp3',
    'wrong': '../sound effects/wrong.mp3'
}


# Wave Animation
WAVE_SPEED = 1000
WAVE_AMPLITUDE = 1.5
WATER_SHADES = {
    0: (0, 50, 150),     # Lighter blue, immediate water next to land
    1: (0, 75, 180),     # Medium-light blue, one tile away from land
    2: (0, 100, 200),    # Light blue, two tiles away from land
    3: (0, 125, 220)     # Very light blue, further away
}

