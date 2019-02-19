import base64
import cv2
import numpy as np
import sys
import VideoParser

def encode(videoFile, messageFile, secretKey, flagEncrypt, flagRandom, flagLSB, outputFilename):
    fileBits, metadataBits = getEncodedBits(messageFile, secretKey, flagEncrypt, flagRandom, flagLSB)
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
        # print('Metadata')
        for bit in metadataBits:
            currPixelRGB = frames[0][currHeight][currWidth][currRGB]
            frames[0][currHeight][currWidth][currRGB] = changeLSB(currPixelRGB, bit)
            x += 1
            #print('%d. %d -> %d - > %d' % (x, currPixelRGB, bit, frames[0][currHeight][currWidth][currRGB]))
            currRGB += 1
            # ganti pixel kalo currRGB dah 3
            if currRGB == 3:
                currWidth += 1
                currRGB = 0
            # ganti baris kalo semua pixel sebaris selesai
            if currWidth == maxWidth-1:
                currHeight += 1
                currWidth = 0
        encodedFrames.append(frames[0])
        # print()
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
        # print('data')
        for bit in fileBits:
            currPixelRGB = frames[currFrame][currHeight][currWidth][currRGB]
            frames[currFrame][currHeight][currWidth][currRGB] = changeLSB(currPixelRGB, bit)
            x += 1
            #print('%d. %d -> %d - > %d' % (x, currPixelRGB, bit, frames[currFrame][currHeight][currWidth][currRGB]))
            currRGB += 1
            # ganti pixel kalo currRGB dah 3
            if currRGB == 3:
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

def decode(videoFilename, secretKey, outputFilename):
    # Parse Metadata
    video = VideoParser.getVideo(videoFilename)
    frames = video.frames
    metadataFrame = 0
    currWidth = 0
    currHeight = 0
    currRGB = 0
    hashtagCounter = 0
    metadataFinished = False
    metadataBits = []
    metadata_string = ""
    len_metadataBits = 0
    while(not metadataFinished):
        currPixelRGB = frames[metadataFrame][currHeight][currWidth][currRGB]
        metadataBits.append(getLSB(currPixelRGB))
        currRGB += 1
        len_metadataBits += 1
        # ganti pixel kalo currRGB dah 3
        if currRGB == 3:
            currWidth += 1
            currRGB = 0
        # ganti baris kalo semua pixel sebaris selesai
        if currWidth == video.width-1:
            currHeight += 1
            currWidth = 0
        if (len_metadataBits == 8):
            char = "".join(chr(int("".join(map(str,metadataBits[i:i+8])),2)) for i in range(0,len(metadataBits),8))
            metadata_string += char
            metadataBits.clear()
            len_metadataBits = 0
            if char == '#':
                hashtagCounter += 1
            if hashtagCounter == 5: 
                metadataFinished = not metadataFinished
    # Get Metadata details
    currFrame = 1
    currWidth = 0
    currHeight = 0
    currRGB = 0
    metadata = metadata_string.split('#')
    message_size = int(metadata[0])
    message_extension = metadata[1]
    message_flag_encrypt = bool(metadata[2])
    message_flag_random = bool(metadata[3])
    message_flag_LSB = bool(metadata[4])
    # Parse message
    message_bit = []
    for i in range(message_size * 8):
        currPixelRGB = frames[currFrame][currHeight][currWidth][currRGB]
        message_bit.append(getLSB(currPixelRGB))
        #print('%d. %d -> %d - > %d' % (x, currPixelRGB, bit, frames[currFrame][currHeight][currWidth][currRGB]))
        currRGB += 1
        # ganti pixel kalo currRGB dah 3
        if currRGB == 3:
            currWidth += 1
            currRGB = 0
        # ganti baris kalo semua pixel sebaris selesai
        if currWidth == video.width-1:
            currHeight += 1
            currWidth = 0
        # ganti frame kalau semua pixel sebaris dan sekolom selesai
        if currHeight == video.height-1:
            currFrame += 1
            currHeight = 0
    message_byte = "".join(chr(int("".join(map(str,message_bit[i:i+8])),2)) for i in range(0,len(message_bit),8))
    message_byte = decrypt_vigener(message_byte, secretKey) if message_flag_encrypt else message_byte
    writeOutput(message_byte, message_extension, outputFilename)
    # write message into file
    return

def getEncodedBits(filename, key, flagEncrypt, flagRandom, flagLSB):
    with open(filename, "rb") as file:
      file_byte = file.read()
    byte_message = base64.b64encode(file_byte).decode('utf-8')
    byte_message = encrypt_vigenere(byte_message, key) if flagEncrypt else byte_message
    extension = filename.split('.').pop()
    length_message = len(byte_message)
    string_metadata = str(length_message) + '#' + extension + '#' + str(flagEncrypt) + '#' + str(flagRandom) + '#' + str(flagLSB) + '#'
    message_bit_list = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in byte_message])))
    metadata_bit_list = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string_metadata])))
    return message_bit_list, metadata_bit_list

def writeOutput(message, extension, filename):
    file_byte = base64.b64decode(message.encode('utf-8'))
    with open(filename + '.' + extension, 'wb') as file:
      file.write(file_byte)
    return

def encrypt_vigenere(plaintext, key):
    plaintext_int = [ord(letter) for letter in plaintext]
    key_int = [ord(letter) for letter in key]
    ciphertext = ''
    for index in range(len(plaintext_int)):
      value = plaintext_int[index] + key_int[index % len(key_int)]
      ciphertext += chr(value % 256)
    return ciphertext

def decrypt_vigener(ciphertext, key):
    ciphertext_int = [ord(letter) for letter in ciphertext]
    key_int = [ord(letter) for letter in key]
    plaintext = ''
    for index in range(len(ciphertext_int)):
      value = ciphertext_int[index] - key_int[index % len(key_int)]
      plaintext += chr(value % 256)
    return plaintext

def getLSB(data):
    return data & 1

def changeLSB(data, lsb):
    return (data & 254 | lsb)

if __name__ == "__main__":
    encode('test.avi', 'test.txt', 'SECRET', False, False, False, 'rassegna2_res.avi')
    decode('rassegna2_res.avi', 'SECRET', 'res')
    encode('test.avi', 'test.txt', 'SECRET', True, False, False, 'resEncrypted.avi')
    decode('resEncrypted.avi', 'SECRET', 'decryptedTest')