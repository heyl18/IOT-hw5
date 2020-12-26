from utils import open_wave_file
import pyaudio
import wave
import datetime
import scipy.signal as signal
import numpy as np

def record_file(record_seconds = 5, wave_output_filename = "recordfile.wav", ret = False):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    RECORD_SECONDS = record_seconds
    WAVE_OUTPUT_FILENAME = wave_output_filename

    p = pyaudio.PyAudio()
    time2 = datetime.datetime.timestamp(datetime.datetime.now())
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    #print("开始录音......")
    time3 = datetime.datetime.timestamp(datetime.datetime.now())
    print(time3, time2)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    #print("录音结束!")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    if ret:
        return time3

if __name__ == '__main__':
    record_file(10)