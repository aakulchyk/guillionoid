#!/usr/bin/env python
import sys, pygame, random, GameArea, GameSound

global head

def sign(x):
    if (x>=0):  return 1
    else:       return -1

MoveCountValMax = 20
PathBin = "bin"
PathTextures = "textures"

class Object:
    sounds = GameSound.Sounds()
    def __init__(self):
        self.image = pygame.image.new()
        self.rect = self.image.get_rect()
        #self.sounds = GameSound.Sounds()

    def move(self):
        pass
    def paint(self, screen):
        screen.blit(self.image, self.rect)
    def collide(self, rect):
        return self.rect.colliderect(rect)

class Ball(Object):
    def __init__(self, area, x, y):
        self.initial_speed = 4
        self.__speed = [1, self.initial_speed]
        self.move_count = MoveCountValMax
        self.area = area
        self.image = pygame.image.load(PathBin + "/" + head)
        self.rect = self.image.get_rect()
        self.rect.move_ip( x, y)
        self.newrect = self.rect
        self.deleted = False

    def __del__(self):
	#find some sound
        pass
    
    def increase_speed(self):
        self.initial_speed += 1
        self.__speed[1] = self.initial_speed
    
    def start_move(self):
        self.newrect = self.rect.move(self.__speed)

        wall_collision = False
        if self.newrect.left < self.area.rect.left or self.newrect.right > self.area.rect.right:
            wall_collision = True
            self.__speed[0] = -self.__speed[0]
            self.move_count *= sign(self.__speed[0])
        if self.newrect.top < self.area.rect.top:
            wall_collision = True
            self.__speed[1] = -self.__speed[1]

    def finish_move(self):
        self.rect = self.rect.move(self.__speed)
        if self.rect.bottom > self.area.rect.bottom:
            self.deleted = True
    
    def check_collision(self, obj):
        if self.collide(obj):
            if self.newrect.left >= (obj.rect.right-obj.rect.width/3):
                self.__speed[0] += 2
            elif self.newrect.right <= (obj.rect.left+obj.rect.width/3):
                self.__speed[0] -=2
                    
            if self.__speed[1]>0 and self.newrect.bottom <= (obj.rect.top + obj.rect.height/3):
                self.__speed[1] = -self.__speed[1]
            elif self.__speed[1]<0 and self.newrect.top >= (obj.rect.bottom - obj.rect.height/3):
                self.__speed[1] = -self.__speed[1]

            obj.collide(self.newrect)
            self.move_count *= sign(self.__speed[0])
    
    def collide(self, rect):
        return self.newrect.colliderect(rect)

    def paint(self,screen):

        if self.__speed[0]>0:
            self.move_count -= 1
        elif self.__speed[0]<0:
            self.move_count += 1

        rotangle = 0
        if self.__speed[0]>0 and self.move_count <=0:
            self.move_count=MoveCountValMax
            rotangle = -90
        if self.__speed[0]<0 and self.move_count >=0:
            self.move_count=-MoveCountValMax
            rotangle = 90

        self.image = pygame.transform.rotate(self.image, rotangle)
        Object.paint(self, screen)

    


class Platform(Object):
    def __init__(self, area):
        self.area = area
        self.image = pygame.image.load(PathTextures + "/platform.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(area.rect.left+2, area.rect.bottom-self.rect.height-2)
        self.newrect = self.rect

    def start_move(self, dir, vert):
        self.newrect = self.rect.move(dir*6,vert*2)
    
    def finish_move(self):
        if self.area.rect.contains(self.newrect):
            self.rect = self.newrect
        
    def move(self, dir, vert):
        self.rect = self.rect.move(dir*6,vert*2)

    def control(self):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        dir = 0
        vert=0
        if key[pygame.K_LEFT]:
                dir =  -1
        if key[pygame.K_RIGHT]:
                dir =   1
        if key[pygame.K_UP]:
                vert =  -1
        if key[pygame.K_DOWN]:
                vert = 1
          
        self.start_move(dir, vert)

        
    def collide(self, rect):
        self.sounds.play("jump")
        return self.rect.colliderect(rect)
        

class Brick(Object):
    def __init__(self, x, y, i):
        self.life=0
        self.image = pygame.image.load(PathTextures + "/brick.png")
        self._hit_sound = "hit"
        self._destroy_sound = "destroy"
        self.rect = self.image.get_rect()
        self.deleted = False
        self.__index = i
        self.score=0

    def collide(self, rect):
        if Object.collide(self, self):
            self.life -= 1
            if self.life<1:
                self.deleted = True
                self.sounds.play(self._destroy_sound)
            else:
                self.sounds.play(self._hit_sound)

class GreenBrick(Brick):
    def __init__(self, x, y, i):
        Brick.__init__(self,x,y,i)
        self.image = pygame.image.load(PathTextures + "/greenbrick.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.life=3
        self.score=30
class BrownBrick(Brick):
    def __init__(self, x, y, i):
        Brick.__init__(self,x,y,i)
        self.image = pygame.image.load(PathTextures + "/brownbrick.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.life=2
        self.score=20
class BubbyBrick(Brick):
    def __init__(self, x, y, i):
        Brick.__init__(self,x,y,i)
        self.image = pygame.image.load(PathTextures + "/bubbybrick.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.life=1
        self.score=10
class GoldBrick(Brick):
    def __init__(self, x, y, i):
        Brick.__init__(self,x,y,i)
        self._destroy_sound = "gold"
        self.image = pygame.image.load(PathTextures + "/goldbrick.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.life=1
        self.score=50


def random_brick_at_random_place(area, i):
        maxx = area.rect.width//42-1
        maxy = area.rect.height//21-2
        type = random.randint(0,3)
        constructor_params =  x,y, i = random.randint(0, maxx)*42+area.rect.left, random.randint(0, maxy)*21+area.rect.top, i
        if type == 0:
            return GreenBrick(x,y, i)
        if type == 1:
            return BrownBrick(x,y, i)
        if type == 2:
            return BubbyBrick(x,y, i)
        if type == 3:
            return GoldBrick(x,y, i)

        return Brick( x,y,i )




