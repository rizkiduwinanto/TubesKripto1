import math
import Util

class psnr:
    def __init__(self,video1,video2,key,fileInput):
        self.video1 = video1
        self.video2 = video2
        self.fileInput = fileInput
        self.key = self.key
        self.framePath = Util.generateFrameSteps(self.key,video1,fileInput.getFileSizeBits())
        self.pixelPath = Util.generatePixelSteps(self.key,self.video1,False)

    def psnrCounter(self):
        frames1 = self.video1.getFrames()
        frames2 = self.video2.getFrames()
        colorIndex = 0
        sumRms = 0
        pembagiRms = len(self.framePath)
        for i in self.framePath:
            pembagi = self.video1.getWidth() *  self.video1.getHeight()
            sumSelisih = 0            
            for j in self.pixelPath:
                selisihPixelKuadrat = math.pow((frames1[i][j[1]][j[0]][colorIndex] - frames2[i][j[1]][j[0]][colorIndex]),2)
                sumSelisih += selisihPixelKuadrat
                colorIndex += 1
                if (colorIndex > 2 ) :
                    colorIndex = colorIndex % 3
            sumRms += math.pow(sumSelisih / pembagi,0.5)
        sumRmsAvg = sumRms / pembagiRms
        return 20 * math.log((256/sumRmsAvg),10)