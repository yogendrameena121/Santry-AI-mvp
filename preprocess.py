import librosa
import numpy as np

def preprocess_audio(file_path):
    audio, sr = librosa.load(file_path, sr=16000)
    mel_spec = librosa.feature.melspectrogram(
        y=audio,
        sr=sr,
        n_mels=128
    )
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    return mel_spec_db
