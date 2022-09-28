#!/usr/bin/python3
import sys
from scipy.io import wavfile
import whale as wcd

def main(audio_file_path):
    fs, data = wavfile.read(audio_file_path)
    return wcd.detect_whale_call_from_audio(data, fs)

result=main(sys.argv[1])
if __name__ == '__main__':
    print(result)

sys.exit(0 if result else 1)
