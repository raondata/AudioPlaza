## Install Ubuntu Packages

```bash
sudo apt update
sudo apt install ffmpeg
apt-get install wget
```
* Pre-install those packages using ubuntu `apt`

## Install using pip
```bash
pip install AudioPlaza
```
* You can install this from PYPI, pip.

## Using Example

1. Audio Downsample
```python
from AudioPlaza.downsample import audio_downsample
input_path = "./input.wav" # 입력 파일명
out_path = "./out.wav" # 출력 파일명
sample_rate = 22050 # 샘플레이트 (22.05 khz)
audio_downsample(input_path, out_path, sr=sample_rate)
```

2. Audio Trimming/Padding 1 (Zero, One, Repeat Padding)
* 그냥 0, 1, 맨 끝 오디오를 기반으로 패팅
* 너무 길면 트리밍
* 같은 숫자로 하기 때문에 미세한 노이즈가 반영되지 못하는 경우가 존재

```python
from AudioPlaza.trim1 import trimmer
input_path = "./input.wav" # 입력 파일명
out_path = "./out.wav" # 출력 파일명
sample_rate = 22050 # 샘플레이트 (22.05 khz)
padding_sec = 0.3 # 앞 뒤로 패딩을 몇초 줄건지
tr = trimmer(sample_rate=sample_rate, pad="zero") # pad = "zero", "one", "repeat"
tr.trim(input_path, out_path, padding_sec=padding_sec)
```

3. Audio Trimming 2 (Noise Sampling)
* 노이즈(말이 아닌 부분)을 샘플링하여 만들고, 이를 패딩에 활용해주는 기법.
* 말이 뚝 짤리는 등의 문제는 해결할 수 없지만, 0으로 되어 소리가 끊겨 모델의 학습에 부정적 영향을 주는 경우는 방지.
```python
from AudioPlaza.trim2 import trimmer
input_path = "./input.wav" # 입력 파일명
out_path = "./out.wav" # 출력 파일명
sample_rate = 22050 # 샘플레이트 (22.05 khz)
padding_sec = 0.3 # 앞 뒤로 패딩을 몇초 줄건지
tr = trimmer(sample_rate=sample_rate, dict_size=50) # dict_size => 노이즈 딕셔너리의 사이즈 / 너무 크지 않게 주의 (50 기본값)
tr.trim(input_path, out_path, padding_sec=padding_sec)
```

4. Download Audio from Google Drive
```python
from AudioPlaza.googledrive import gdown
fid = ""
fname = ""
gdown(fid, fname)
```

5. Get Audio Duration Statistics
```python
from AudioPlaza.duration import get_duration, get_folder_duration
dur = get_duration("./audio.wav") 
print(dur) # ~~ sec
stat = get_folder_duration("./wavs/")
print(stat) # 정보
stat.draw_plot("./stat.png") #내용을 plot으로 그려서 시각화
```

## Version Information
* 0.0.1: Initial version with trim, downsample, googledrive, duration statistics. (Some features from RAONDIO)
