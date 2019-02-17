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
                self.filestr += item
            self.charlist.append(None)
            self.totalBits, self.totalBytes = self.calculateBitsAndBytes()
            file.close()
            self.intList = self.createIntList()
            print("Task Succeeded")
        except Exception as inst:
            print(inst)
            print("Task Failed")
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
        return intlist
    
    def printFileDetails(self):
        print('Filename   : ' + self.filename)
        print('Total Bits : ' + str(self.totalBits))
        print('Total Byte : ' + str(self.totalBits))
        print('File String: ' + self.filestr)
        print('Int List   : ', end='')
        print(self.intList)
        print('Char List  : ', end='')
        print(self.charlist)

def getFile(filename):
    return InputFile(filename) 