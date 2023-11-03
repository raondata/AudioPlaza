## Install Ubuntu Packages

```bash
sudo apt update
sudo apt install ffmpeg
apt-get install wget
```

## Using Example

1. Audio Downsample
```python
from AudioPlaza.downsample import audio_downsample
input_path = "./input.wav" # 입력 파일명
out_path = "./out.wav" # 출력 파일명
sample_rate = 22050 # 샘플레이트 (22.05 khz)

audio_downsample(input_path, out_path, sr=sample_rate)
```

2. Audio Trimming
```python
from AudioPlaza.trim import trimmer
input_path = "./input.wav" # 입력 파일명
out_path = "./out.wav" # 출력 파일명
sample_rate = 22050 # 샘플레이트 (22.05 khz)
padding_sec = 0.3 # 앞 뒤로 패딩을 몇초 줄건지

tr = trimmer(sample_rate=sample_rate, pad="zero") # pad = "zero", "one", "repeat"
tr.trim(input_path, out_path, padding_sec=padding_sec)
```

3. Download Audio from Google Drive
```python
from AudioPlaza.googledrive import gdown
fid = ""
fname = ""

gdown(fid, fname)
```

4. Get Audio Duration Statistics
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
