import pygame

def load_sprite_sheet(path, frame_width, frame_height):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []

    sheet_width, sheet_height = sheet.get_size()

    for y in range(0, sheet_height, frame_height):
        row = []
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface((x, y, frame_width, frame_height))
            row.append(frame)
        frames.append(row)

    return frames