from scipy.spatial import distance
import random

class GenetiqueAlgo:


    def __init__(self, deaparture, deplacementMaxCars, bonusCars, weightsCars, biaisCars, POPULATION):


        #Entrances
        self.deaparture = deaparture
        self.POPULATION = POPULATION

        self.deplacementMaxCars = deplacementMaxCars
        self.bonusCars   = bonusCars
        self.weightsCars = weightsCars
        self.biaisCars   = biaisCars


        #variable intraClass
        self.score = {}

        self.firstCar = int(POPULATION / 8)
        self.last     = 20




    def scoring(self):

        for indexCar, (coord, bonus) in enumerate(zip(self.deplacementMaxCars, self.bonusCars)):
            distanceRun = distance.euclidean(self.deaparture, coord) + sum(bonus)
            self.score[indexCar] = distanceRun



    def selection(self):

        self.score = sorted(self.score.items(), key=lambda t: t[1], reverse=True)




    def mutationByTheFirstCar(self, indexCar, randomMutation):

        for nb, (couche, coucheParent) in enumerate(zip(self.weightsCars[indexCar], self.weightsCars[self.score[0][0]])):

            for nb1, (neurone, neuroneParent) in enumerate(zip(couche, coucheParent)):
                for indexWeight, (weight, weightParent) in enumerate(zip(neurone, neuroneParent)):

                    probaMuta = random.randrange(100)
                    if probaMuta > randomMutation:
                        neurone[indexWeight] = neuroneParent[indexWeight]


        for nb, (couche, coucheParent) in enumerate(zip(self.weightsCars[indexCar], self.biaisCars[self.score[0][0]])):

            for nb1, (neurone, neuroneParent) in enumerate(zip(couche, coucheParent)):
                for indexWeight, (weight, weightParent) in enumerate(zip(neurone, neuroneParent)):

                    probaMuta = random.randrange(100)
                    if probaMuta > randomMutation:
                        neurone[indexWeight] = neuroneParent[indexWeight]






    def mutationByIntraListRandom(self, indexCar, randomMutation):

        for couche in self.weightsCars[indexCar]:
            for neurone in couche:
                for indexWeight, weight in enumerate(neurone):

                    probaMuta = random.randrange(100)
                    if probaMuta > randomMutation:
                        neurone[indexWeight] = random.uniform(-3, 3)


        for couche in self.biaisCars[indexCar]:
            for neurone in couche:
                for indexBiais, biais in enumerate(neurone):

                    probaMuta = random.randrange(100)
                    if probaMuta > randomMutation:
                        neurone[indexBiais] = random.uniform(-3, 3)






    def deleteLastCar(self):

        for i in range(len(self.score) - self.last, len(self.score)):

            indexCar, _ = self.score[i]

            self.weightsCars[indexCar] = []
            self.biaisCars[indexCar]   = []



    def mutation(self):



        for iteration, (indexCar, _) in enumerate(self.score):

            #Savegarde first car
            if iteration <= self.firstCar:
                pass

            elif self.firstCar < iteration <= self.firstCar * 2:
                GenetiqueAlgo.mutationByIntraListRandom(self, indexCar, 80)

            elif self.firstCar * 2 < iteration <= self.firstCar * 3:
                #GenetiqueAlgo.mutationByIntraListRandom(self, indexCar, 75)
                GenetiqueAlgo.mutationByTheFirstCar(self, indexCar, 60)
            elif self.firstCar * 3 < iteration <= self.firstCar * 4:
                #GenetiqueAlgo.mutationByIntraListRandom(self, indexCar, 70)
                GenetiqueAlgo.mutationByTheFirstCar(self, indexCar, 50)
            elif self.firstCar * 4 < iteration <= self.firstCar * 5:
                #GenetiqueAlgo.mutationByIntraListRandom(self, indexCar, 80)
                GenetiqueAlgo.mutationByTheFirstCar(self, indexCar, 90)
            elif self.firstCar * 5 < iteration <= self.firstCar * 6:
                GenetiqueAlgo.mutationByIntraListRandom(self, indexCar, 60)


            else:
                GenetiqueAlgo.mutationByTheFirstCar(self, indexCar, 80)

        GenetiqueAlgo.deleteLastCar(self)


    













    def getterFirst(self):
        firstCar = self.score[0][0]
        return self.weightsCars[firstCar], self.biaisCars[firstCar]

    def getterWeightMutation(self):
        return self.weightsCars

    def getterBiaisMutation(self):
        return self.biaisCars



