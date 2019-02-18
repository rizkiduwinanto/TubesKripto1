import wave
import base64
import random

class EchoHiding:
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
      print(self.audio_params)
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
    pass

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
    pass
 
if __name__ == "__main__":
  lsb_encode = LeastSignificantBit("../Data/LRMonoPhase4.wav")
  lsb_encode.encode("../Message/1200px-Flag_of_South_Korea.svg.png", "TOLOL", '../Fuck1.wav', False, True)

  lsb_decode = LeastSignificantBit('../Fuck1.wav')
  lsb_decode.decode("TOLOL", "../unicorn")
