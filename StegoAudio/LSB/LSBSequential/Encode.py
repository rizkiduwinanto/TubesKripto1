import wave
import AudioParser
import AudioSteganography

audio = wave.open("../Data/ChallengerAccident.wav", "r")
list = AudioParser.parseFrames(audio)
samplerate = audio.getframerate()
encodedAudio = AudioSteganography.encode(list, "../Message/HarryKane.txt")
AudioParser.writeNewWave(encodedAudio, samplerate, "../Data_Altered/New.wav")
audio.close()