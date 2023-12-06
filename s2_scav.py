import os
import subprocess
import datetime
import json
from subtitles import Subtitles
from yuvhistogram import yuvhistogram

class S2:
    def cut_video(input_path):
        output_path = "/mnt/d/Download/s2_scav/BBBseconds.mp4"
        seconds = int(input("Please enter the number of seconds to cut from the video: "))
        end_time = str(datetime.timedelta(seconds=seconds))
        os.system(f'ffmpeg -i {input_path} -ss 00:00:00 -t {end_time} -c:v copy -c:a copy {output_path}')
    def show_macroblocs_motionvectors(input_path):
        output_path = "/mnt/d/Download/s2_scav/BBB_mmv.mp4"
        os.system(f'ffmpeg -hide_banner -flags2 +export_mvs -i {input_path} -vf codecview=mv=pf+bf+bb -an {output_path}')

    
    def custom_bbb(input_path):

        output_path = "/mnt/d/Download/s2_scav/BBBc50.mp4"
        output_mono = "/mnt/d/Download/s2_scav/BBB50mono.mp3"
        output_stereolb = "/mnt/d/Download/s2_scav/BBB50stereolb.mp3"
        output_aac = "/mnt/d/Download/s2_scav/BBB50aac.aac"
        output_final = "/mnt/d/Download/s2_scav/BBB_final.mp4"
        #Cut BBB into 50 seconds only video.
        os.system(f'ffmpeg -i {input_path} -t 50 -c:v copy -c:a copy {output_path}')

        #Export BBB(50s) audio as MP3 mono track.
        os.system(f'ffmpeg -i {output_path} -vn -ac 1 -ab 128k {output_mono}')

        #Export BBB(50s) audio in MP3 stereo w/ lower bitrate
        os.system(f'ffmpeg -i {output_path} -vn -q:a 5 {output_stereolb}')

        #Export BBB(50s) audio in AAC codec
        os.system(f'ffmpeg -i {output_path} -vn -c:a aac {output_aac}')

        #Packaging everything in a .mp4:
        os.system(f'ffmpeg -i {output_path} -i {output_mono} -i {output_stereolb} -i {output_aac} -c:v copy -c:a copy {output_final}')

    def count_tracks(input_path):

        result = subprocess.run(f'ffprobe -v error -show_entries stream=index,codec_name,codec_type -of json {input_path}',shell=True,check=True,capture_output=True,text=True)

        # Access the stdout attribute of the CompletedProcess object
        stracks = result.stdout

        # Load the JSON data from the string
        json_data = json.loads(stracks)

        # Check if json_data has 'streams' property and get its length
        num_tracks = len(json_data.get('streams', []))
        print(f'The container contains {num_tracks} track(s).')



def main():
    while True:
        n = input(
            "1.- Cut 9 seconds and show macroblocks/motion vectors\n2.- Create new BBB container\n3.- Count tracks\n"
            "4.- Integrate subtitles\n5.- Extract YUV histogram\n6.- Exit\n")

        n = int(n)

        # Menu with cases
        match n:
            case 1:
                print("Cutting 9 seconds and showing macroblocks/motion vectors")
                path = "/mnt/d/Download/s2_scav/BBB.mp4"
                S2.cut_video(path)
                output_path = "/mnt/d/Download/s2_scav/BBBseconds.mp4"
                S2.show_macroblocs_motionvectors(output_path)
            case 2:
                print("Creating new BBB container")
                path = "/mnt/d/Download/s2_scav/BBBseconds.mp4"
                S2.custom_bbb(path)
            case 3:
                print("Counting tracks")
                path = "/mnt/d/Download/s2_scav/BBB_final.mp4"
                S2.count_tracks(path)
            case 4:
                print("Integrating subtitles")
                sub = Subtitles("/mnt/d/Download/s2_scav/BBBseconds.mp4","/mnt/d/Download/s2_scav/cars_subtitles.srt")
                sub.integrate_subtitles("/mnt/d/Download/s2_scav/BBBsub.mp4")
            case 5:
                print("Extracting YUV histogram")
                path = "/mnt/d/Download/s2_scav/BBBseconds.mp4"
                output = "/mnt/d/Download/s2_scav/BBBhistogram.mp4"
                yuvhistogram(path,output)
            case 6:
                print("Exit")
                exit()
            case _:
                print("You entered an invalid input. Choose [1, 2, 3, 4, 5, 6, or 7]")


if __name__ == "__main__":
    main()