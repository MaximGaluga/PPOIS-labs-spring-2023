import random
from .util.vectorsprites import *
from src.shooter import *
from src.soundManager import *


class Rock(VectorSprite):
    largeRockType = 0
    mediumRockType = 1
    smallRockType = 2

    velocities = (1.5, 3.0, 4.5)
    scales = (2.5, 1.5, 0.6)

    rockShape = 1

    def __init__(self, stage, position, rockType):

        scale = Rock.scales[rockType]
        velocity = Rock.velocities[rockType]
        heading = Vector2d(random.uniform(-velocity, velocity), random.uniform(-velocity, velocity))

        # Ensure that the rocks don't just sit there or move along regular lines
        if heading.x == 0:
            heading.x = 0.1

        if heading.y == 0:
            heading.y = 0.1

        self.rockType = rockType
        pointlist = self.createPointList()
        newPointList = [self.scale(point, scale) for point in pointlist]
        VectorSprite.__init__(self, position, heading, newPointList)

    def createPointList(self):

        if Rock.rockShape == 1:
            pointlist = [(-4, -12), (6, -12), (13, -4), (13, 5), (6, 13), (0, 13), (0, 4), \
                         (-8, 13), (-15, 4), (-7, 1), (-15, -3)]

        elif Rock.rockShape == 2:
            pointlist = [(-6, -12), (1, -5), (8, -12), (15, -5), (12, 0), (15, 6), (5, 13), \
                         (-7, 13), (-14, 7), (-14, -5)]

        elif Rock.rockShape == 3:
            pointlist = [(-7, -12), (1, -9), (8, -12), (15, -5), (8, -3), (15, 4), (8, 12), \
                         (-3, 10), (-6, 12), (-14, 7), (-10, 0), (-14, -5)]

        elif Rock.rockShape == 4:
            pointlist = [(-7, -11), (3, -11), (13, -5), (13, -2), (2, 2), (13, 8), (6, 14), \
                         (2, 10), (-7, 14), (-15, 5), (-15, -5), (-5, -5), (-7, -11)]

        Rock.rockShape += 1
        if Rock.rockShape == 5:
            Rock.rockShape = 1

        return pointlist

    def move(self):
        VectorSprite.move(self)

        self.angle += 1


class Debris(Point):

    def __init__(self, position, stage):
        heading = Vector2d(random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5))
        Point.__init__(self, position, heading, stage)
        self.ttl = 50

    def move(self):
        Point.move(self)
        r, g, b = self.color
        r -= 5
        g -= 5
        b -= 5
        self.color = (r, g, b)


class Saucer(Shooter):
    largeSaucerType = 0
    smallSaucerType = 1

    velocities = (1.5, 2.5)
    scales = (1.5, 1.0)
    scores = (500, 1000)
    pointlist = [(-9, 0), (-3, -3), (-2, -6), (-2, -6), (2, -6), (3, -3), (9, 0), (-9, 0), (-3, 4), (3, 4), (9, 0)]
    maxBullets = 1
    bulletTtl = [60, 90]
    bulletVelocity = 5

    def __init__(self, stage, saucerType, ship):
        position = Vector2d(0.0, random.randrange(0, stage.height))
        heading = Vector2d(self.velocities[saucerType], 0.0)
        self.saucerType = saucerType
        self.ship = ship
        self.scoreValue = self.scores[saucerType]
        # stopSound("ssaucer")
        # stopSound("lsaucer")
        if saucerType == self.largeSaucerType:
            playSoundContinuous("lsaucer")
        else:
            playSoundContinuous("ssaucer")
        self.laps = 0
        self.lastx = 0

        newPointList = [self.scale(point, self.scales[saucerType]) for point in self.pointlist]
        Shooter.__init__(self, position, heading, newPointList, stage)

    def move(self):
        Shooter.move(self)

        if (self.position.x > self.stage.width * 0.33) and (self.position.x < self.stage.width * 0.66):
            self.heading.y = self.heading.x
        else:
            self.heading.y = 0

        self.fireBullet()

        if self.lastx > self.position.x:
            self.lastx = 0
            self.laps += 1
        else:
            self.lastx = self.position.x

    def fireBullet(self):
        if self.ship is not None:
            dx = self.ship.position.x - self.position.x
            dy = self.ship.position.y - self.position.y
            mag = math.sqrt(dx * dx + dy * dy)
            heading = Vector2d(self.bulletVelocity * (dx / mag), self.bulletVelocity * (dy / mag))
            position = Vector2d(self.position.x, self.position.y)
            shotFired = Shooter.fireBullet(self, heading, self.bulletTtl[self.saucerType], self.bulletVelocity)
            if shotFired:
                playSound("sfire")
