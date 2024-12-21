import pysrt
import time
import pyperclip
import vlc
from tkinter import Tk, filedialog
from datetime import datetime, timedelta
import sys

# Pastikan encoding terminal UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def select_file(file_types):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=file_types)
    return file_path

def parse_srt_file(file_path):
    try:
        subtitles = pysrt.open(file_path, encoding='utf-8')
        return subtitles
    except Exception as e:
        print(f"Error reading subtitle file: {e}")
        return None

def get_current_subtitle(subtitles, current_time):
    for subtitle in subtitles:
        start_time = timedelta(hours=subtitle.start.hours, minutes=subtitle.start.minutes, seconds=subtitle.start.seconds, milliseconds=subtitle.start.milliseconds)
        end_time = timedelta(hours=subtitle.end.hours, minutes=subtitle.end.minutes, seconds=subtitle.end.seconds, milliseconds=subtitle.end.milliseconds)
        if start_time <= current_time <= end_time:
            return subtitle.text
    return None

def play_video_with_subtitles(video_path, subtitle_path):
    subtitles = parse_srt_file(subtitle_path)
    if not subtitles:
        return

    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(video_path)
    player.set_media(media)

    player.play()
    time.sleep(1)
    print("Video started. Subtitles will be copied to clipboard...")

    start_time = datetime.now()
    last_text = None

    try:
        while True:
            elapsed_time = datetime.now() - start_time
            current_text = get_current_subtitle(subtitles, elapsed_time)
            if current_text and current_text != last_text:
                pyperclip.copy(current_text)
                print(f"Subtitle copied to clipboard: {current_text}")
                last_text = current_text
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped.")
        player.stop()

print("Select your video file:")
video_file = select_file([("Video files", "*.mp4 *.mkv *.avi")])
if not video_file:
    print("No video file selected. Exiting...")
    exit()

print("Select your subtitle file:")
subtitle_file = select_file([("Subtitle files", "*.srt")])
if not subtitle_file:
    print("No subtitle file selected. Exiting...")
    exit()

play_video_with_subtitles(video_file, subtitle_file)