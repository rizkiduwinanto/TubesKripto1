import wave
import struct
import sys
import base64

class LeastSignificantBit:
  def __init__(self, audio_path):
    self.audio_path = audio_path
    self.audio = wave.open(self.audio_path, "r")
    self.audio_frames = self.audio_to_frames()
    self.frame_rate = self.audio.getframerate()

  def audio_to_frames(self):
    frame_length = self.audio.getnframes()
    audio_frames = []
    for _ in range(0, frame_length):
      frame = self.audio.readframes(1)
      data = struct.unpack("<h", frame)
      audio_frames.append(data[0])
    return audio_frames
  
  def write_wave(self, new_audio_frames, sample_rate, output_path):
    new_wave = wave.open(output_path, "w")
    new_wave.setnchannels(1)
    new_wave.setsampwidth(2)
    new_wave.setframerate(sample_rate)
    for frames in new_audio_frames:
      byte_type = struct.pack("<h", frames)
      new_wave.writeframes(byte_type)
    new_wave.close()

  def write_output_file(self, message, output_path):
    bytes_message = message.encode('utf-8')
    with open(output_path, "wb") as file:
      file.write(bytes_message)
    file.close()

  @staticmethod
  def file_to_intlist(file_input_path):
    file = open(file_input_path, "rb")
    file_byte = file.read()
    file_intlist = []
    for byte in bytearray(file_byte):
      file_intlist.append(byte)
    file_intlist.append(0)
    return file_intlist

  @staticmethod
  def write_bit(integer, bit):
    return (integer | 0x01) if bit else (integer & ~0x01)

  @staticmethod
  def read_bit(integer, position):
    return ((0x01 << position & abs(integer)) >> position)
  
  def encode(self, message_input_path, key, output_wave_path):
    extension = message_input_path.split('.').pop()
    message_integer_list = self.file_to_intlist(message_input_path)
    total_bytes = len(message_integer_list)
    total_bits = total_bytes * 8
    total_frames = len(self.audio_frames)
    new_audio_frames = []
    index_audio = 0
    if total_bits <= total_frames:
      for int in message_integer_list:
        for index in range(7, -1, -1):
          new_int = self.write_bit(abs(self.audio_frames[index_audio]), self.read_bit(int, index))
          if (self.audio_frames[index_audio] != abs(self.audio_frames[index_audio])):
            new_audio_frames.append(-1 * new_int)
          else:
            new_audio_frames.append(new_int)
          index_audio += 1
      self.write_wave(new_audio_frames + self.audio_frames[index_audio:], self.frame_rate, output_wave_path)
    else:
      print('Payload Excedded')

  def decode(self, key, output_message_path):
    total_frames = len(self.audio_frames)
    bitlist = []
    for bits in self.audio_frames:
      bitlist.append(self.read_bit(abs(bits), 0))
    total_bytes = int(len(bitlist)/8)
    new_byte = ""
    end_byte = False
    count = 0
    message = []
    for index in range(total_bytes):
      if count < 8 and end_byte == False:
        new_byte += str(bitlist[index])
        count += 1
      elif count >= 8:
        char = int(new_byte, 2)
        if (char == 0):
          end_byte = True
        message.append(chr(char))
        new_byte = ""
        count = 0
        new_byte += str(bitlist[index])
        count += 1
      elif end_byte:
        string_message = ""
        message.pop()
        for char in message:
          string_message += char
        self.write_output_file(string_message, output_message_path)
        break
 
if __name__ == "__main__":
  lsb_encode = LeastSignificantBit("../Data/Vietnam.wav")
  lsb_encode.encode("../Message/rinaldi.jpg", "CEBONG", '../New4.wav')

  lsb_decode = LeastSignificantBit('../New4.wav')
  lsb_decode.decode("CEBONG", "../dosbing.jpg")
