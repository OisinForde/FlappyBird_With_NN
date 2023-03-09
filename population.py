import  components
import config
import random

class Population:
    def __init__(self,popSize):
        self.popSize=popSize
        self.birds=[]
        self.deadBirds=[]
        self.FittestBird=[]
        self.gen=1

        for i in range(self.popSize):
            self.birds.append(components.Player())

    def FindFittestBird(self):
        self.deadBirds.sort(key = lambda x : x.points)
        self.deadBirds.reverse()

        for bird in self.deadBirds:
            #print(bird.points)
            if (self.deadBirds.index(bird)<(self.popSize/2)):
                if bird.points>-10:
                    self.FittestBird.append(bird)
                else:
                    self.FittestBird.append(components.Player())

    def update(self):
        if len(self.FittestBird)>0:
            self.FittestBird[0].colour=(255,0,0)
            self.FittestBird[0].colour=(255,0,0)

        self.display()

        for bird in self.birds:
            if self.birds.index(bird)+1>self.popSize:
                self.birds.remove(bird)
            if bird.alive==False:
                self.deadBirds.append(bird)
                self.birds.remove(bird)
        #print("Dead: ",len(self.deadBirds))


        if len(self.deadBirds) == self.popSize:
            self.new_gen()
            self.gen += 1
        #print("Alive: ",len(self.birds))

    def display(self):

        if len(self.birds)>0:
            self.birds.sort(key=lambda x: x.points)
            self.birds.reverse()
            '''text = config.font.render('Score: ' + str(self.birds[0].points), True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.topright = (config.window.get_width(),0)
            config.window.blit(text, textRect)'''

            scoreText=config.font.render(str(self.birds[0].pipesPassed),True,(255,255,255))
            scoreRect=scoreText.get_rect()
            scoreRect.center=(config.window.get_width()/2,650)
            config.window.blit(scoreText,scoreRect)

    def cross_over(self,A,B):
        cutLocationA= round(len(A.brain.weights) * random.uniform(0, 1))
        child1=components.Player()
        child2=components.Player()
        Parent1=components.Player()
        Parent2=components.Player()

        child1.brain.weights[cutLocationA:],child1.brain.weights[:cutLocationA]=A.brain.weights[cutLocationA:],B.brain.weights[:cutLocationA]
        child2.brain.weights[:cutLocationA], child2.brain.weights[cutLocationA:] = A.brain.weights[:cutLocationA], B.brain.weights[cutLocationA:]


        Parent1.brain=A.brain
        Parent2.brain=B.brain

        self.birds.append(child1)
        self.birds.append(child2)
        self.birds.append(Parent1)
        self.birds.append(Parent2)

    def new_gen(self):
        #print(len(self.FittestBird))
        self.FindFittestBird()
        self.deadBirds.clear()
        self.birds.clear()
        #random.shuffle(self.FittestBird)
        self.FittestBird.sort(key=lambda x: x.points)
        self.FittestBird.reverse()
        for i in range(0,len(self.FittestBird),2):
            if self.FittestBird[i]!=self.FittestBird[-1]:
                self.cross_over(self.FittestBird[i],self.FittestBird[i+1])
            else:
                self.cross_over(self.FittestBird[i], self.FittestBird[0])

        for bird in self.birds:
            x=random.randint(0,4)
            bird.brain.weights[x]=bird.brain.weights[x]*0.01


        config.pipes.clear()