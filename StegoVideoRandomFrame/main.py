import Util
from video import video
from inputFile import inputFile
from stego import stuff,extract

if __name__ == "__main__":
    video1 = video('./flame.avi')
    file1 = inputFile('./tes.txt')
    fileName = 'kudukudu'
    key = 'diar'
    isRandom = True


    stuffer = stuff(video1,file1,key,isRandom)
    stuffer.insertLength()
    stuffer.insertExtension()
    stuffer.insertFile()
    stuffer.write('tes.avi')

    video2 = video('./tes.avi')
    extractor = extract(video2,key,isRandom,fileName)
    print('length :', extractor.readBitLength(),"bit")
    print('extension :',extractor.readExtension())
    extractor.readBits()


    