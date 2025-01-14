import random
from math import *
from .util.vectorsprites import *
from .shooter import *
from .soundManager import *


class Ship(Shooter):

    # Class attributes
    acceleration = 0.2
    decelaration = -0.005
    maxVelocity = 10
    turnAngle = 6
    bulletVelocity = 13.0
    maxBullets = 4
    bulletTtl = 35

    def __init__(self, stage):

        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.thrustJet = ThrustJet(stage, self)
        self.shipDebrisList = []
        self.visible = True
        self.inHyperSpace = False
        pointlist = [(0, -10), (6, 10), (3, 7), (-3, 7), (-6, 10)]

        Shooter.__init__(self, position, heading, pointlist, stage)

    def draw(self):
        if self.visible:
            if not self.inHyperSpace:
                VectorSprite.draw(self)
            else:
                self.hyperSpaceTtl -= 1
                if self.hyperSpaceTtl == 0:
                    self.inHyperSpace = False
                    self.color = (255, 255, 255)
                    self.thrustJet.color = (255, 255, 255)
                    self.position.x = random.randrange(0, self.stage.width)
                    self.position.y = random.randrange(0, self.stage.height)
                    position = Vector2d(self.position.x, self.position.y)
                    self.thrustJet.position = position

        return self.transformed_point_list

    def rotateLeft(self):
        self.angle += self.turnAngle
        self.thrustJet.angle += self.turnAngle

    def rotateRight(self):
        self.angle -= self.turnAngle
        self.thrustJet.angle -= self.turnAngle

    def increaseThrust(self):
        playSoundContinuous("thrust")
        if math.hypot(self.heading.x, self.heading.y) > self.maxVelocity:
            return

        dx = self.acceleration * math.sin(radians(self.angle)) * -1
        dy = self.acceleration * math.cos(radians(self.angle)) * -1
        self.changeVelocity(dx, dy)

    def decreaseThrust(self):
        stopSound("thrust")
        if (self.heading.x == 0 and self.heading.y == 0):
            return

        dx = self.heading.x * self.decelaration
        dy = self.heading.y * self.decelaration
        self.changeVelocity(dx, dy)

    def changeVelocity(self, dx, dy):
        self.heading.x += dx
        self.heading.y += dy
        self.thrustJet.heading.x += dx
        self.thrustJet.heading.y += dy

    def move(self):
        VectorSprite.move(self)
        self.decreaseThrust()

    def explode(self):
        pointlist = [(0, -10), (6, 10)]
        self.addShipDebris(pointlist)
        pointlist = [(6, 10), (3, 7)]
        self.addShipDebris(pointlist)
        pointlist = [(3, 7), (-3, 7)]
        self.addShipDebris(pointlist)
        pointlist = [(-3, 7), (-6, 10)]
        self.addShipDebris(pointlist)
        pointlist = [(-6, 10), (0, -10)]
        self.addShipDebris(pointlist)


    def addShipDebris(self, pointlist):
        heading = Vector2d(0, 0)
        position = Vector2d(self.position.x, self.position.y)
        debris = VectorSprite(position, heading, pointlist, self.angle)

        self.stage.add_sprite(debris)

        centerX = debris.boundingRect.centerx
        centerY = debris.boundingRect.centery

        debris.heading.x = ((centerX - self.position.x) +
                            0.1) / random.uniform(20, 40)
        debris.heading.y = ((centerY - self.position.y) +
                            0.1) / random.uniform(20, 40)
        self.shipDebrisList.append(debris)


    def fireBullet(self):
        if self.inHyperSpace == False:
            vx = self.bulletVelocity * math.sin(radians(self.angle)) * -1
            vy = self.bulletVelocity * math.cos(radians(self.angle)) * -1
            heading = Vector2d(vx, vy)
            Shooter.fireBullet(self, heading, self.bulletTtl,
                               self.bulletVelocity)
            playSound("fire")

    def enterHyperSpace(self):
        if not self.inHyperSpace:
            self.inHyperSpace = True
            self.hyperSpaceTtl = 100
            self.color = (0, 0, 0)
            self.thrustJet.color = (0, 0, 0)


class ThrustJet(VectorSprite):
    pointlist = [(-3, 7), (0, 13), (3, 7)]

    def __init__(self, stage, ship):
        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.accelerating = False
        self.ship = ship
        VectorSprite.__init__(self, position, heading, self.pointlist)

    def draw(self):
        if self.accelerating and self.ship.inHyperSpace == False:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)

        VectorSprite.draw(self)
        return self.transformed_point_list
