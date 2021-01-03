import neat
import pygame

from src.entities.background import Background
from src.entities.bird import Bird
from src.entities.floor import Floor
from src.entities.pipe import Pipe


class GameState:
    def __init__(self, gen, **kwargs):
        pygame.display.set_caption("Flappy Bird")

        self.__width = 288
        self.__height = 512
        self.__score = 0
        self.__running = True
        self.__debug = True
        self.__win = pygame.display.set_mode((self.__width, self.__height))
        self.__clock = pygame.time.Clock()
        self.__genomes = kwargs.get('genomes')
        self.__config = kwargs.get('config')
        gen += 1

        self.__nets = []
        self.__ge = []
        self.__birds = []
        self.__pipes = [Pipe(self.__width)]
        self.__remove = []

        self.__floor = Floor(self.__height)
        self.__background = Background()

        self.bind_genomes()

    def bind_genomes(self):
        for genome_id, genome in self.__genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, self.__config)
            self.__nets.append(net)
            self.__birds.append(Bird(100, 266))
            self.__ge.append(genome)

    def __draw(self, pipe_ind):
        self.__background.draw(self.__win)
        self.__floor.draw(self.__win)

        for pipe in self.__pipes:
            pipe.draw(self.__win)

        for bird in self.__birds:
            bird.draw(self.__win)

            if self.__debug:
                try:
                    pygame.draw.line(self.__win, (255, 0, 0),
                                     (bird.get_x() + bird.get_img().get_width() / 2,
                                      bird.get_y() + bird.get_img().get_height() / 2),
                                     (self.__pipes[pipe_ind].get_x() + self.__pipes[
                                         pipe_ind].get_pipe_top().get_width() / 2,
                                      self.__pipes[pipe_ind].get_pipe_top_y()), 5)
                    pygame.draw.line(self.__win, (255, 0, 0),
                                     (bird.get_x() + bird.get_img().get_width() / 2,
                                      bird.get_y() + bird.get_img().get_height() / 2),
                                     (self.__pipes[pipe_ind].get_x() + self.__pipes[
                                         pipe_ind].get_pipe_bottom().get_width() / 2,
                                      self.__pipes[pipe_ind].get_pipe_bottom_y()), 5)
                except:
                    pass

        pygame.display.update()

    def __check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                pygame.quit()
                quit()
                break

    def __check_next_pipe(self):
        pipe_ind = 0
        if len(self.__birds) > 0:
            if len(self.__pipes) > 1 and self.__birds[0].get_x() > self.__pipes[0].get_x() + self.__pipes[0].get_pipe_top().get_width():
                pipe_ind = 1
        return pipe_ind

    def __play_decision(self, pipe_ind):
        for x, bird in enumerate(self.__birds):
            self.__ge[x].fitness += 0.1
            bird.move()

            output = self.__nets[self.__birds.index(bird)].activate(
                (
                    bird.get_y(),
                    abs(bird.get_y() - self.__pipes[pipe_ind].get_height()),
                    abs(bird.get_y() - self.__pipes[pipe_ind].get_pipe_bottom_y())
                )
            )

            if output[0] > 0.5:
                bird.jump()

    def __check_collide(self):
        add_pipe = False
        for pipe in self.__pipes:
            for bird in self.__birds:
                if pipe.collide(bird):
                    self.__ge[self.__birds.index(bird)].fitness -= 1
                    self.__nets.pop(self.__birds.index(bird))
                    self.__ge.pop(self.__birds.index(bird))
                    self.__birds.pop(self.__birds.index(bird))

            if pipe.get_x() + pipe.get_pipe_top().get_width() < 0:
                self.__remove.append(pipe)

            if not pipe.has_passed() and pipe.get_x() < bird.get_x():
                pipe.set_passed(True)
                add_pipe = True

        if add_pipe:
            self.__score += 1
            for genome in self.__ge:
                genome.fitness += 5
            self.__pipes.append(Pipe(self.__width))

        for r in self.__remove:
            self.__pipes.remove(r)

    def __remove_deads(self):
        for bird in self.__birds:
            if bird.get_y() + bird.get_img().get_height() - 10 >= self.__height - 50 or bird.get_y() < -50:
                self.__nets.pop(self.__birds.index(bird))
                self.__ge.pop(self.__birds.index(bird))
                self.__birds.pop(self.__birds.index(bird))

    def run(self):
        while self.__running and len(self.__birds) > 0:
            self.__remove = []
            self.__clock.tick(30)
            self.__check_event()
            pipe_ind = self.__check_next_pipe()
            self.__play_decision(pipe_ind)
            self.__check_collide()
            self.__remove_deads()
            self.__draw(pipe_ind)
