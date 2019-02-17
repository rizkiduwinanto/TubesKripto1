import FileReader
import cv2
import numpy as np
import sys
import VideoParser

def encode(videoFile, textFile):
    file = FileReader.getFile(textFile)
    video = VideoParser.getVideo(videoFile)
    encodedFrames = []
    if video.totalBit > file.totalBits:
        # TODO: sisipin byte ke tiap frame
        # TODO: iterate tiap frame, sisipin tiap bit file ke bit masing2
        maxHeight = video.height
        maxWidth = video.width
        frames = video.frames
        fileBits = file.intList
        currFrame = 0
        currHeight = 0
        currWidth = 0
        currRGB = 0
        for data in fileBits:
            for i in range(7, -1, -1):
                currBit = getBit(data, i)
                currPixelRGB = frames[currFrame][currHeight][currWidth][currRGB]
                frames[currFrame][currHeight][currWidth][currRGB] = changeLSB(currPixelRGB, currBit)
                currRGB += 1
                # ganti pixel kalo currRGB dah 3
                if currRGB == 2:
                    currWidth += 1
                    currRGB = 0
                # ganti baris kalo semua pixel sebaris selesai
                if currWidth == maxWidth-1:
                    currHeight += 1
                    currWidth = 0
                # ganti frame kalau semua pixel sebaris dan sekolom selesai
                if currHeight == maxHeight-1:
                    currFrame += 1
                    currHeight = 0
                    encodedFrames.append(frames[currFrame])
        encodedFrames += frames[currFrame:]
        VideoParser.writeVideo(encodedFrames, video.fps, video.width, video.height, 'result.avi')
    else:
        print("Not enough frames to encode message in.")
        sys.exit(-1)

def getBit(data, pos):
    return (data << pos & 0x01)

def changeLSB(data, lsb):
    return (data & 254 | lsb)

if __name__ == "__main__":
    encode('test.avi', 'test.txt') 