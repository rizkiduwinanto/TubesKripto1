import Util
class stuff:
    def __init__(self,videoInput,fileInput,key,isRandom):
        self.videoInput = videoInput
        self.fileInput = fileInput
        self.key = key
        self.isRandom = isRandom
    
    def insertExtension(self):
        frames = self.videoInput.getFrames()
        extensionBinary = ''
        extension = self.fileInput.getExtension()
        for i in extension:
            extensionBinary += Util.intToBinaryString(ord(i))

        extensionBinary += Util.intToBinaryString(ord('#'))

        colorIndex = 0
        yIndex = 0
        xIndex = 0

        while (len(extensionBinary) > 0):
            
            frames[0][xIndex][yIndex][colorIndex] = Util.binaryStringToInt(Util.intToBinaryString(frames[0][xIndex][yIndex][colorIndex])[:-1] + extensionBinary[0])
            extensionBinary = extensionBinary[1:]
            colorIndex +=1
            if (colorIndex > 2):
                colorIndex = 0
                yIndex += 1

            if (colorIndex > self.videoInput.getHeight()):
                yIndex = 0
                xIndex += 1

        return 0

    def insertLength(self):
        frames = self.videoInput.getFrames()    
        toBeInserted = Util.intToBinaryString(self.fileInput.getFileSizeBits()) + Util.intToBinaryString(ord('#'))
        colorIndex = 0
        yIndex = 0
        xIndex = 0

        while (len(toBeInserted) > 0):
            
            frames[1][xIndex][yIndex][colorIndex] = Util.binaryStringToInt(Util.intToBinaryString(frames[1][xIndex][yIndex][colorIndex])[:-1] + toBeInserted[0])
            toBeInserted = toBeInserted[1:]
            colorIndex +=1
            if (colorIndex > 2):
                colorIndex = 0
                yIndex += 1

            if (colorIndex > self.videoInput.getHeight()):
                yIndex = 0
                xIndex += 1

        return 0
    
    def insertFile(self):
        framePath = Util.generateFrameSteps(self.key,self.videoInput,self.fileInput.getFileSizeBits())
        pixelPath = Util.generatePixelSteps(self.key,self.videoInput,self.isRandom)
        if (self.fileInput.willItFit(self.videoInput)):
            bits = ''
            for i in self.fileInput.getFileInputByte():
                bits += Util.intToBinaryString(i)
            colorIndex = 0
            for j in framePath:
                for k in pixelPath:
                    value = Util.intToBinaryString(self.videoInput.getFrames()[j][k[1]][k[0]][colorIndex])[:-1] + bits[0]
                    self.videoInput.manipulateFrames(j,k[1],k[0],colorIndex,value)
                    bits = bits[1:]
                    colorIndex += 1
                    if (colorIndex > 2):
                        colorIndex = colorIndex % 3
                    if(len(bits)<1):
                        break
                if(len(bits)<1):
                    break
        else:
            print("File is larger than container")

    def write(self,fileName):
        self.videoInput.writeVideo(fileName)



class extract:
    def __init__(self,videoInput,key,isRandom,fileName):
        self.videoInput = videoInput
        self.key = key
        self.isRandom = isRandom
        self.fileName = fileName
        self.extension = ''
        self.bitLength = 0

    def readExtension(self):
        length = 0
        frames = self.videoInput.getFrames()
        stringToBeMatched = Util.intToBinaryString(ord('#'))
        colorIndex = 0
        yIndex = 0
        xIndex = 0
        datas = ''

        while True:
            datas += Util.intToBinaryString(frames[0][xIndex][yIndex][colorIndex])[-1:]
            colorIndex +=1
            if (colorIndex > 2):
                colorIndex = 0
                yIndex += 1

            if (colorIndex > self.videoInput.getHeight()):
                yIndex = 0
                xIndex += 1

            if (datas[-8:] == stringToBeMatched):
                datas = datas[:-8]
                break

        length = int(len(datas)/8)    
        extension = ''
        for i in range(length):
            extension += chr(Util.binaryStringToInt(datas[:8]))
            datas = datas[8:]
        return extension

    def readBitLength(self):
        length = 0
        frames = self.videoInput.getFrames()
        stringToBeMatched = Util.intToBinaryString(ord('#'))
        colorIndex = 0
        yIndex = 0
        xIndex = 0
        datas = ''

        while True:
            datas += Util.intToBinaryString(frames[1][xIndex][yIndex][colorIndex])[-1:]
            colorIndex +=1
            if (colorIndex > 2):
                colorIndex = 0
                yIndex += 1

            if (colorIndex > self.videoInput.getHeight()):
                yIndex = 0
                xIndex += 1

            if (datas[-8:] == stringToBeMatched):
                datas = datas[:-8]
                break

        length = Util.binaryStringToInt(datas)
        return length


    def write(self,arrayByte):
        with open(self.fileName+'.'+self.readExtension(), 'wb') as fo:
            fo.write(arrayByte)
        return 0
        
    def readBits(self):
        self.bitLength = self.readBitLength()
        framePath = Util.generateFrameSteps(self.key,self.videoInput,self.bitLength)
        pixelPath = Util.generatePixelSteps(self.key,self.videoInput,self.isRandom)
        frames = self.videoInput.getFrames()
        counter = 0
        colorIndex = 0
        fileOutput = bytearray()
        bits = ''

        for i in framePath:
            for j in pixelPath:
                bits += Util.intToBinaryString(frames[i][j[1]][j[0]][colorIndex])[-1:]
                if (len(bits) == 8):                    
                    fileOutput += Util.bitStringtoBytes(bits)
                    bits = ''
                colorIndex += 1
                if (colorIndex > 2):
                    colorIndex = colorIndex % 3
                counter += 1
                if (counter >= self.bitLength):
                    break
            if (counter >= self.bitLength):
                break
        
        self.write(fileOutput)
        
