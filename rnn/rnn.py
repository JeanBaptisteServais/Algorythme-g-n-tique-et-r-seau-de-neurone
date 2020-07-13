import numpy as np
import random

class Rnn:

    def __init__(self, layers):

        self.layers  = layers
        self.weights = [[] for i in range(len(self.layers))]
        self.biais   = [[] for i in range(len(self.layers))]






    def sauvegardeWeight(self):
        pass

    def sauvegardeBiais(self):
        pass


    def setterWeights(self, newWeights):
        self.weights = [[] for i in range(len(self.layers))]
        self.weights = newWeights

    def setterBiais(self, newBiais):
        self.biais   = [[] for i in range(len(self.layers))]
        self.biais = newBiais





    def activation(self, couche):

        activationNeurone = []

        for preActNeurone in couche:
            sigmoid = 1.0 / (1.0 + np.exp(-preActNeurone))
            activationNeurone.append(sigmoid)

        return activationNeurone



    def preActivation(self, entries, couche):

        """
        print(entries)
        print(self.weights[couche])
        print(self.biais[couche])
        print("")
        """


        coucheNeurone = []

        for weight, biais in zip(self.weights[couche], self.biais[couche]):
            preActSomme = 0
            for xi, wi in zip(entries, weight):
                preActSomme += xi * wi

            coucheNeurone.append(preActSomme + biais[0])

        return coucheNeurone







    def biaisWeight(self):


        def controlWeightBiais():
            if self.weights == [[] for i in range(len(self.layers))]:
                return True
            elif self.weights == []:
                self.weights = [[] for i in range(len(self.layers))]
                self.biais   = [[] for i in range(len(self.layers))]
                return True
            return False


        if controlWeightBiais() is True:

            for index, (entries, nbPoids) in enumerate(self.layers.items()):

                coucheNeurone = []
                for wi in range(nbPoids):

                    self.biais[index].append([random.uniform(-3, 3)])

                    poidsNeurone = []
                    for xi in range(entries):

                        poidsNeurone.append(random.uniform(-3, 3))
                    coucheNeurone.append(poidsNeurone)

                self.weights[index] = coucheNeurone


        """
        for indexCouche, (wi, bi) in enumerate(zip(self.weights, self.biais)):

            print("COUCHE NUMERO: ", indexCouche)

            for numeroNeurone, (w, b) in enumerate(zip(wi, bi)):
            
                print("neurone numero:", numeroNeurone,
                      " = poids: ", w, " biais:", b)

            print("")
        """




    def getterWeights(self):
        return self.weights


    def getterBiais(self):
        return self.biais
























        
