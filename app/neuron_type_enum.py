from enum import Enum, auto

from neural_network import SigmoidLogisticNeuron, SigmoidTanhNeuron, ReLU_Neuron, LeakyReLU_Neuron, LinearNeuron


class NeuronTypeEnum(Enum):
	Logistic = SigmoidLogisticNeuron
	Tanh = SigmoidTanhNeuron
	ReLU = ReLU_Neuron
	LeakyReLU = LeakyReLU_Neuron
	Identity = LinearNeuron