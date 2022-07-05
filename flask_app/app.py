from flask import Flask
import pyaudio
import wave
import asyncio
from ShazamAPI import Shazam
from flask import render_template,request,redirect

app =Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html',pageTitle='Discover Tunes')

@app.route('/listen', methods=['POST','GET'])
def listen():
	if request.method=='POST':
		form=request.form
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		CHUNK = 1024
		RECORD_SECONDS = 10
		WAVE_OUTPUT_FILENAME = "record.wav"
		 
		audio = pyaudio.PyAudio()
		 
		# start Recording
		stream = audio.open(format=FORMAT, channels=CHANNELS,
		                rate=RATE, input=True,
		                frames_per_buffer=CHUNK)
		print ("recording sample...")
		frames = []
		 
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    frames.append(data)
		print ("finished recording")
		 
		 
		# stop Recording
		stream.stop_stream()
		stream.close()
		audio.terminate()
		 
		waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		waveFile.setnchannels(CHANNELS)
		waveFile.setsampwidth(audio.get_sample_size(FORMAT))
		waveFile.setframerate(RATE)
		waveFile.writeframes(b''.join(frames))
		waveFile.close()


		mp3_file_content_to_recognize = open('record.WAV', 'rb').read()
		shazam = Shazam(mp3_file_content_to_recognize)
		recognize_generator =shazam.recognizeSong()
		while request.is_json:
			return (recognize_generator)

	def myoutput():
		global myoutput
		myoutput=list(recognize_generator)
		title=myoutput[0]
		print(myoutput[1])
		return myoutput


	return render_template('index.html',display=myoutput(), pageTitle='Discover Tunes')

	return redirect("/")


if __name__=='__main__':
	app.run(debug=True)
