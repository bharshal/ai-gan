from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import pyaudio
import wave
import copy
from time import strftime, gmtime
from sys import byteorder
from array import array
from struct import pack


THRESHOLD = 15000  # audio levels not normalised.
CHUNK_SIZE = 512
SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
RATE = 44100
CHANNELS = 1
TRIM_APPEND = RATE / 4

def is_silent(data_chunk):
	"""Returns 'True' if below the 'silent' threshold"""
	return max(data_chunk) < THRESHOLD

def normalize(data_all):
	"""Amplify the volume out to max -1dB"""
	# MAXIMUM = 16384
	normalize_factor = (float(NORMALIZE_MINUS_ONE_dB * FRAME_MAX_VALUE)
						/ max(abs(i) for i in data_all))

	r = array('h')
	for i in data_all:
		r.append(int(i * normalize_factor))
	return r

def trim(data_all):
	_from = 0
	_to = len(data_all) - 1
	for i, b in enumerate(data_all):
		if abs(b) > THRESHOLD:
			_from = max(0, i - TRIM_APPEND)
			break

	for i, b in enumerate(reversed(data_all)):
		if abs(b) > THRESHOLD:
			_to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)            
			break

	return copy.deepcopy(data_all[int(_from):(int(_to + 1000))])

def record():
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index= 0, frames_per_buffer=CHUNK_SIZE)
	silent_chunks = 0
	audio_started = False
	data_all = array('h')

	while True:
		# little endian, signed short
		data_chunk = array('h', stream.read(CHUNK_SIZE))
		if byteorder == 'big':
			data_chunk.byteswap()
		data_all.extend(data_chunk)

		silent = is_silent(data_chunk)

		if audio_started:
			if silent:
				silent_chunks += 1
				if silent_chunks > SILENT_CHUNKS:
					break
			else: 
				silent_chunks = 0
		elif not silent:
			print('Started')
			audio_started = True              

	sample_width = p.get_sample_size(FORMAT)
	stream.stop_stream()
	stream.close()
	p.terminate()

	data_all = trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
	data_all = normalize(data_all)
	return sample_width, data_all

def record_to_file():
	"Records from the microphone and outputs the resulting data to 'path'"
	path="./utils/words/record.wav"
	sample_width, data = record()
	data = pack('<' + ('h' * len(data)), *data)

	wave_file = wave.open(path, 'wb')
	wave_file.setnchannels(CHANNELS)
	wave_file.setsampwidth(sample_width)
	wave_file.setframerate(RATE)
	wave_file.writeframes(data)
	wave_file.close()

def get_sound():
	path='./utils/words/record.wav'
	sound_file = AudioSegment.from_wav(wav_path)
	audio_chunks = split_on_silence(sound_file,min_silence_len=150,silence_thresh=-45)
	for i, chunk in enumerate(audio_chunks):
		if (len(chunk) >= 400):
			print(len(chunk))
			x=len(chunk)
			silence=((1000-int(x))/2)
			print(silence)
			segment = AudioSegment.silent(duration=silence)  #duration in milliseconds
			#song = AudioSegment.from_wav(chunk)
			final = segment + chunk + segment
			out_file = path+new+"{0}.wav".format(i)
			print ("exporting", out_file)
			final.export(out_file, format="wav")

if __name__ == '__main__':
	wav_path='./mo160.wav'
	get_sound(wav_path)