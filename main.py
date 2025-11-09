from pygame import*
from random import randint


init()
size = 1000, 800
win = display.set_mode(size)
clock = time.Clock()

platform = Rect(400, 700, 120, 20)
platform_speed = 10

class Ball:
    def __init__(self, x, y, radius, speed, color):
        self.x = x
        self.y = y
        self.dx = speed
        self.dy = speed
        self.radius = radius
        self.color = color
        self.rect = Rect(self.x, self.y, self.rdius * 2, self.radius * 2)

    def reset(self):
        draw.circle(window, self.color, (self.x, self.y), self.radius)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

        if self.x >= 1000 - self.radius or self.x <= 0:
            self.dx *= -1
            self.dx += randint(1, 2)

        if self.y <= 0:
            self.dy *= -1
            self.dy += randint(1, 2)

def load_level_map(filename):
    bricks = list()
    with open(filename, 'r') as file:
        lines = [line for line in file.readlines()]
    for row_index, line in enumerate(lines):
        for col_index, char in enumerate(line):
            if char == '#':
                x = col_index * 50
                y = row_index * 50
                brick = Rect(x, y, 15, 15)
                bricks.append(brick)
    return bricks


class Boost:
    def __init__(self, x, y, c):
        self.rect = Rect(x, y, 25, 25)
        self.color = c

    def reset(self):
        self.rect.y += 3
        draw.rect(window, self.color, self.rect)

balls = list()
balls.append(Ball(200, 400, 10, 8, (255, 255, 255)))

lvl = load_level_map('lvl1.txt')
boosts = list()

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

    window.fill((0, 0, 0))
    draw.rect(window, (0, 0, 255), platform, border_radius=15)

    for brick in lvl:
        draw.rect(window, (255, 0, 0), brick)
        draw.rect(window, (0, 0, 0), (brick.x, brick.y, brick.w, brick.h), 2)

    for boost in boosts:
        boost.reset()
        if boost.rect.colliderect(platform):
            balls.append(Ball(boost.rect.x, boost.rect.y, 10, 8, (255, 255, 255)))
            boosts.remove(boost)

    for ball in balls:
        ball.reset()
        ball.update()
        if ball.rect.colliderect(platform):
            ball.dy *= -1
        colliding_indexes = ball.rect.collidelistall(lvl)
        if colliding_indexes:
            ball.dy *= -1
            if not randint(0, 10):
                boosts.append(Boost(ball.rect.x, ball.rect.y, (0, 255, 0)))
            for i in colliding_indexes:
                lvl.pop(i)
        if ball.y >= window.get_height():
            balls.remove(ball)

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_d]:
        platform.x += platform_speed
    if keys[K_a]:
        platform.x -= platform_speed

    if not balls:
        balls.append(Ball(400, 200, 10, 8, (255, 255, 255)))