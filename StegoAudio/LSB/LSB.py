import wave
import base64
import random

class LeastSignificantBit:
  def __init__(self, audio_path):
    self.audio_path = audio_path
    self.audio = wave.open(self.audio_path, "r")
    self.frame_length = self.audio.getnframes()
    self.audio_params = self.audio.getparams()
    self.audio_bytes = self.audio_to_bytes()

  def audio_to_bytes(self):
    bytes = bytearray(list(self.audio.readframes(self.frame_length)))
    return bytes

  @staticmethod
  def message_to_bytes(input_path):
    with open(input_path, "rb") as file:
      file_byte = file.read()
    return base64.b64encode(file_byte).decode('utf-8')
  
  def write_wave(self, frame_encoded, output_path):
    with wave.open(output_path, 'wb') as wav_file:
      wav_file.setparams(self.audio_params)
      wav_file.writeframes(frame_encoded)

  def write_output_file(self, message, extension, output_path):
    file_byte = base64.b64decode(message.encode('utf-8'))
    with open(output_path + '.' + extension, 'wb') as file:
      file.write(file_byte)
    
  @staticmethod
  def encrypt_vigener(plaintext, key):
    plaintext_int = [ord(letter) for letter in plaintext]
    key_int = [ord(letter) for letter in key]
    ciphertext = ''
    for index in range(len(plaintext_int)):
      value = plaintext_int[index] + key_int[index % len(key_int)]
      ciphertext += chr(value % 256)
    return ciphertext
  
  def encode(self, message_input_path, key, output_wave_path, flag_encrypt, flag_random):
    byte_message = self.message_to_bytes(message_input_path)
    byte_message = self.encrypt_vigener(byte_message, key) if flag_encrypt else byte_message
    extension = message_input_path.split('.').pop()
    length_message = len(byte_message)
    string_message = byte_message + '#' + extension + '#' + str(length_message) + '#' + str(flag_encrypt) + '#' + str(flag_random) + '#'
    bits_message = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string_message])))
    # seed = sum(ord(alphabet) for alphabet in key)
    # random.seed(seed)
    # random.shuffle(bits_message)
    if len(bits_message) <= len(self.audio_bytes):
      for index, bit in enumerate(bits_message):
        self.audio_bytes[index] = (self.audio_bytes[index] & 254) | bit
      self.write_wave(self.audio_bytes, output_wave_path)
    else:
      print('Payload Excedeed')

  @staticmethod
  def decrypt_vigener(ciphertext, key):
    ciphertext_int = [ord(letter) for letter in ciphertext]
    key_int = [ord(letter) for letter in key]
    plaintext = ''
    for index in range(len(ciphertext_int)):
      value = ciphertext_int[index] - key_int[index % len(key_int)]
      plaintext += chr(value % 256)
    return plaintext

  def decode(self, key, output_message_path):
    bits_extracted = [self.audio_bytes[i] & 1 for i in range(len(self.audio_bytes))]
    # seed = sum(ord(alphabet) for alphabet in key)
    # random.seed(seed)
    # random.shuffle(bits_extracted)
    string_message = "".join(chr(int("".join(map(str,bits_extracted[i:i+8])),2)) for i in range(0,len(bits_extracted),8))
    splitted_string = string_message.split('#')
    raw_message = splitted_string[0]
    extension = splitted_string[1]
    flag_decrypt = splitted_string[3]
    flag_random = splitted_string[4]
    message = self.decrypt_vigener(raw_message, key) if flag_decrypt == 'True' else raw_message
    self.write_output_file(message, extension, output_message_path)
 
if __name__ == "__main__":
  lsb_encode = LeastSignificantBit("../Data/LRMonoPhase4.wav")
  lsb_encode.encode("../Message/plongaplongo.png", "TOLOL", '../GOT7.wav', True, True)

  lsb_decode = LeastSignificantBit('../WEMUSTLOVE.wav')
  lsb_decode.decode("TOLOL", "../jokodok")
