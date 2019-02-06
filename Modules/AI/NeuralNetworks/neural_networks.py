''' NEURAL NETWORSK
Author: Pawel Brysch
Date: Jan 2019

Module contains classes which allow to build neural networks prepared to work as decision unit in cars, which are
learned to drive autonomously.

...
Classes
----------
InputTransformator:
    Class, which converts car's attributes to data acceptable by KERAS's neural networks's input layers.
OutputTransformator:
    Class, which converts KERAS's neural networks's output to car's attributes.
Brain:
    Neural network.
'''

from keras.models import Sequential
from keras.layers.core import Dense
from Modules.General.general_types import Move
import numpy as np


class InputTransformator:
    ''' Converts car's attributes to data acceptable by KERAS's neural networks's input layers.
        This is only selected example among possible transformators. You can write another.

    ...
    Attributes
    ----------
    inputArchitecturalFactor: int
        how many neurons should neural networks has in its first layer in order to connect with this object.
        To be set in external module (e.q. settings). In our case this attribute should be equal to the number of
        rangefinders in the car.
    '''
    inputArchitecturalFactor = None

    @classmethod
    def TransformedInput(cls, car):
        ''' See: class description

        :param car: Trainable car
        :return: list
        '''

        # Data will consist of distances between car and environment.
        listOfDistances = []
        for rangeFinder in car.radar.listOfRangefinders:
            listOfDistances.append(rangeFinder.distance)

        # Return as a structure which KERAS accepts.
        return np.array([listOfDistances])


class OutputTransformator:
    ''' Converts KERAS's neural networks's output to car's attributes.
        This is only selected example among possible transformators. You can write another.

    ...
    Attributes
    ----------
    outputArchitecturalFactor: int
        how many neurons should neural network has in its output layer to connect with this object. In our case this
        is 3, because we have 3 decisions we can take.
    '''
    outputArchitecturalFactor = 3

    @classmethod
    def TransformedOutput(cls, output):
        ''' Prepare data from brain to be passed to car.

        :param output: list
            output of neural network
        :return: Move
        '''

        # Get proper output from KERAS's output structure.
        output = output[0]

        # The decision depends on which element of output is maximal.
        choice = np.argmax(output)
        if choice == 0:
            result = Move.RIGHT
        elif choice == 1:
            result = Move.NONE
        elif choice == 2:
            result = Move.LEFT

        return result


class Brain:
    ''' Neural network with additional features.

    ...
    Attributes
    ----------
    neuralNetwork: keras.models.Sequential
        core attribute. Proper neural network.
    inputTransformator: InputTransformator
        see: "InputTransformator" documentation
    outputTransformator: OutputTransformator:
        see: "OutputTransformator" documentation
    deepArchitecturalFactors: list
        list of numbers of neurons in hidden layers of neural network excluding last layer. E.q. if you want to your
        network has consecutively 9,2,7,5 neuron in 1st (input), 2nd, 3rd and 4st layer, this attribute should be [2,7].
        Rest of numbers (in this case 9 and 5 depends of connected transformators (input and output respectively).
    '''

    neuralNetwork = None
    inputTransformator = None
    outputTransformator = None
    deepArchitecturalFactors = []

    @classmethod
    def Create(cls, inputTransformator, outputTransformator):
        ''' Prepare brain for future work. This method has to be used before experiment.
        '''

        # Set transformators
        cls.inputTransformator = inputTransformator
        cls.outputTransformator = outputTransformator

        # Create full architecture from all necessary data.
        architecture = [inputTransformator.inputArchitecturalFactor] + cls.deepArchitecturalFactors + [outputTransformator.outputArchitecturalFactor]

        # Create right neural network.
        cls.CreateNeuralNetwork(architecture)

    @classmethod
    def CreateNeuralNetwork(cls, architecture):
        ''' Create right neural network.

        :param architecture: list
            list of numbers of neurons in consecutive layers of neural network. E.q. if you want to your network has
            consecutively 9,2,7,5 neuron in 1st (input), 2nd, 3rd and 4st layer, this attribute should be [9,2,7,5]
            exactly.
        '''

        # Initialize neural network. Notice that first element from architecture is passed as "input_shape", not as a
        # number of neurons in layer.
        cls.neuralNetwork = Sequential([Dense(architecture[1], input_shape=(architecture[0],), activation='relu'),
                                         Dense(architecture[2], activation='relu'),
                                         Dense(architecture[3], activation='softmax')])

    def SetPattern(self, pattern):
        ''' Set weights on neural network.
            Method is complicated. It is due fact, that KERAS store weights in relatively complicated structures.
            Hence, conversion from standard lists to that structures is complicated.

        :param pattern: Pattern
            see: "Pattern" class documentation in "genetics" module
        '''

        # Get weights from neural network in order to get its structure shape.
        weights = self.neuralNetwork.get_weights()

        # Put elements from list of weights (pattern.wages) into appropriate slots (in KERAS's "weights" structure).
        index = 0
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                try:
                    for k in range(len(weights[i][j])):
                        weights[i][j][k] = pattern.wages[index]
                        index += 1
                except:
                    weights[i][j] = pattern.wages[index]
                    index += 1

        # Set changed weights to neural network.
        self.neuralNetwork.set_weights(weights)

    def CalculateMove(self, car):
        ''' Make decision about turning of car.

        :param car: TrainableCar
        :return: Move
        '''

        # Conduct signal through input transformator
        input = self.inputTransformator.TransformedInput(car)

        # Conduct signal through neural network
        output = self.neuralNetwork.predict(input)

        # Conduct signal through output transformator
        move = self.outputTransformator.TransformedOutput(output)

        return move
