import torch
torch.set_num_threads(1)

class trimmer:
    def __init__(self, sample_rate=22050, pad="zero"):
        self.USE_ONNX = False
        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True,
                              onnx=self.USE_ONNX)
        
        (self.get_speech_timestamps,
        self.save_audio,
        self.read_audio,
        self.VADIterator,
        self.collect_chunks) = utils

        self.sample_rate = sample_rate
        if pad not in ["zero", "one", "repeat"]:
            raise ValueError("pad must be one of zero, one, repeat")
        else:
            self.pad = pad


    def __find_speech_points(self, ts):
        startpoint_16, endpoint_16 = ts[0]["start"], ts[-1]["end"]
        if self.sample_rate != 16000:
            startpoint = int(startpoint_16 * self.sample_rate / 16000)
            endpoint = int(endpoint_16 * self.sample_rate / 16000)
        return startpoint, endpoint
    

    def pad_audio(self, audio, startpoint, endpoint, padding_sec=0.3):
        base_size = int(padding_sec * self.sample_rate) *2 + (endpoint - startpoint)
        padded = torch.zeros(base_size, dtype=torch.float32)
        padded[int(padding_sec * self.sample_rate):int(padding_sec * self.sample_rate) + (endpoint - startpoint)] = audio[startpoint:endpoint]

        if self.pad == "one":
            padded[:int(padding_sec * self.sample_rate)] = 1
            padded[-int(padding_sec * self.sample_rate):] = 1
        elif self.pad == "repeat":
            padded[:int(padding_sec * self.sample_rate)] = audio[startpoint]
            padded[-int(padding_sec * self.sample_rate):] = audio[endpoint]
        return padded


    def trim(self, audio_path, output_path, padding_sec=0.3):
        cal_audio = self.read_audio(audio_path, sampling_rate=16000)
        speech_timestamps = self.get_speech_timestamps(cal_audio, self.model, sampling_rate=16000)
        startpoint, endpoint = self.__find_speech_points(speech_timestamps)

        if startpoint >= endpoint:
            raise ValueError("Audio is not valid.")

        if self.sample_rate != 16000:
            audio = self.read_audio(audio_path, sampling_rate=self.sample_rate)
        
        padded_audio = self.pad_audio(audio, startpoint, endpoint, padding_sec=padding_sec)
        self.save_audio(output_path, padded_audio, self.sample_rate)
        return padded_audio
        
    

if __name__ == "__main__":
    trimmer = trimmer()
    trimmer.trim("test.wav", "test_trimmed.wav")



    