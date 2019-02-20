import cv2
import Util
class video:

    def __init__(self,filename):
        self.frames = []
        self.readVideo(filename)

    def readVideo(self,filename):
        vidcap = cv2.VideoCapture(filename)
        if (vidcap.isOpened()== False): 
            print("Error opening video stream or file")
        success = True
        frames = []
        while(vidcap.isOpened()):
            success,image = vidcap.read()
            if(success):
                frames.append(image)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        vidcap.release()

        self.frames = frames
        self.width = self.frames[0].shape[1]
        self.height = self.frames[0].shape[0]

    def writeVideo(self,filename):
        out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'HFYU'), 30, (self.getWidth(),self.getHeight()))
        for i in self.frames:
            out.write(i)
        out.release()

    def getFrames(self):
        return self.frames

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def manipulateFrames(self,frameIdx,xIdx,yIdx,colorIdx,value):
        self.frames[frameIdx][xIdx][yIdx][colorIdx] = Util.binaryStringToInt(value)
    
    def setFrames(self,framesInput):
        self.frames = framesInput