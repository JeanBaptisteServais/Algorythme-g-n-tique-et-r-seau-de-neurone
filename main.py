import cv2

from voiture.controleCar import *
from rnn.rnn import *
from rayon.rayon import *
from genetique.algoGenetique import *


""" ---------------------------- CONSTANTES -----------------------------"""
img = cv2.imread("circuit1.png")
WALL_PICTURE = img.copy()

CIRCUIT     = (20, 10)
MODE        = 0
LAYERS      = {5:25, 25:15, 15:3}
POPULATION  = 300
nbIteration = 2000











drawPopulation  = [Drawing() for i in range(POPULATION)]
carPopulation   = [MovementCar(CIRCUIT) for i in range(POPULATION)]
rayonPopulation = [Rayon() for i in range(POPULATION)]
rnnPopulation   = [Rnn(LAYERS) for i in range(POPULATION)]






evolution = True
while evolution:


    #Decrash the car
    [car.decrashCar()  for car in carPopulation]
    #Reinitialize bonus
    [car.removeBonus() for car in carPopulation]
    #Reinitialize coord
    [car.reinitializePosition(CIRCUIT) for car in carPopulation]



        

    nbCrashCar = 0
    iteration  = 0
    generation = True
    while generation:

        copy = img.copy()



        for car, rayon, rnn, draw in zip(carPopulation, rayonPopulation, rnnPopulation, drawPopulation):



            """ ----------------- VERIFY CIRCLE NOT CRASH------------------"""
            isCrash = car.getterCrash()
            if isCrash is False:



                """ ----------------- CONTROLE THE CIRCLE ------------------"""
                """Le cercle doit soit allé a droite, soit aller a gauche, et avancer"""


                if MODE == 0:

                    car.makeMoveTheCircle()
                    acceleration, _, _ = car.getterNextMove()

                    move = car.getterMove()
                    car.movements(move[0] * acceleration, move[1] * acceleration)

                    car.setterMove(move)



                if MODE == 2:

                    move = car.getterMove()

                    if cv2.waitKey(0) & 0xFF == ord('d'):
                        if   move == [0, -5]: move = [5, 0]
                        elif move == [0, 5] : move = [-5, 0]
                        elif move == [5, 0] : move = [0, 5]
                        elif move == [-5, 0]: move = [0, -5]


                    elif cv2.waitKey(0) & 0xFF == ord('g'):
                        if   move == [ 0, 5]: move = [5, 0]
                        elif move == [ 5, 0]: move = [0, -5]
                        elif move == [-5, 0]: move = [0, 5] 
                        elif move == [0, -5]:move = [-5, 0]

                    elif cv2.waitKey(0) & 0xFF == ord('m'):
                        move = move

                    car.movements(move[0], move[1])
                    car.setterMove(move)



 



                """ ------------------- DRAW THE CIRCLE ------------------"""

                coordinates = car.getterCoord()
                draw.drawCar(copy, coordinates)





                """ ----------------- MAKE THE RAYONS ------------------"""

                
                move = car.getterMove()

                rayon.defineOrientationRayon(move)
                rayon.makeRayons(WALL_PICTURE, copy, coordinates, move)
                rayon.transformeRayonToEucli(coordinates)
                rayonCircle = rayon.getterRayon()

                #print("rayon size: ", rayonCircle)



                """ ----------------------- RNN ------------------------"""

                
                rnn.biaisWeight()

                coucheNeuroneUne = rnn.preActivation(rayonCircle, 0)
                activationNeuroneCoucheUne = rnn.activation(coucheNeuroneUne)

                coucheNeuroneDeux = rnn.preActivation(activationNeuroneCoucheUne, 1)
                activationNeuroneCoucheDeux = rnn.activation(coucheNeuroneDeux)

                coucheNeuroneTrois = rnn.preActivation(activationNeuroneCoucheDeux, 2)
                activationNeuroneCoucheTrois = rnn.activation(coucheNeuroneTrois)


                #print("activation : ", activationNeuroneCoucheTrois)
                #print("")




                """ ----------------- OUT RNN ------------------"""
                acceleration, right, left = activationNeuroneCoucheTrois
                car.setterNextMove(acceleration, right, left)




                """ ----------------- BONNUS CAR ------------------"""
                car.bonusCar(WALL_PICTURE)



                """ ----------------- CRASH CAR ------------------"""
                car.crashCar(WALL_PICTURE)
                if car.getterCrash() is True:
                    nbCrashCar += 1 

                elif iteration >= nbIteration:
                    car.setterCrash()
                    nbCrashCar += 1



                """ ----------------- REMOVE VARIABLES ------------------"""
                rayon.removeRayons()





        cv2.imshow("image", copy)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            iteration = nbIteration


        """ ----------------- STOP GENERATION ------------------"""

        if nbCrashCar == POPULATION:


            """ ----------------- GENETIC ALGO ------------------"""
            deplacementMaxCars = [car.getterCoord()   for car in carPopulation]
            bonusCars          = [car.getterBonus()   for car in carPopulation]
            weightsCars        = [rnn.getterWeights() for rnn in rnnPopulation]
            biaisCars          = [rnn.getterWeights() for rnn in rnnPopulation]

            genetique = GenetiqueAlgo(CIRCUIT, deplacementMaxCars, bonusCars, weightsCars, biaisCars, POPULATION)
            genetique.scoring()
            genetique.selection()
            genetique.mutation()


            weightMutation = genetique.getterWeightMutation()
            biaisMutation  = genetique.getterBiaisMutation()


            #reCreate weight, biais if empty
            [rnn.biaisWeight() for rnn in rnnPopulation]


            #Re associate weight, biais to cars.
            for indexCarFromMutaiton, rnn in enumerate(rnnPopulation):
                rnn.setterWeights(weightMutation[indexCarFromMutaiton])
                rnn.setterBiais(biaisMutation[indexCarFromMutaiton])







            firstCar = genetique.getterFirst()
            print(firstCar)



            generation = False





        
    


        iteration += 1







        
