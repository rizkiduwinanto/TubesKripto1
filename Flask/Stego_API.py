from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

from LSB import LeastSignificantBit

@app.route("/")
def index():
  return render_template('index.html')

@app.route('/lsb/encode', methods = ['GET', 'POST'])
def encode_lsb():
  if request.method == 'POST':
    message = request.files['message']
    audio_wave = request.files['audio-wave']
    key = request.form['key']
    encrypt = request.form['encrypt']
    random = request.form['random']
    message.save(secure_filename(message.filename))
    audio_wave.save(secure_filename(audio_wave.filename))
    filename = audio_wave.filename.split('.')
    encoded_file = filename[0] + '_encoded.wav'
    LSB_encode = LeastSignificantBit(audio_wave.filename)
    LSB_encode.encode(message.filename, key, encoded_file, bool(encrypt), bool(random))
    return render_template('index.html', wave_file=audio_wave.filename, encoded_file=encoded_file)

@app.route('/download/', methods = ['GET', 'POST'])
def download():
  pass
  
@app.route('/lsb/decode', methods = ['GET', 'POST'])
def decode_lsb():
  if request.method == 'POST':
    audio_wave = request.files['audio-wave']
    key = request.form['key']
    audio_wave.save(secure_filename(audio_wave.filename))
    LSB_decode = LeastSignificantBit(audio_wave.filename)
    LSB_decode.decode(key, 'test')
    return 'File Decoded Succesfully'