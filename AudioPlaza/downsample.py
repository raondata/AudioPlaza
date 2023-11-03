import os

def audio_downsample(from_path, to_path, sr=22050):
    if not os.path.exists(to_path):
        os.makedirs(os.path.dirname(to_path), exist_ok=True)

    os.system(f"ffmpeg -y -v quiet -i '{from_path}'-ac 1 -ab 32k -c:a pcm_s16le -ar {sr} -ac 1 '{to_path}'")