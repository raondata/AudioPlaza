
import torch
import numpy as np
torch.set_num_threads(1)

class trimmer:
    def __init__(self, sample_rate=22050, dict_size=50):
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
        self.dict_size = dict_size


    def __find_speech_points(self, ts, audio):
        startpoint_16, endpoint_16 = ts[0]["start"], ts[-1]["end"]
        spare_front = 0
        spare_back = 0

        if startpoint_16-3000 < 0:
            startpoint_16 = 0
            spare_front = ts[0]["start"] - startpoint_16
        else:
            startpoint_16 = startpoint_16 - 3000
            spare_front = 3000
        if endpoint_16+3000 > len(audio):
            endpoint_16 = len(audio)
            spare_back = endpoint_16 - ts[-1]["end"]
        else:
            endpoint_16 = endpoint_16 + 3000
            spare_back = 3000

        spare_front_sec = spare_front / 16000
        spare_back_sec = spare_back / 16000

        if self.sample_rate != 16000:
            startpoint = int(startpoint_16 * self.sample_rate / 16000)
            endpoint = int(endpoint_16 * self.sample_rate / 16000)
        return startpoint, endpoint, spare_front_sec, spare_back_sec
    
    def __make_noise_samples(self, ts, cal_audio):
        not_voice_area = np.zeros(len(cal_audio))
        for i in range(len(ts)):
            not_voice_area[ts[i]["start"]:ts[i]["end"]] = 1
        
        noise_samples = []
        for i in range(0, len(not_voice_area)-self.dict_size, self.dict_size):
            if not_voice_area[i:i+self.dict_size].sum() == 0:
                noise_samples.append(cal_audio[i:i+self.dict_size])
        return noise_samples        


    def __noised_pad(self, noise_samples, padding_sec):
        num_samples = int(padding_sec * self.sample_rate) // self.dict_size+1
        random_idx = np.random.randint(0, len(noise_samples), num_samples)
        noise = torch.cat([noise_samples[i] for i in random_idx], dim=0)[:int(padding_sec * self.sample_rate)]
        return noise


    def pad_audio(self, audio, startpoint, endpoint, padding_sec=0.3, noise_samples=None, audio_path=None, spare_front=0, spare_back=0):
        padding_sec_front = padding_sec - spare_front
        padding_sec_back = padding_sec - spare_back

        if noise_samples is None or len(noise_samples) == 0:
            print(f"The trimmer cannot make noise samples from Audio Path {audio_path}. The audio will be padded with zero.")
            base_size = int(padding_sec_front * self.sample_rate) + int(padding_sec_back*self.sample_rate) + (endpoint - startpoint)
            padded = torch.zeros(base_size, dtype=torch.float32)
            padded[int(padding_sec_front * self.sample_rate):int(padding_sec_front * self.sample_rate) + (endpoint - startpoint)] = audio[startpoint:endpoint]
            return padded
        else:
            base_size = int(padding_sec * self.sample_rate) + int(padding_sec*self.sample_rate) + (endpoint - startpoint)
            padded_front = self.__noised_pad(noise_samples, padding_sec_front)
            padded_back = self.__noised_pad(noise_samples, padding_sec_back)
            padded = torch.cat([padded_front, audio[startpoint:endpoint], padded_back], dim=0)
            return padded


    def trim(self, audio_path, output_path, padding_sec=0.3):
        cal_audio = self.read_audio(audio_path, sampling_rate=16000)
        speech_timestamps = self.get_speech_timestamps(cal_audio, self.model, sampling_rate=16000)
        noise_samples = self.__make_noise_samples(speech_timestamps, cal_audio)
        startpoint, endpoint, spare_front, spare_back = self.__find_speech_points(speech_timestamps, cal_audio)

        if startpoint >= endpoint:
            raise ValueError("Audio is not valid.")

        if self.sample_rate != 16000:
            audio = self.read_audio(audio_path, sampling_rate=self.sample_rate)
        
        padded_audio = self.pad_audio(audio, startpoint, endpoint, padding_sec=padding_sec, noise_samples=noise_samples, audio_path=audio_path, spare_front=spare_front, spare_back=spare_back)
        self.save_audio(output_path, padded_audio, self.sample_rate)
        return padded_audio
        
    

if __name__ == "__main__":
    trimmer = trimmer()
    trimmer.trim("test.wav", "trim_noise.wav")



    