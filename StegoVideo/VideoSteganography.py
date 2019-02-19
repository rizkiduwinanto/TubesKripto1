import base64
import cv2
import numpy as np
import random
import sys
import VideoParser

def encode(videoFile, messageFile, secretKey, flagEncrypt, flagRandom, flagtwoLSB, outputFilename):
    fileBits, metadataBits = getEncodedBits(messageFile, secretKey, flagEncrypt, flagRandom, flagtwoLSB)
    video = VideoParser.getVideo(videoFile)
    frames = video.frames
    encodedFrames = []
    totalBitInFrame = video.width * video.height * 3
    maxHeight = video.height
    maxWidth = video.width
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
        if flagRandom:
            seed = sum(ord(alphabet) for alphabet in secretKey)
            random.seed(seed)
            bit_order = [[int(random.random()*(video.lenFrames-2)+1),int(random.random()*(video.height-1)),int(random.random()*(video.width)),int(random.random()*(2))] for i in range(len(fileBits))]
            for order in range(len(fileBits)):
                currPixelRGB = frames[bit_order[order][0]][bit_order[order][1]][bit_order[order][2]][bit_order[order][3]]
                if flagtwoLSB:
                    frames[bit_order[order][0]][bit_order[order][1]][bit_order[order][2]][bit_order[order][3]] = changeTwoLSB(currPixelRGB, fileBits[order])
                else:
                    frames[bit_order[order][0]][bit_order[order][1]][bit_order[order][2]][bit_order[order][3]] = changeLSB(currPixelRGB, fileBits[order])
            encodedFrames = frames
            VideoParser.writeVideo(frames, video.fps, video.width, video.height, outputFilename)
        else:
            currFrame = 1
            currHeight = 0
            currWidth = 0
            currRGB = 0
            x = 0
            # print('data')
            for bit in fileBits:
                currPixelRGB = frames[currFrame][currHeight][currWidth][currRGB]
                if flagtwoLSB:
                    frames[currFrame][currHeight][currWidth][currRGB] = changeTwoLSB(currPixelRGB, bit)
                else:
                    frames[currFrame][currHeight][currWidth][currRGB] = changeLSB(currPixelRGB, bit)
                x += 1
                print('%d. %d -> %d - > %d' % (x, currPixelRGB, bit, frames[currFrame][currHeight][currWidth][currRGB]))
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
    message_flag_encrypt = True if metadata[2] == 'True' else False
    message_flag_random = True if metadata[3] == 'True' else False
    message_flag_twoLSB = True if metadata[4] == 'True' else False
    
    # Parse message
    message_bit = []
    bit_list_size = (message_size*4) if message_flag_twoLSB else (message_size*8) 
    if message_flag_random:
        seed = sum(ord(alphabet) for alphabet in secretKey)
        random.seed(seed)
        bit_order = [[int(random.random()*(video.lenFrames-2)+1),int(random.random()*(video.height-1)),int(random.random()*(video.width)),int(random.random()*(2))] for i in range(bit_list_size)]
        for order in range(bit_list_size):
            currPixelRGB = frames[bit_order[order][0]][bit_order[order][1]][bit_order[order][2]][bit_order[order][3]]
            if message_flag_twoLSB:
                message_bit.append(getTwoLSB(currPixelRGB))
            else:
                message_bit.append(getLSB(currPixelRGB))
    else:
        for i in range(bit_list_size):
            currPixelRGB = frames[currFrame][currHeight][currWidth][currRGB]
            if message_flag_twoLSB:
                message_bit.append(getTwoLSB(currPixelRGB))
            else: #(indent yg di bawah pls)
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

    # double lsb
    if message_flag_twoLSB:
        message_byte = "".join(chr(int("".join(map(str,message_bit[i:i+4])),4)) for i in range(0,len(message_bit),4))
    else:
        message_byte = "".join(chr(int("".join(map(str,message_bit[i:i+8])),2)) for i in range(0,len(message_bit),8))
    # decrypt kalo perlu
    message_byte = decrypt_vigener(message_byte, secretKey) if message_flag_encrypt else message_byte
    # write message into file
    writeOutput(message_byte, message_extension, outputFilename)
    return

def getEncodedBits(filename, key, flagEncrypt, flagRandom, flag_twoLSB):
    with open(filename, "rb") as file:
      file_byte = file.read()
    byte_message = base64.b64encode(file_byte).decode('utf-8')
    byte_message = encrypt_vigenere(byte_message, key) if flagEncrypt else byte_message
    extension = filename.split('.').pop()
    length_message = len(byte_message)
    string_metadata = str(length_message) + '#' + extension + '#' + str(flagEncrypt) + '#' + str(flagRandom) + '#' + str(flag_twoLSB) + '#'
    message_bit_list = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in byte_message])))
    metadata_bit_list = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string_metadata])))
    if flag_twoLSB:
       message_twobit_list = [message_bit_list[i]*2+message_bit_list[i+1] for i in range(0, len(message_bit_list),2)]
       return message_twobit_list, metadata_bit_list
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

def getTwoLSB(data):
    return data & 3

def changeLSB(data, lsb):
    return (data & 254 | lsb)

def changeTwoLSB(data, lsb):
    return (data & 253) & (data & 254) | lsb

if __name__ == "__main__":
    #encode('test.avi', 'test.txt', 'SECRET', False, False, False, 'res.avi')
    #decode('res.avi', 'SECRET', 'res')
    #encode('test.avi', 'test.txt', 'SECRET', True, False, False, 'resEncrypted.avi')
    #decode('resEncrypted.avi', 'SECRET', 'decryptedTest')
    #encode('test.avi', 'test.txt', 'SECRET', False, True, False, 'resRandom.avi')
    #decode('resRandom.avi', 'SECRET', 'randomTest')
    #encode('test.avi', 'test.txt', 'SECRET', True, True, False, 'resEncryptedRandom.avi')
    #decode('resEncryptedRandom.avi', 'SECRET', 'encryptedRandomTest')
    #encode('test.avi', 'test.txt', 'SECRET', False, False, True, 'resDouble.avi')
    #decode('resDouble.avi', 'SECRET', 'double')
    #encode('test.avi', 'test.txt', 'SECRET', True, False, True, 'encryptedDouble.avi')
    #decode('encryptedDouble.avi', 'SECRET', 'encryptedDouble')
    #encode('test.avi', 'test.txt', 'SECRET', False, True, True, 'randomDouble.avi')
    #decode('randomDouble.avi', 'SECRET', 'randomDouble')
    encode('test.avi', 'test.txt', 'SECRET', True, True, True, 'allFlag.avi')
    decode('allFlag.avi', 'SECRET', 'allFlag')