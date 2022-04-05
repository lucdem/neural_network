# my_neural_network

v1.1 - Basic neural network implementation with a PyQt interface for setting network configuration and training parameters as well as tracking training progress thorugh validation data accuracy and training data cost.

Nets can be saved as json files to be loaded again into the program later, training and test data are imported through jsonl files were each line is one data point.

Includes:

- Linear, Logistic, Tanh, ReLU and LeakyReLU activation functions
- MSE and MAE cost functions
- Vectorialized batch training
- Momentum based gradient descent
- Regularization methods (dropout, L1 and L2)

Planned additions:

- Cross-entropy cost function

- convolutional layers, image datasets and data augmentation

maybes?:

- fork to use pytorch behind the GUI instead of my own implementation?

- improve parallelism of my own implementation?

- add other forms of importing data sets?

- a more visual way of building the network structure, like a block diagram?