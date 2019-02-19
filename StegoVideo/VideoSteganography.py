import base64
import cv2
import numpy as np
import sys
import VideoParser

def encode(videoFile, messageFile, secretKey, flagEncrypt, flagRandom, flagLSB, outputFilename):
    fileBits, metadataBits = getEncodedBits(messageFile, flagEncrypt, flagRandom, flagLSB)
    video = VideoParser.getVideo(videoFile)
    encodedFrames = []
    totalBitInFrame = video.width * video.height * 3
    maxHeight = video.height
    maxWidth = video.width
    frames = video.frames
    currFrame = 0
    currHeight = 0
    currWidth = 0
    currRGB = 0
    x = 0
    # simpen metadata
    if totalBitInFrame > len(metadataBits):
        currWidth = 0
        currHeight = 0
        currRGB = 0
        x = 0
        print('Metadata')
        for bit in metadataBits:
            currPixelRGB = frames[0][currHeight][currWidth][currRGB]
            frames[0][currHeight][currWidth][currRGB] = changeLSB(currFrame, bit)
            x += 1
            print('%d. %d -> %d - > %d' % (x, currPixelRGB, bit, frames[0][currHeight][currWidth][currRGB]))
            currRGB += 1
            # ganti pixel kalo currRGB dah 3
            if currRGB == 2:
                currWidth += 1
                currRGB = 0
            # ganti baris kalo semua pixel sebaris selesai
            if currWidth == maxWidth-1:
                currHeight += 1
                currWidth = 0
        encodedFrames.append(frames[0])
        print()
    else:
        print("Not enough pixel to save metadata")
        sys.exit(-1)

    # simpen data
    if video.totalBit > len(fileBits):
        currFrame = 1
        currHeight = 0
        currWidth = 0
        currRGB = 0
        x = 0
        print('data')
        for bit in fileBits:
            currPixelRGB = frames[currFrame][currHeight][currWidth][currRGB]
            frames[currFrame][currHeight][currWidth][currRGB] = changeLSB(currPixelRGB, bit)
            x += 1
            print('%d. %d -> %d - > %d' % (x, currPixelRGB, bit, frames[currFrame][currHeight][currWidth][currRGB]))
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
        VideoParser.writeVideo(encodedFrames, video.fps, video.width, video.height, outputFilename)
    else:
        print("Not enough frames to encode message in.")
        sys.exit(-1)

def getEncodedBits(filename, flagEncrypt, flagRandom, flagLSB):
    with open(filename, "rb") as file:
      file_byte = file.read()
    byte_message = base64.b64encode(file_byte).decode('utf-8')
    extension = filename.split('.').pop()
    length_message = len(byte_message)
    string_metadata = str(length_message) + '#' + extension + '#' + str(flagEncrypt) + '#' + str(flagRandom) + '#' + str(flagLSB) + '#'
    print(byte_message)
    print(string_metadata)
    message_bit_list = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in byte_message])))
    metadata_bit_list = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string_metadata])))
    print(message_bit_list)
    print(len(message_bit_list))
    print(metadata_bit_list)
    print(len(metadata_bit_list))
    return message_bit_list, metadata_bit_list


def changeLSB(data, lsb):
    return (data & 254 | lsb)

if __name__ == "__main__":
    encode('rassegna2.avi', 'test.txt', 'SECRET', False, False, False, 'rassegna2_res.avi')
    #getEncodedBits('test.txt', False, False, False)