import numpy as np
import cv2
import sys

class VideoFile:
    def __init__(self, videoPath):
        self.frames = []
        self.lenFrames = 0
        self.width = 0
        self.height = 0
        self.fps = 0
        self.totalBit = 0
        self.totalByte = 0
        self.filename = videoPath
        self.parseVideo()
    
    def parseVideo(self):
        self.frames, self.lenFrames, self.width, self.height, self.fps = self.parseVideoFrames()
        self.totalBit, self.totalByte = self.countTotalBitsAndBytes()
        return

    def parseVideoFrames(self):
        try:
            cap = cv2.VideoCapture(self.filename)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            count = 0
            videoFrames = []
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    count += 1
                    videoFrames.append(frame)
                else:
                    break
            cap.release()
            return videoFrames, count, width, height, fps
        except Exception as ex:
            print(ex)
            print("Failed to read video " + self.filename)
            sys.exit()
    
    def countTotalBitsAndBytes(self):
        byte = self.lenFrames * self.width * self.height * 3
        bit = byte * 8
        return bit, byte

    def printVideoDetails(self):
        print("Video Filename: " + self.filename)
        print("Resolution    : " + str(self.width) + " x " + str(self.height))
        print("Video FPS     : " + str(self.fps))
        print("Total Byte    : " + str(self.totalByte))
        print("Total Bit     : " + str(self.totalBit))

def getVideo(filename):
    return VideoFile(filename)

def writeVideo(videoFrames, fps, width, height, outputFilename):
    fourcc = cv2.VideoWriter_fourcc('H', 'F', 'Y', 'U')
    out = cv2.VideoWriter(outputFilename, fourcc, fps, (width, height))
    for frame in videoFrames:
        out.write(frame)
    out.release()
    return
    
if __name__ == "__main__":
    testVid = VideoFile('test.avi')
    testVid.printVideoDetails()