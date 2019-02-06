# Applying Evolutionary Artificial Neural Networks using Python

A 2D Unity simulation in which cars learn to navigate themselves through different courses. The cars are steered by a feedforward Neural Network. The weights of the network are trained using a modified genetic algorithm.
There is brief presentation on the Youtube. !!!link do youtube'a!!! 
It is highly recommended to watch this before further reading.


!!!DEMO!!!


## The Simulation

Cars have to navigate through a course without touching the walls or any other obstacles of the course. A car has three front-facing sensors which measure the distance to obstacles in a given direction. The readings of these sensors serve as the input of the car's neural network. Each sensor points into a different direction, covering a front facing range of approximately 70 degrees. The output of the Neural Network then determines the car’s current turning force.


!!!CAR!!!


If you would like to tinker with the parameters of the simulation, you can do so in the !!!SETTINGS!!! module. If you would simply like to run the simulation with default parameters, you can run [Applying_EANNs_using_Python/Scripts/](Applying_EANNs_using_Python/Scripts/perform_experiments.py) script. To show the results you can run !!!show_single_album!!! script.

## Simulation environment.
!!!


## The Neural Network

The Neural Network used is a standard, fully connected, feedforward Neural Network. It comprises 4 layers: an input layer with 3 neurons, two hidden layers with 4 and 3 neurons respectively and an output layer with 3 neurons.
The core of neural network is model adopted from [Keras](https://github.com/keras-team/keras) library
The code for the Neural Network can be found at !!!NEURAL NETWORKS!!!


## Training the Neural Network

The weights of the Neural Network are trained using an Evolutionary Algorithm known as the Genetic Algorithm.

At first there are N randomly initialised cars spawned. The best cars are then selected to be recombined with each other, creating new "offspring" cars. These offspring cars then form a new population of N cars and are 
also slightly mutated in order to inject some more diversity into the population. The newly created population of cars then tries to navigate the course again and the process of evaluation, selection, recombination and mutation starts again. One complete cycle from the evaluation of one population to the evaluation of the next is called a generation.

Methods listed above (evaluation, selection and recombination) are adopted from [DEAP](https://github.com/DEAP). The same with tools necessary to build data structures used in algorithm.
The entire code related with algorithm can be found at !!!algorytm genetyczny!!!. The operation of this class can be modified  by changing parameters in !!!SETTINGS!!! module (methods are also considered as parameters). You can choose method from DEAP library (by default) or create your own.


## User Interface

User interface uses [pygame](https://github.com/pygame/) library. 
In the upper right corner a generation counter is displayed.
The entire UI-code is located at !!!GUI!!!.


## License

Feel free to use my code in your personal projects. I would be very interested in any work that originates from this project. I would be more than happy to hear from your impressions and results, so feel free to mail me at pawel.brysch@gmail.com
