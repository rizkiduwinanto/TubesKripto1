import math
import Util
class inputFile:
    def __init__(self,filename):
        self.filename = filename
        self.readInputFileByte()

    def readInputFileByte(self):
        f = open(self.filename, "rb")        
        self.filebyte = bytearray(f.read())
    
    def getFileInputByte(self):
        return self.filebyte

    def getFileName(self):
        return self.filename

    def getFileSize(self):
        return len(self.filebyte)

    def getFileSizeBits(self):
        return len(self.filebyte) * 8    

    def getExtension(self):
        return self.getFileName()[self.getFileName().index('.',1,len(self.getFileName()))+1:]
    
    def writeFileWithExtension(self,filename):
        with open(filename+'.'+self.getExtension(), 'wb') as fo:
            fo.write(self.getFileInputByte())
        return 0

    def willItFit(self,video):
        out = False
        calculation = 3 * video.getWidth() * video.getHeight() * (len(video.getFrames())-2)
        if (self.getFileSizeBits() <= calculation):
            out = True
        return out

    def willExtensionFit(self,video):
        out = False
        calculation = 3 * video.getWidth() * video.getHeight()
        if ((len(self.getExtension())*8) <= calculation):
            out = True
        return out

    def willLengthFit(self,video):
        out = False
        calculation = 3 * video.getWidth() * video.getHeight()
        if (len(Util.intToBinaryString(self.getFileSizeBits())) <= calculation):
            out = True
        return out