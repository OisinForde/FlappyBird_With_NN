import random

class Percreptron:
    learningRate=2
    def __init__(self):
        self.weights=[]
        for i in range(6):
            self.weights.append(random.uniform(-.5,.5)) #self.weights=

    def Activation_Function(self, x):
        if x >= 0:
            return 1
        else:
            return -1

    def foward_propagration(self,inputs):
        weightedSum=0
        for i in range(len(self.weights)):
            weightedSum+=self.weights[i]*inputs[i]*self.learningRate+1
        output=self.Activation_Function(weightedSum)
        return output

    def mutation(self):
        pass

