import wave
import base64
import random
import numpy
import struct

DELAY = 0.002

class EchoHiding:
  def __init__(self, audio_path):
    self.audio_path = audio_path
    self.audio = wave.open(self.audio_path, 'rb')
    self.frame_length = self.audio.getnframes()
    self.frame_rate = self.audio.getframerate()
    self.channel = self.audio.getnchannels()
    self.audio_params = self.audio.getparams()
    self.echo = self.audio_to_echo()
    self.audio_echo_path = ''
    self.audio_echo = None

  def audio_to_echo(self):
    frames = self.audio.readframes(self.frame_length)
    echo = numpy.frombuffer(frames, dtype='h').reshape(-1, self.channel)
    return echo
  
  def create_echo_file(self):
    filename = self.audio_path.split('/')
    self.audio_echo_path = 'echo_' + filename[-1]
    with wave.open(self.audio_echo_path, 'wb') as echo_output:
      echo_output.setparams(self.audio_params)
      print(self.frame_length)
      for index in range(0, self.frame_length):
        if index > DELAY * self.frame_rate:
          value = self.echo[index] + 1 * self.echo[index - int(DELAY * self.frame_rate)]
        else:
          value = self.echo[index]

        if self.channel == 1 :
          packed_value = struct.pack('h', int(value[0]))
        else:
          packed_value = struct.pack('hh', int(value[0]), int(value[1]))
        echo_output.writeframes(packed_value)
    self.audio_echo = wave.open(self.audio_echo_path, 'rb')

  @staticmethod
  def message_to_bytes(input_path):
    with open(input_path, "rb") as file:
      file_byte = file.read()
    return base64.b64encode(file_byte).decode('utf-8')
  
  def write_wave(self, frames, output_path):
    with wave.open(output_path, 'wb') as wav_file:
      wav_file.setparams(self.audio_params)
      for frame in frames:
        wav_file.writeframes(frame)

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
    self.create_echo_file()
    byte_message = self.message_to_bytes(message_input_path)
    extension = message_input_path.split('.').pop()
    string_message = "#".join([byte_message, extension]) + '#'
    bits_message = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string_message])))
    if len(bits_message) <= self.frame_length:
      self.audio.rewind()
      self.audio_echo.rewind()
      new_frame = []
      print(bits_message[:10])
      for index in range(self.frame_length):
        frame_one = self.audio_echo.readframes(1024)
        frame_zero = self.audio.readframes(1024)
        if index < len(bits_message):
          if bits_message[index] == 0:
            new_frame.append(frame_zero)
          else:
            new_frame.append(frame_one)
        else:
          new_frame.append(frame_zero)
      self.write_wave(new_frame, output_wave_path)
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

  def decode(self, key, output_message_path, wave_real_path):
    real_file = wave.open(wave_real_path, 'rb')
    bits_extracted = []
    for _ in range(self.frame_length):
      hidden_frames = self.audio.readframes(1024)
      real_frames = real_file.readframes(1024)
      if hidden_frames == real_frames:
        bits_extracted.append(0)
      else:
        bits_extracted.append(1)
    string_message = "".join(chr(int("".join(map(str,bits_extracted[i:i+8])),2)) for i in range(0,len(bits_extracted),8))
    splitted_string = string_message.split('#')
    raw_message = splitted_string[0]
    extension = splitted_string[1]
    self.write_output_file(raw_message, extension, output_message_path)
 
if __name__ == "__main__":
  echo_hiding = EchoHiding("../Data/piano2.wav")
  echo_hiding.encode("../Message/Jokowi.txt", "KOMUNIS", '../Jaenudin.wav', False, False)

  echo_hiding_decode = EchoHiding('../Fuck1.wav')
  echo_hiding_decode.decode("KOMUNIS", "../mukidi", "../Data/piano2.wav")
