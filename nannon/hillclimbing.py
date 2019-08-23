import numpy as np
import scipy.special
from nannon import *

def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1.0 - x)

class HCNetwork:
    def __init__(self, n_input, n_hidden, n_output, type):
        # Set number of nodes in each input, hidden, output layer
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_output = n_output

        # We link the weight matrices below.
        # Weights between input and hidden layer = weights_ih
        # Weights between hidden and output layer = weights_ho
        # Weights inside the arrays are w_i_j, where the link is from node i to
        # node j in the next layer

        #   w11 w21
        #   w12 w22 etc...
        #
        # Weights are sampled from a normal probability distribution centered at
        # zero with a standard deviation related to the number of incoming links
        # into a node: 1/√(number of incoming links).
        if type == 0:
            self.weights_ih = np.zeros((self.n_hidden, self.n_input))
            self.weights_ho = np.zeros((self.n_output, self.n_hidden))
        else: #add random noise to passed-in weights
            random_init_range = pow(self.n_input, -0.5)
            self.weights_ih = type.weights_ih+np.random.normal(0.0, random_init_range,
                                                    (self.n_hidden, self.n_input))
            self.weights_ho = type.weights_ho+np.random.normal(0.0, random_init_range,
                                                    (self.n_output, self.n_hidden))


    # Use to train the neural network with hill climbing.
    def train(self,learning_rate):
        #create a version of itself plus noises to the weights
        other = HCNetwork(self.n_input,self.n_hidden,self.n_output,self)
        # Step 1: play a tournament
        def playnet1(pos,roll):
            candidates = [];
            for move in legal_moves(pos,roll):
                potential = make_move(pos,move,roll)
                score = self.query(pos_to_list(potential))
                candidates.append((move,score))
            best_move, _ = max(candidates, key=lambda x: x[1])
            return make_move(pos, best_move, roll)

        def playnet2(pos,roll):
            candidates = [];
            for move in legal_moves(pos,roll):
                potential = make_move(pos,move,roll)
                score = other.query(pos_to_list(potential))
                candidates.append((move,score))
            best_move, _ = max(candidates, key=lambda x: x[1])
            return make_move(pos, best_move, roll)

        result = play_tourn(playnet1,playnet2)

        # Step 2: Update the weights if improved
        if result < 0.5:
            self.weights_ho = self.weights_ho*(1-learning_rate)+ other.weights_ho*learning_rate
            self.weights_ih = self.weights_ih*(1-learning_rate)+ other.weights_ih*learning_rate




    # Query the neural network with simple feed-forward.
    def query(self, inputs_list):
        # Convert inputs list to 2d array.
        inputs = np.array(inputs_list, ndmin=2).T
        # Calculate signals into hidden layer.
        hidden_inputs = np.dot(self.weights_ih, inputs)
        # Calculate the signals emerging from hidden layer.
        hidden_outputs = sigmoid(hidden_inputs)
        # Calculate signals into final output layer.
        final_inputs = np.dot(self.weights_ho, hidden_outputs)
        # Calculate the signals emerging from final output layer.
        final_outputs = sigmoid(final_inputs)
        return final_outputs
