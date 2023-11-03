import soundfile as sf


class DurationStatistic:
    def __init__(self, count_secs, folder_path, max_filename, min_filename):
        self.count_secs = count_secs
        self.total_secs = sum(count_secs)
        self.total_hours = self.total_secs / 3600
        self.len_files = len(count_secs)
        self.mean_second_per_file = self.total_secs / self.len_files
        self.min_second = min(count_secs)
        self.max_second = max(count_secs)
        self.max_filename = max_filename
        self.min_filename = min_filename
        self.text_format = "Total {} files, {:.2f} hours, {:.2f} seconds per file\nMax Sec: {:.2f}, Min sec:{:.2f}".format(
            self.len_files, self.total_hours, self.mean_second_per_file, self.max_second, self.min_second
        )
        self.folder_path = folder_path

    def __str__(self):
        return self.text_format
    
    def draw_plot(self, save_path):
        import plotly.express as px

        fig = px.histogram(x=self.count_secs, nbins=100)
        fig.update_layout(
            title="Duration of {} files".format(self.len_files),
            xaxis_title="Duration (seconds)",
            yaxis_title="Count",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
        fig.add_annotation(
            x=self.max_second,
            y=0,
            xref="x",
            yref="y",
            text="{:.2f}".format(self.max_second),
            showarrow=True,
            # arrowhead=1,
            ax=0,
            ay=-40
        )
        fig.add_annotation(
            x=self.min_second,
            y=0,
            xref="x",
            yref="y",
            text="{:.2f}".format(self.min_second),
            showarrow=True,
            # arrowhead=1,
            ax=0,
            ay=-40
        )
        fig.write_image(save_path)


def get_duration(filename):
    f = sf.SoundFile(filename)
    return f.frames / f.samplerate

def get_folder_duration(folder)->DurationStatistic:
    from glob import glob
    from tqdm import tqdm
    count_secs = []
    max_filename = ""
    min_filename = ""
    max_sec = 0
    min_sec = float("inf")
    for idx, file in enumerate(tqdm(sorted(glob(f"{folder}/*.wav")))):
        count_secs.append(get_duration(file))
        if count_secs[-1] > max_sec:
            max_sec = count_secs[-1]
            max_filename = file
        if count_secs[-1] < min_sec:
            min_sec = count_secs[-1]
            min_filename = file
    
    return DurationStatistic(count_secs, folder, max_filename, min_filename)