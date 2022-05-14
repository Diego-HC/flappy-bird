import pygame as pg
from random import randint

class Bird:
    def __init__(self, pos, screen) -> None:
        self.screen = screen

        self.pos = pos
        self.width = 80
        self.height = 50
        self.speed = 1
        self.accel = 1

    def drawBird(self):
        pg.draw.rect(self.screen, [255, 255, 0], pg.Rect(100, self.pos, self.width, self.height))

    def reset(self, pos):
        self.pos = pos
        self.speed = 1
        self.accel = 1

    def checkRoofCeil(self):
        if self.pos <= 0 or self.pos >= 720:
            return True
        else:
            return False
    
    def moveBird(self):
        self.pos += self.speed
        self.speed += self.accel

    def changeVel(self):
        self.speed = -10

class Pipes:
    def __init__(self, screen, pos) -> None:
        self.screen = screen
        self.pos = pos
        self.height = randint(200, 720 - 200)
        self.height2 = randint(200, 720 - 200)
        self.width = 150

    def drawPipes(self):
        pg.draw.rect(self.screen, (0, 255, 0), pg.Rect(self.pos, 0, self.width, self.height))
        pg.draw.rect(self.screen, (0, 255, 0), pg.Rect(self.pos, self.height + 200, self.width, 720 - 200 - self.height))

        pg.draw.rect(self.screen, (0, 255, 0), pg.Rect(self.pos + 400, 0, self.width, self.height2))
        pg.draw.rect(self.screen, (0, 255, 0), pg.Rect(self.pos + 400, self.height2 + 200, self.width, 720 - 200 - self.height2))

    def movePipes(self):
        self.pos -= 5
        if self.pos + self.width <= 0:
            self.pos = self.pos + 400
            self.height = self.height2
            self.height2 = randint(200, 720 - 200)

    def checkCollision(self, bird):
        if pg.Rect.colliderect(pg.Rect(self.pos, 0, self.width, self.height), pg.Rect(100, bird.pos, bird.width, bird.height)) or pg.Rect.colliderect(pg.Rect(self.pos, self.height + 200, self.width, 720 - 200 - self.height), pg.Rect(100, bird.pos, bird.width, bird.height)):
            return True
        else:
            return False

if __name__ == '__main__':
    pg.init()
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 720
    WHITE = (255, 255, 255)
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pg.display.set_caption('Flappy Bird')
    clock = pg.time.Clock()

    bird = Bird(SCREEN_HEIGHT//2 - 25, screen)
    pipes = Pipes(screen, 600)
    screen.fill(WHITE)
    bird.drawBird()
    pipes.drawPipes()
    pg.display.flip()

    game = True
    started = False

    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT: game = False
        
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and  not started:
            started = True

        if started:
            if bird.checkRoofCeil():
                bird.reset(SCREEN_HEIGHT//2 - 25)
                started = False

            if pipes.checkCollision(bird):
                bird.reset(SCREEN_HEIGHT//2 - 25)
                pipes = Pipes(screen, 600)
                started = False
                
            if keys[pg.K_UP]:
                bird.changeVel()
            
            screen.fill(WHITE)
            bird.moveBird()
            pipes.movePipes()
            bird.drawBird()
            pipes.drawPipes()

        pg.display.flip()
        clock.tick(60)