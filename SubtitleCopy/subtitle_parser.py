import pysrt
import time
import pyperclip
import vlc
from tkinter import Tk, filedialog
from datetime import datetime, timedelta
import threading
import sys
import keyboard  # Untuk menangkap input keyboard

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

def monitor_subtitles(subtitles, player):
    """
    Fungsi untuk memonitor posisi video dan menyalin subtitle ke clipboard.
    """
    last_text = None
    try:
        while True:
            current_time = timedelta(seconds=player.get_time() / 1000)  # Waktu dalam detik
            current_text = get_current_subtitle(subtitles, current_time)
            if current_text and current_text != last_text:
                pyperclip.copy(current_text)
                print(f"Subtitle copied to clipboard: {current_text}")
                last_text = current_text
            time.sleep(0.1)  # Periksa setiap 0.1 detik
    except KeyboardInterrupt:
        print("\nStopped.")

def monitor_keyboard(player):
    """
    Fungsi untuk menangkap input keyboard untuk kontrol video.
    """
    is_paused = False
    last_press_time = None
    jump_duration = 5  # Default lompat 5 detik

    try:
        while True:
            current_time = time.time()

            # Pause/Resume dengan SPACE
            if keyboard.is_pressed("space"):
                if is_paused:
                    player.play()
                    print("Video Resumed")
                else:
                    player.pause()
                    print("Video Paused")
                is_paused = not is_paused
                time.sleep(0.3)  # Hindari deteksi ganda

            # Lompat 5 atau 10 detik ke depan
            if keyboard.is_pressed("right"):
                if last_press_time and current_time - last_press_time < 1:  # Tekan dalam waktu <1 detik
                    jump_duration = 10
                else:
                    jump_duration = 5

                current_time_ms = player.get_time()
                player.set_time(current_time_ms + jump_duration * 1000)  # Tambahkan dalam ms
                print(f"Skipped forward {jump_duration} seconds")
                last_press_time = current_time
                time.sleep(0.3)  # Hindari deteksi ganda

            # Lompat 5 atau 10 detik ke belakang
            if keyboard.is_pressed("left"):
                if last_press_time and current_time - last_press_time < 1:  # Tekan dalam waktu <1 detik
                    jump_duration = 10
                else:
                    jump_duration = 5

                current_time_ms = player.get_time()
                player.set_time(max(0, current_time_ms - jump_duration * 1000))  # Kurangi dalam ms
                print(f"Skipped backward {jump_duration} seconds")
                last_press_time = current_time
                time.sleep(0.3)  # Hindari deteksi ganda
    except KeyboardInterrupt:
        print("\nKeyboard monitoring stopped.")

def play_video_with_subtitles(video_path, subtitle_path):
    """
    Memutar video dengan kontrol keyboard dan membaca subtitle di latar belakang.
    """
    subtitles = parse_srt_file(subtitle_path)
    if not subtitles:
        return

    # Instance VLC
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(video_path)
    player.set_media(media)

    # Mainkan video
    player.play()
    time.sleep(1)
    print("Video started. Press SPACE to play/pause, ARROW RIGHT to skip forward, ARROW LEFT to skip backward. Subtitles will be copied to clipboard...")

    # Jalankan thread untuk memonitor subtitle
    subtitle_thread = threading.Thread(target=monitor_subtitles, args=(subtitles, player))
    subtitle_thread.daemon = True
    subtitle_thread.start()

    # Jalankan thread untuk memonitor keyboard
    keyboard_thread = threading.Thread(target=monitor_keyboard, args=(player,))
    keyboard_thread.daemon = True
    keyboard_thread.start()

    try:
        while True:
            time.sleep(1)  # Program utama tetap berjalan
    except KeyboardInterrupt:
        print("\nExiting program...")
        player.stop()

# Pilih file video dan subtitle
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

# Mainkan video dengan subtitle
play_video_with_subtitles(video_file, subtitle_file)