import wave
import struct
import sys

def getAudioInfo(audio):
    print("Samples in the file: {}", audio.getnframes())
    print("Sampling rate of the file: {}", audio.getframerate())
    print("Sampling width of file (bits per file: output*8):", audio.getsamplewidth())
    length = round(int(audio.getnframes()) / int(audio.getframerate()), 3)
    print("Length in seconds of the file:", length, "seconds")

def parseFrames(audio):
    length = audio.getnframes()
    audioFrames = []
    for i in range(0, length):
        frame = audio.readframes(1)
        data = struct.unpack("<h", frame)
        audioFrames.append(data[0])
    del length
    return audioFrames

def writeNewWave(list, sr, name):
    try :
        newWave = wave.open(name, "w")
        newWave.setnchannels(1)
        newWave.setsampwidth(2)
        newWave.setframerate(sr)
        for items in list:
            byteType = struct.pack('<h', items)
            newWave.writeframes(byteType)
        newWave.close()
        del list, sr, name
        return newWave
    except:
        print("Error")
        sys.exit(-1)