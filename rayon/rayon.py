import cv2
from scipy.spatial import distance



class Rayon:

    def __init__(self):
        self.rayonDimension = 50
        self.orientation = None

        self.coeffsBas     = [0, 1, 1, 1, -1, 1, -1, 0, 1, 0]
        self.coeffsHaut    = [0, -1, -1, -1, 1, -1, 1, 0, -1, 0]
        self.coeffsDroite  = [1, 0, 1, -1, 1, 1, 0, 1, 0, -1]
        self.coeffsGauche  = [-1, 0, -1, 1, -1, -1, 0, -1, 0, 1]

        self.detectionWall = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

        self.rayonDistance = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

        self.sauvegardeMaxValue = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]






    def getterRayon(self):
        return self.rayonDistance





    def transformeRayonToEucli(self, coordinate):

        maxValue = 38.0

        for nb, rayon in enumerate(self.detectionWall):
            if rayon == (0, 0):
                rayon = self.sauvegardeMaxValue[nb]

            dist = distance.euclidean(coordinate, rayon)
            self.rayonDistance[nb] = dist / maxValue
            #self.rayonDistance[nb] = dist

        #print(self.rayonDistance)





    def CircleWall(self, isWallR1, r1, isWallR2, r2, isWallR3, r3, isWallR4, r4, isWallR5, r5):

        wallDetection  = [isWallR1, isWallR2, isWallR3, isWallR4, isWallR5]
        rayonDetection = [r1, r2, r3, r4, r5]

        for nb, (detection, coordRayon) in enumerate(zip(wallDetection, rayonDetection)):

            if detection is True and self.detectionWall[nb] == (0, 0):
                self.detectionWall[nb] = coordRayon





    def sauvegardeMaxValue(self, r1, r2, r3, r4, r5):
        for nb, r in enumerate([r1, r2, r3]):
            self.sauvegardeMaxValue[nb] = r





    def getDistanceRayon(self, wallPicture, image, coordinates, coeffs):

        def displayLine(image, coordinates, r1, r2, r3, r4, r5):
            cv2.line(image, coordinates, r1, (0, 0, 255), 1)
            cv2.line(image, coordinates, r2, (0, 255, 0), 1)
            cv2.line(image, coordinates, r3, (0, 255, 0), 1)
            cv2.line(image, coordinates, r4, (0, 255, 0), 1)
            cv2.line(image, coordinates, r5, (0, 255, 0), 1)


        def displayLineWall(image, coordinates, isWallR1, isWallR2, isWallR3, isWallR4, isWallR5,
                            r1, r2, r3, r4, r5):

            if isWallR1 == True:
                cv2.line(image, coordinates, r1, (0, 0, 255), 1)
            if isWallR2 == True:
                cv2.line(image, coordinates, r2, (0, 0, 255), 1)
            if isWallR3 == True:
                cv2.line(image, coordinates, r3, (0, 0, 255), 1)
            if isWallR4 == True:
                cv2.line(image, coordinates, r4, (0, 0, 255), 1)
            if isWallR5 == True:
                cv2.line(image, coordinates, r5, (0, 0, 255), 1)

        def isWallFunction(wallPicture, r):
            x, y = r

            h = wallPicture.shape[0]
            w = wallPicture.shape[1]

            if 0 < x < w and\
               0 < y < h and\
               wallPicture[y, x][0] == 0 and\
               wallPicture[y, x][1] == 0 and\
               wallPicture[y, x][2] == 0:
                return True
            return False



        x, y = coordinates
        coef1, coef2, coef3, coef4, coef5, coef6, coef7, coef8, coef9, coef10 = coeffs

        for i in range(self.rayonDimension):

            r1 = ( x + (i * coef1), y + (i * coef2) )
            r2 = ( x + (i * coef3), y + (i * coef4) )
            r3 = ( x + (i * coef5), y + (i * coef6) )
            r4 = ( x + (i * coef7), y + (i * coef8) )
            r5 = ( x + (i * coef9), y + (i * coef10) )


            if i < self.rayonDimension:

                #displayLine(image, coordinates, r1, r2, r3, r4, r5)
                isWallR1 = isWallFunction(wallPicture, r1)
                isWallR2 = isWallFunction(wallPicture, r2)
                isWallR3 = isWallFunction(wallPicture, r3)
                isWallR4 = isWallFunction(wallPicture, r4)
                isWallR5 = isWallFunction(wallPicture, r5)

                displayLineWall(image, coordinates, isWallR1, isWallR2, isWallR3, isWallR4, isWallR5,
                                r1, r2, r3, r4, r5)

                Rayon.CircleWall(self, isWallR1, r1, isWallR2, r2,
                                 isWallR3, r3, isWallR4, r4, isWallR5, r5)

            else:
                Rayon.sauvegardeMaxValue(self, r1, r2, r3, r4, r5)



    def defineOrientationRayon(self, move):

        if move == [0, 5]:
            self.orientation = "bas"
        elif move == [5, 0]:
            self.orientation = "droite"
        elif move == [-5, 0]:
            self.orientation = "gauche"
        elif move == [0, -5]:
            self.orientation = "haut"




    def makeRayons(self, wallPicture, image, coordinates, move):


        if self.orientation == "bas":
            Rayon.getDistanceRayon(self, wallPicture, image, coordinates, self.coeffsBas)

        elif self.orientation == "droite":
            Rayon.getDistanceRayon(self, wallPicture, image, coordinates, self.coeffsDroite)

        elif self.orientation == "gauche":
            Rayon.getDistanceRayon(self, wallPicture, image, coordinates, self.coeffsGauche)

        elif self.orientation == "haut":
            Rayon.getDistanceRayon(self, wallPicture, image, coordinates, self.coeffsHaut)






    def removeRayons(self):
        self.detectionWall = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        self.rayonDistance = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        self.sauvegardeMaxValue = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]



