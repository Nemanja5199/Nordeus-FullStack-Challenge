from settings import *


def height_to_color(height):
    if height == 0:  # Special case for water
        return (0, 0, 139)  # Dark blue


    # elif 1 <= height <= 199:  # Water to dark blue range
    #     return (0, 0, int(255 * (height / 399)))

    elif 1 <= height <= 399:  # Blue to green range
        ratio = (height - 1) / 399
        return (0,
                int(255 * ratio),
                int(255 * (1 - ratio)))

    elif 400 <= height <= 599:  # Green to yellow range
        ratio = (height - 400) / 199
        return (int(255 * ratio),
                255,
                0)

    elif 600 <= height <= 799:  # Yellow to brown range
        ratio = (height - 600) / 199
        brown = (165, 142, 42)
        yellow = (255, 255, 0)
        return (int(yellow[0] + (brown[0] - yellow[0]) * ratio),
                int(yellow[1] + (brown[1] - yellow[1]) * ratio),
                int(yellow[2] + (brown[2] - yellow[2]) * ratio))

    else:  # 800 to 1000 - Brown to white range
        ratio = (height - 800) / 200
        brown = (165, 142, 42)
        return (int(brown[0] + (255 - brown[0]) * ratio),
                int(brown[1] + (255 - brown[1]) * ratio),
                int(brown[2] + (255 - brown[2]) * ratio))