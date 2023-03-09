import random

import pygame
import config
import NN

class Ground:
    def __init__(self,winHeight):
        self.colour=(255,255,255)
        self.groundLevel=winHeight-150
        self.img=config.bg
        self.groundImg=config.ground
    def bg(self):
        config.window.blit(self.img, (0, 0))
    def draw(self,win):

        config.window.blit(self.groundImg, (0,self.groundLevel))
        #pygame.draw.rect(win,self.colour,(0,self.groundLevel,win.get_width(),10))

class Pipes:
    def __init__(self):
        self.colour=(255,255,255)
        self.width=52
        self.x=config.window.get_width()+self.width
        self.height=random.randint(150,350)
        self.gap=config.gap
        self.bottomPipe=pygame.Rect((self.x,config.ground.groundLevel-self.height),(self.width,self.height))
        self.topPipe=pygame.Rect((self.x,0),(self.width,self.bottomPipe.top-self.gap))

        self.IsFirst=False
        self.cleared=False

        self.pipeVel=2

        self.topPipeimg=config.topImg
        self.bottomPipeimg=config.bottomImg

    def update(self):
        self.bottomPipe.x-=1
        self.topPipe.x-=1



    def delete(self):
        if (self.bottomPipe.right+10) < 0:
            return True
    def draw(self,win):
        config.window.blit(self.topPipeimg,(self.topPipe.left,self.topPipe.bottom-550))
        config.window.blit(self.bottomPipeimg, self.bottomPipe)


class Player:
    def __init__(self):

        self.x,self.y=50,random.randint(100,400)
        self.rect=pygame.Rect(self.x,self.y,34,34)
        self.colour=(random.randint(100,255),random.randint(100,255),random.randint(100,255))

        self.imgs=[config.birdUp,config.birdMid,config.birdDown]
        self.imgIndex = 0
        self.img=self.imgs[self.imgIndex]
        self.imgcooldown=10

        '''self.angle=0
        self.FlapAngle=50
        self.angleVel=0
        self.angleAccel=4
        self.angleDeaceel=-2
        
    

        self.MaxAngleVel=5
        self.MinAngelVel=-3'''

        self.angle = 0

        self.vel = 0.0
        self.flap = False
        self.alive = True

        self.nextPipe=0
        self.pipesPassed=0

        self.points=0
        self.vision=[0,0,0,0,0,0]#Distance to pipe, distance to ground
        self.brain=NN.Percreptron()



    def update(self,input):

        '''if self.vel<0:
            if self.angleVel<self.MaxAngleVel:
                self.angleVel+=self.angleAccel

            if self.angle<self.FlapAngle:
                self.angle+=self.angleVel
            print(self.angleVel)
        else:
            if self.angleVel>self.MinAngelVel:
                self.angleVel+=self.angleDeaceel
            if self.angle>-90:
                self.angle += self.angleVel'''


        self.imgcooldown-=1
        if self.imgcooldown==0:
            self.imgcooldown=10
            if self.imgIndex!=2:
                self.img=pygame.transform.rotate(self.imgs[self.imgIndex],self.angle)
            else:
                self.img=pygame.transform.rotate(self.imgs[0],self.angle)


        self.vision[5]=self.vel
        if self.brain.foward_propagration(self.vision)==1:
            self.bird_flap()
        if not(self.ground_collison() or self.pipe_collison(config.pipes)):
            # Gravity
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

        self.point()
        if self.sky_collision()==True:
            self.points-=1

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap=True
            self.vel=-6
        if self.vel>=3:
            self.flap=False

    def draw(self,win):
        #pygame.draw.rect(win, self.colour, self.rect)
        config.window.blit(self.img,(self.rect.left,self.rect.top+4))


    def pipe_collison(self,pipes):
        for pipe in pipes:
            if self.rect.colliderect(pipe.bottomPipe) or self.rect.colliderect(pipe.topPipe):
                self.alive=False
                self.points-=10
                return True

    def sky_collision(self):
        return bool(self.rect.y+30 < 30)


    def ground_collison(self):
        if self.rect.y+30>=config.ground.groundLevel:
            self.alive=False
            self.points =0
            return True

    def point(self):
        config.pipes.sort(key=lambda x: x.bottomPipe.x)
        for pipe in config.pipes:
            if pipe.IsFirst==True or self.rect.x>=config.pipes[self.nextPipe].bottomPipe.x+50:
                self.nextPipe=config.pipes.index(pipe)
            if self.rect.right>self.vision[self.nextPipe] and pipe.cleared==False:
                self.pipesPassed += 1
                pipe.cleared=True
                self.points += 10

        if (self.vision[4]-self.rect.height-5>0) and (self.vision[3]+self.rect.height+5>0):
            self.points+=2
        else:
            self.points-=.5



    def look(self,pipes):
        if len(config.pipes)>0:
            self.vision[0]=pipes[self.nextPipe].bottomPipe.x-(self.rect.x)+pipes[self.nextPipe].width*1.5
            pygame.draw.line(config.window,(0,255,0),self.rect.center,(self.vision[0],self.rect.y+(self.rect.height/2)))
        else:
            self.vision[self.nextPipe]=config.window.get_width()


        self.vision[1]=config.ground.groundLevel-self.rect.bottom+6
        pygame.draw.line(config.window,(0,255,0),self.rect.center,(self.rect.x+(self.rect.width/2),config.ground.groundLevel))

        self.vision[2]=-(0-self.rect.top)
        pygame.draw.line(config.window,(0,255,0),self.rect.center,(self.rect.x+(self.rect.width/2),0))

        if len(config.pipes)>0:
            self.vision[3] = -(pipes[self.nextPipe].topPipe.bottom - self.rect.top)
            pygame.draw.line(config.window, (0, 255, 0), self.rect.center,
                             (self.vision[0], self.rect.top - self.vision[3]))
        else:
            self.vision[self.nextPipe]=0

        if len(config.pipes)>0:
            self.vision[4] = (pipes[self.nextPipe].bottomPipe.top - self.rect.bottom)
            pygame.draw.line(config.window, (0, 255, 0), self.rect.center,
                             (self.vision[0], self.rect.bottom + self.vision[4]))
        else:
            self.vision[self.nextPipe]=0

    def think(self):
        pass

