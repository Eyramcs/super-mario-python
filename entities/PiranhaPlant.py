import pygame.transform

from classes.Animation import Animation
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase


class PiranhaPlant(EntityBase):

    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(PiranhaPlant, self).__init__(y, x - 1, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("Piranha_Plant1").image,
                self.spriteCollection.get("Piranha_Plant2").image
            ]
        )
        self.screen = screen
        self.type = "Mob"
        self.dashboard = level.dashboard
        self.collision = Collider(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound
        self.textPos = Vec2D(0, 0)

    def update(self, camera):
        if self.alive:
            self.applyGravity()
            self.drawPiranha_Plant(camera)
            self.checkEntityCollision()
        else:
            self.onDead()

    def onDead(self):
        pygame.transform.flip(self.animation, False, True)
        

    def drawPiranha_Plant(self, camera):
        self.screen.blit(self.animation.image, (self.rect.x + camera.x, self.rect.y))
        self.animation.update()

    def _onCollisionWithMob(self, mob, collisionState):
        if collisionState.isColliding and mob.bouncing:
            self.alive = False
            self.sound.play_sfx(self.sound.brick_bump)

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)
