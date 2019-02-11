import wave
import AudioParser
import AudioSteganography

encodedAudio = wave.open("../Data_Altered/New.wav", "r")
newlist = AudioParser.parseFrames(encodedAudio)
secretMessage = AudioSteganography.decode(newlist, "../Secret/Secret1.txt")
print(secretMessage)
encodedAudio.close()