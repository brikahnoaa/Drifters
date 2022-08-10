import sys
from scipy.io import wavfile
import whale_call_detection as wcd

def main(audio_file_path):
    fs, data = wavfile.read(audio_file_path)
    return wcd.detect_whale_call_from_audio(data, fs)

if __name__ == '__main__':
    print(main(sys.argv[1]))