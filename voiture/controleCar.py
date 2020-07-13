import cv2
import math



class MovementCar:

    def __init__(self, coordinates):

        self.dimension = 5

        self.x = coordinates[0]
        self.y = coordinates[1]
        self.move = [5, 0]

        self.acceleration = False
        self.turnRight    = False
        self.turnLeft     = False

        self.crash = False

        self.bonus = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]






    def removeBonus(self):
        self.bonus = [0, 0]


    def getterBonus(self):
        return self.bonus



    def bonusCar(self, WALL_PICTURE):

        indexBonus = 0

        for nb, i in enumerate(self.bonus):
            if i == 0:
                indexBonus = nb
                break


        if WALL_PICTURE[self.y, self.x][0] == 255 and\
           WALL_PICTURE[self.y, self.x][1] == 156 and\
           WALL_PICTURE[self.y, self.x][1] == 88:
            self.bonus[indexBonus] = 500








    def setterCrash(self):
        self.crash = True

    def decrashCar(self):
        self.crash = False

    def getterCrash(self):
        return self.crash


    def crashCar(self, WALL_PICTURE):

        if WALL_PICTURE[self.y, self.x][0] == 0 and\
           WALL_PICTURE[self.y, self.x][1] == 0 and\
           WALL_PICTURE[self.y, self.x][1] == 0:
            self.crash = True








    def makeMoveTheCircle(self):

        if self.acceleration > 0.5:
            self.acceleration = 1
        else:
            self.acceleration = 0


        if self.turnRight != False and self.turnRight > 0.5 and\
           self.turnRight > self.turnLeft:

            if   self.move == [0, -5]: self.move = [5, 0]
            elif self.move == [0, 5] : self.move = [-5, 0]
            elif self.move == [5, 0] : self.move = [0, 5]
            elif self.move == [-5, 0]: self.move = [0, -5]


        elif self.turnLeft != False and self.turnLeft > 0.5 and\
             self.turnLeft > self.turnRight:

            if   self.move == [ 0, 5]: self.move = [5, 0]
            elif self.move == [ 5, 0]: self.move = [0, -5]
            elif self.move == [-5, 0]: self.move = [0, 5] 
            elif self.move == [0, -5]: self.move = [-5, 0] 








    def getterNextMove(self):
        return self.acceleration, self.turnRight, self.turnLeft



    def setterNextMove(self, acceleration, right, left):

        self.acceleration = acceleration
        self.turnRight    = right
        self.turnLeft     = left







    def movements(self, x, y):
        self.x += x
        self.y += y



    def getterCoord(self):
        return self.x, self.y


    def setterMove(self, move):
        self.move = move


    def getterMove(self):
        return self.move


    def reinitializePosition(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.move = [5, 0]







class Drawing:

    def __init__(self):
        self.dimension = 5


    def drawCar(self, image, coordinates):
        cv2.circle(image, coordinates, self.dimension, (0, 0, 255), 1)

