import numpy as np
import random
from tqdm import tqdm


class AppleArray:
    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.array = np.zeros((self.xSize, self.ySize), dtype=int)
        self.integralImage = np.zeros((self.xSize+1, self.ySize+1), dtype=int)
        
        self.setNewGame()
    
    def printArray(self):
        print("Array:", self.xSize, '*', self.ySize)

        print("- 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7")
        for i in range(0, self.ySize):
            print(i, end=' ')
            for j in range(0, self.xSize):
                if self.array[j][i]==0:
                    print(" ", end=' ')
                else:
                    print("%d" % self.array[j][i], end=' ')
            print()
        
        return self.array
    
    def printIntegral(self):
        print("Integral Image:", self.xSize+1, '*', self.ySize+1)

        for i in range(0, self.ySize+1):
            for j in range(0, self.xSize+1):
                print("%3d" % self.integralImage[j][i], end=' ')
            print()
        
        return self.integralImage
    

    def getSum(self, startPoint:list, endPoint:list):
        if startPoint[0]>endPoint[0] or startPoint[1]>endPoint[1]:
            print(startPoint, "-", endPoint)
            raise ValueError("Check the coordinates.")
        
        x1 = startPoint[0] + 1
        y1 = startPoint[1] + 1

        x2 = endPoint[0] + 1
        y2 = endPoint[1] + 1

        return (
            self.integralImage  [x2]   [y2]
            - self.integralImage[x1-1] [y2]
            - self.integralImage[x2]   [y1-1]
            + self.integralImage[x1-1] [y1-1]
        )
    
    def tryBreak(self, startPoint:list, endPoint:list):
        if self.getSum(startPoint, endPoint) == 10:
            for i in range(startPoint[0], endPoint[0]+1):
                for j in range(startPoint[1], endPoint[1]+1):
                    self.changeValue((i, j), 0)
            return True
        else:
            return False

    
    def changeValue(self, coordinate:list, value):
        offset = value - self.array[coordinate[0]][coordinate[1]]
        self.array[coordinate[0]][coordinate[1]] = value

        affectedXSize = self.xSize - coordinate[0]
        affectedYSize = self.ySize - coordinate[1]
        mask = np.full((affectedXSize, affectedYSize), offset, dtype=int)
        mask = np.pad(mask,
                      pad_width=((self.xSize - affectedXSize, 1), (self.ySize - affectedYSize, 1))
                      )

        self.integralImage += mask



    def setNewGame(self):
        # self.useConstantValue()
        # return

        for i in range(0, self.xSize):
            for j in range(0, self.ySize):
                self.array[i][j] = random.randrange(1, 10)
        self.makeIntegralImage()
    
    def useConstantValue(self):
        self.array = np.array([
            [6, 2, 4, 8, 8, 8, 1, 1, 7, 8, 2, 7, 1, 4, 3, 5, 7, 3],
            [9, 9, 2, 8, 1, 9, 6, 2, 9, 6, 4, 2, 2, 2, 4, 5, 7, 2],
            [7, 5, 5, 1, 1, 8, 8, 1, 4, 9, 1, 4, 9, 6, 3, 2, 9, 8],
            [8, 7, 7, 6, 2, 5, 4, 4, 7, 6, 4, 4, 8, 2, 4, 2, 8, 6],
            [4, 9, 6, 8, 4, 1, 7, 4, 2, 6, 2, 5, 9, 6, 9, 6, 7, 4],
            [9, 4, 2, 4, 2, 5, 8, 6, 8, 9, 4, 1, 6, 2, 8, 7, 8, 3],
            [3, 9, 4, 2, 4, 2, 2, 1, 8, 5, 5, 7, 4, 7, 1, 2, 2, 9],
            [1, 5, 8, 3, 9, 8, 9, 3, 3, 6, 9, 2, 4, 3, 8, 1, 6, 4],
            [2, 7, 1, 7, 2, 2, 3, 6, 1, 8, 8, 2, 4, 9, 4, 6, 7, 4],
        ])
        self.array = self.array.T

        self.array = np.ones((self.xSize, self.ySize), dtype=int)
        self.makeIntegralImage()

    def makeIntegralImage(self):
        processinglImage = np.zeros((self.xSize+1, self.ySize+1), dtype=int)
        for i in range(0, self.xSize):
            for j in range(0, self.ySize):
                processinglImage[i+1][j+1] = (processinglImage[i+1][j]+processinglImage[i][j+1] - processinglImage[i][j]) + self.array[i][j]

        self.integralImage = processinglImage


def startAlgorithm(apples:AppleArray):
    for repeat in range(2000):
    # for repeat in tqdm(range(2000)):
        # i = random.randrange(0, 18)
        # j = random.randrange(0, 9)
        # case = findPossibleCase(apples, (i, j))
        # if type(case) != bool: apples.tryBreak((i, j), case)
        beforeArray = apples.array.copy()

        for i in range(0, apples.xSize):
            for j in range(0, apples.ySize):
                case = findPossibleCase(apples, (i, j))
                if type(case) != bool: apples.tryBreak((i, j), case)
        
        if np.array_equal(beforeArray, apples.array):
            return

# def 

def findPossibleCase(apples:AppleArray, startPoint:tuple):
    startPoint = np.array(startPoint, dtype=int)
    relativeEndPoint = np.array([1, 0], dtype=int)   # x좌표부터 확대.

    # x축 최대 확인
    for relativeEndPoint[0] in range(0, apples.xSize - startPoint[0]):
        apples.makeIntegralImage()
        sum = apples.getSum(startPoint, startPoint+relativeEndPoint)
        if sum == 10:
            return (startPoint+relativeEndPoint)
        elif sum > 10:
            relativeEndPoint[0]-=1
            break
    
    # y축 기준 계단식 탐색
    for relativeEndPoint[1] in range(1, apples.ySize - startPoint[1]):
        sum = 9999
        while sum > 10:
            sum = apples.getSum(startPoint, startPoint+relativeEndPoint)
            if sum == 10:
                return (startPoint+relativeEndPoint)
            
            if relativeEndPoint[0] == 0:
                break
            else:
                relativeEndPoint[0]-=1
    
    return False


def startTerminal(apples:AppleArray):
    print("--Terminal mode--")
    apples.printArray()

    while True:
        inputPoint1 = [0, 0]
        inputPoint2 = [0, 0]
        inputString = input("> ")

        if inputString == "end":
            exit(0)
        elif inputString == "printRaw":
            print(str(apples.array).replace(" ", ", "))
        elif inputString == "printArray":
            apples.printArray()
        elif inputString == "printIntegral":
            apples.printIntegral()
        else:
            inputPoint1[0], inputPoint1[1], inputPoint2[0], inputPoint2[1] = input("> ").split()
            inputPoint1[0] = int(inputPoint1[0])
            inputPoint1[1] = int(inputPoint1[1])
            inputPoint2[0] = int(inputPoint2[0])
            inputPoint2[1] = int(inputPoint2[1])

            print(apples.tryBreak(inputPoint1, inputPoint2))
            apples.printArray()

if __name__ == '__main__':
    apples = AppleArray(18, 9)

    startAlgorithm(apples)
    apples.printArray()
    print(np.count_nonzero(apples.array))
    exit(0)
    
    i = 0
    sumScore = 0
    while True:
        i+=1
        apples.setNewGame()
        startAlgorithm(apples)
        score = np.count_nonzero(apples.array)
        sumScore+=score
        if score>=100:
            print("\n----------")
            print(score)
            apples.printArray()
        # print(score, end=' ')
        if i%10 == 0:
            print(".")
            # print(" | %.2f"%(sumScore/i))