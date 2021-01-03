import os
import neat

from src.entities.game_state import GameState

gen = 0


def eval_genomes(genomes, config):
    global gen
    GameState(gen, genomes=genomes, config=config).run()


def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_file
    )

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "src", "config", 'config-feedforward.txt')
    run(config_path)
