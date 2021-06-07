import pygame
import math
import random
import time

SCREEN_WIDTH = 1980
SCREEN_HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = pygame.font.SysFont('Comic Sans MS', 30)

TARGETS_MAX = 3
TARGET_RADIUS = 50
TARGET_TIME = 3
GAME_TIME = 30

running = True
targets = []


class Target:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

    def checkHit(self, x, y):
        return math.sqrt((x-self.x)**2 + (y-self.y)**2) < TARGET_RADIUS

    def checkTime(self, timeNow):
        return timeNow - self.time > TARGET_TIME


def addTarget():
    x = random.randint(TARGET_RADIUS, SCREEN_WIDTH - TARGET_RADIUS)
    y = random.randint(TARGET_RADIUS, SCREEN_HEIGHT - TARGET_RADIUS)

    targets.append(Target(x, y, time.time()))


score = 0
startTime = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for t in targets:
                if t.checkHit(x, y):
                    targets.remove(t)
                    score += 1
                
    for t in targets:
        if t.checkTime(time.time()):
            targets.remove(t)
            score -= 1

    for i in range(TARGETS_MAX - len(targets)):
        addTarget();

    screen.fill((0, 0, 0))

    for t in targets:
        pygame.draw.circle(screen, (0, 0, 255 - 255 * (time.time()-t.time + TARGET_TIME) / 8), (t.x, t.y), TARGET_RADIUS)

    timeElapsed = time.time() - startTime
    if(timeElapsed > GAME_TIME):
        running = False

    screen.blit(font.render(str(score), False, (255, 255, 255)), (SCREEN_WIDTH/2, 25))
    screen.blit(font.render(str(round(GAME_TIME - timeElapsed,2)), False, (255, 255, 255)), (SCREEN_WIDTH/2, 50))

    pygame.display.flip()


pygame.quit()

print("Your score is:")
print(score)
