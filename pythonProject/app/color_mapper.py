COLORS = {
    (0, 0): lambda h: (0, 0, 139),
    (1, 200): lambda h: (0, int(255 * h / 200), int(255 * (1 - h / 200))),
    (201, 400): lambda h: (int(255 * (h - 200) / 200), 255, 0),
    (401, 600): lambda h: (int(255 * (1 - (h - 400) / 200) + 205 * (h - 400) / 200),
                           int(255 * (1 - (h - 400) / 200) + 180 * (h - 400) / 200),
                           int(90 * (h - 400) / 200)),
    (601, 899): lambda h: (int(205 + (139 - 205) * (h - 600) / 299),
                           int(180 + (125 - 180) * (h - 600) / 299),
                           int(90 + (107 - 90) * (h - 600) / 299)),
    (900, 1000): lambda h: (int(139 + (255 - 139) * (h - 900) / 100),
                            int(125 + (255 - 125) * (h - 900) / 100),
                            int(107 + (255 - 107) * (h - 900) / 100)),
}

def height_to_color(height):
    for range_tuple, color_func in COLORS.items():
        if range_tuple[0] <= height <= range_tuple[1]:
            return color_func(height)
    return (255, 255, 255)