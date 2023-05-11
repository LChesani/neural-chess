from Arena import *
import numpy as np
from MCTS import *
from _chess.ChessGame import ChessGame as Game
from _chess.pytorch.NNet import NNetWrapper as nn
from utils import *





args = dotdict({
    'numIters': 100,
    'numEps': 25,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.55,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

g = Game()
nnet1 = nn(g)
nnet2 = nn(g)
print('loading models')
nnet1.load_checkpoint('./temp/', 'temp.pth.tar')
nnet2.load_checkpoint('./temp/', 'temp.pth.tar')

pmcts = MCTS(g, nnet1, args)
nmcts = MCTS(g, nnet2, args)




arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                          lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), g)
pwins, nwins, draws = arena.playGames(args.arenaCompare)