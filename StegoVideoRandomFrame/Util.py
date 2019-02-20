import random
import math
def intToBinaryString(input):
    out = bin(input)[2:]
    if ((len(out) % 8) != 0):
        out = ''
        for i in range(8-len(out)):
            out += '0'
        out += bin(input)[2:]
    return bin(input)[2:].zfill(8)

def binaryStringToInt(input):
    return int(input, 2)

def generateSeed(inputstring):
    output = 0
    for i in inputstring:
        output += ord(i)

    return output

def encryptVigenereAsciiForBytes(input,key,mode):
    cipher = input
    for i in range(len(cipher)):
        cipher[i] = ((cipher[i] + ord(key[i]%len(key))) % 256)
    return cipher  

def generateFrameSteps(key,videoInput,fileBitLength):
    requiredFrame = (math.ceil(fileBitLength / (3 * videoInput.getHeight() * videoInput.getWidth())))
    limitBitSize = 3 * videoInput.getWidth() * videoInput.getHeight() * (len(videoInput.getFrames())-2)
    seed = generateSeed(key)
    frameSteps = []
    if (fileBitLength <= limitBitSize):
        for i in range(2,2+requiredFrame):
            frameSteps.append(i)
        random.seed(seed)
        random.shuffle(frameSteps)
    return frameSteps

def generatePixelSteps(key,videoInput,isRandom):
    pixelSteps = []
    for i in range(videoInput.getWidth()):
        for j in range(videoInput.getHeight()):
            step = []
            step.append(i)
            step.append(j)
            pixelSteps.append(step)

    if (isRandom):
        seed = generateSeed(key)  

        random.seed(seed)    
        random.shuffle(pixelSteps)
    return pixelSteps

def bitStringtoBytes(string):
    v = int(string, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])