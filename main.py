import pygame
import sys
import config
import components
import population

def main():
    clock = pygame.time.Clock()
    pipeSpawnDelay = 225
    pop=population.Population(50)
    Maxscore = 0
    MaxScoreGen = 0
    MaxWeights=[]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Highest Score Achieved was: " + str(Maxscore) + ' in Gen ' + str(MaxScoreGen)+' with weights of '+ str(MaxWeights))
                pygame.quit()
                sys.exit()

        input=pygame.key.get_pressed()

        config.window.fill((0, 0, 0))

        config.ground.bg()




        pipeSpawnDelay -= 1
        if pipeSpawnDelay < 0:
            config.pipes.append(components.Pipes())
            pipeSpawnDelay = 225

        for pipe in config.pipes:
            pipe.update()
            pipe.draw(config.window)
            if config.pipes[0]==pipe:
                pipe.IsFirst=True
            else:
                pipe.IsFirst=False
            if pipe.delete():
                config.pipes.remove(pipe)

        text = config.font.render('Gen: ' + str(pop.gen), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (0, 0)
        config.window.blit(text, textRect)

        config.ground.draw(config.window)

        for p in pop.birds:
            #print(p.pipesPassed)
            if p.pipesPassed>Maxscore:
                Maxscore=p.pipesPassed
                MaxScoreGen=pop.gen
                MaxWeights=p.brain.weights
            p.update(input)
            p.look(config.pipes)
            p.draw(config.window)
        pop.update()

        pygame.display.update()
        clock.tick(60)


main()