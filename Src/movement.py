import math
from config import SPEED, STOP_DISTANCE, ACCELERATION, FRICTION, MAX_SPEED


def move_towards(entity, target_x, target_y):
    dx = target_x - entity.x
    dy = target_y - entity.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance > STOP_DISTANCE:
        entity.set_state("walk")
        if dx > 0:
            entity.direction = "right"
        else:
            entity.direction = "left"

        dx /= distance
        dy /= distance

        entity.vx += dx * ACCELERATION
        entity.vy += dy * ACCELERATION
    else:
        if abs(entity.vx) < 0.1 and abs(entity.vy) < 0.1:
            entity.set_state("idle")

    entity.vx *= FRICTION
    entity.vy *= FRICTION

    speed = math.sqrt(entity.vx**2 + entity.vy**2)
    if speed > MAX_SPEED:
        entity.vx = (entity.vx / speed) * MAX_SPEED
        entity.vy = (entity.vy / speed) * MAX_SPEED

    entity.x += entity.vx
    entity.y += entity.vy
