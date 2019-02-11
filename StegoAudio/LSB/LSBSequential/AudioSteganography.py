import struct
import sys

class InputFile:
    def __init__(self, audio_path):
        self.totalBits = 0
        self.totalByted = 0
        self.charlist = []
        self.intList = []
        self.filestr = ""
        self.filename = audio_path
        self.openfile()
    
    def openfile(self):
        try:
            file = open(self.filename, "r")
            for item in file.read():
                self.charlist.append(item)
            self.charlist.append(None)
            self.totalBits, self.totalBytes = self.calculateBitsAndBytes()
            self.filestr = file.read()
            file.close()
            self.createIntList()
            print("Task Succeeded")
        except Exception as inst:
            print(inst)
            print("Task Failed Succesfully")
            sys.exit()
            
    def calculateBitsAndBytes(self):
        bit = 0
        byte = 0
        for i in range(len(self.charlist)):
            bit += 8
            byte += 1
        return bit, byte
    
    def createIntList(self):
        intlist = []
        for i in range(len(self.charlist)-1):
            intlist.append(ord(self.charlist[i]))
        intlist.append(0)
        self.intlist = intlist
    
def encode(list, textfile):
    file = InputFile(textfile)
    encodedAudio = []
    audioNum = 0
    
    if len(list) >= file.totalBits:
        for val in file.intlist:
            for i in range(7, -1, -1):
                bitToEncode = readBit(val, i)
                negative = True if list[audioNum] != abs(list[audioNum]) else False
                newVal = writeBit(abs(list[audioNum]), bitToEncode)
                encodedAudio.append(-1*newVal) if negative else encodedAudio.append(newVal)
                audioNum +=1
        totalEncode = encodedAudio + list[audioNum:]
        return encodedAudio + list[audioNum:]
    else: 
        print("Not enough samples to encode message in.")
        sys.exit(-1)
    
def decode(list, newfilename):
    bitlist = []
    for bits in list:
        bitlist.append(readBit(abs(bits), 0))
    potentialBytes = determineTotalBytes(bitlist)
    newByte = ""
    endByte = False
    counter = 0
    message = []
    for i in range(potentialBytes):
        if counter < 8 and endByte == False:
            newByte += str(bitlist[i])
            counter += 1
        elif counter >= 8:
            character = int(newByte, 2)
            if (character == 0):
                endByte = True
            message.append(chr(character))
            newByte = ""
            newByte += str(bitlist[i])
            counter = 0
            counter += 1
        elif endByte:
            strMessage = ""
            for characters in message:
                strMessage += characters
            writeMessageToFile(strMessage, newfilename)
            return strMessage
    
    garbage = ""
    for things in message:
        garbage += things
    return garbage
    
def writeMessageToFile(message, filename):
    try:
        newtext = open(filename, "w")
        newtext.write(message)
        newtext.close()
    except:
        print("Unable to open and write to file. Check file name and extension.")
        sys.exit()
    return

def determineTotalBytes(list):
    return int(len(list) / 8)

def writeBit(integer, boolean):
    return ((integer | 0x01) if boolean else (integer & ~0x01))

def readBit(integer, position):
    return ((0x01 << position) & abs(integer)) >> position
