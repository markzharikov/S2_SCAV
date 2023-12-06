import subprocess
import os

def yuvhistogram(input_path, output_video):
    base_name, ext = os.path.splitext(os.path.basename(input_path))
    os.system(f'ffmpeg -hide_banner -i {input_path} -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay" {base_name}_with_histogram{ext}')