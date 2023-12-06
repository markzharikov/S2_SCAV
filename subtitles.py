import subprocess
import os

class Subtitles:
    def __init__(self, input_path, subtitles_path):
        self.input_path = input_path
        self.subtitles_path = subtitles_path

    def integrate_subtitles(self, output_path):
        # Embedding the subtitles into the video using ffmpeg with re-encoding
        base_name, _ = os.path.splitext(output_path)
        subprocess.run(f"ffmpeg -i {self.input_path} -vf subtitles={self.subtitles_path} -c:a aac -c:v libx264 {base_name}_with_subtitles.mp4", shell=True, check=True)

