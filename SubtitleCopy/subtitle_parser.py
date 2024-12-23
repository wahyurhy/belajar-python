import pysrt
import time
import pyperclip
import vlc
from tkinter import Tk, filedialog
from datetime import timedelta
import threading
import sys
import keyboard  # Untuk menangkap input keyboard
from pathlib import Path
import requests
from telegram_config import my_bot_token, my_chat_id
import subprocess
import logging

# Pastikan encoding terminal UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Antrian untuk menyimpan pesan
message_queue = []
queue_lock = threading.Lock()

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

# Menambahkan Pesan ke Antrian
def add_message_to_queue(message):
    with queue_lock:
        message_queue.append(message)
    logging.info(f"Message added to queue: {message}")

# Mengirim Batch Pesan ke Telegram
def send_telegram_message_batch(bot_token, chat_id):
    global message_queue
    while True:
        time.sleep(15)  # Tunggu 15 detik sebelum memproses pesan berikutnya

        # Ambil pesan dari antrian
        with queue_lock:
            if not message_queue:
                continue
            combined_message = "\n\n".join(message_queue)  # Gabungkan pesan dengan newline
            message_queue.clear()

        # Kirim pesan gabungan ke Telegram
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': combined_message
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                logging.info(f"Combined message sent:\n{combined_message}")
            else:
                logging.error(f"Error sending combined message: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending combined message: {e}")

# Monitoring Subtitle dan Mengirim ke Antrian
def monitor_subtitles_with_queue(subtitles, extracted_subtitles, player, bot_token, chat_id):
    last_text = None
    last_extracted_text = None
    threading.Thread(target=send_telegram_message_batch, args=(bot_token, chat_id), daemon=True).start()

    try:
        while True:
            current_time = timedelta(seconds=player.get_time() / 1000)

            current_text = get_current_subtitle(subtitles, current_time)
            if current_text and current_text != last_text:
                pyperclip.copy(current_text)
                last_text = current_text
                add_message_to_queue(current_text)

            extracted_text = get_current_subtitle(extracted_subtitles, current_time)
            if extracted_text and extracted_text != last_extracted_text:
                last_extracted_text = extracted_text
                add_message_to_queue(extracted_text)

            time.sleep(0.1)
    except KeyboardInterrupt:
        logging.info("Stopped monitoring subtitles.")

def monitor_keyboard(player, subtitle, is_subtitle_enabled, is_using_external_subtitle, subtitle_path):
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

            # Enable/Disable subtitle dengan tombol C
            if keyboard.is_pressed("c"):
                if is_subtitle_enabled[0]:
                    player.video_set_spu(-1)  # Disable subtitle
                    print("Subtitles Disabled")
                else:
                    player.video_set_spu(0)  # Enable subtitle
                    print("Subtitles Enabled")
                    current_time_ms = player.get_time()
                    player.set_time(current_time_ms)
                is_subtitle_enabled[0] = not is_subtitle_enabled[0]
                time.sleep(0.3)  # Hindari deteksi ganda

            # Toggle external/internal subtitle dengan tombol X
            if keyboard.is_pressed("x"):
                if is_using_external_subtitle[0]:
                    # Kembali ke subtitle default
                    player.video_set_spu(0)  # Set ke subtitle internal VLC (index 0 default)
                    print("Switched to Default Subtitle")
                else:
                    # Gunakan subtitle eksternal menggunakan URI
                    uri = Path(subtitle_path).as_uri()
                    result = player.add_slave(vlc.MediaSlaveType.subtitle, uri, True)
                    if result == 0:
                        print(f"Switched to External Subtitle: {subtitle_path}")
                    else:
                        print("Failed to switch to External Subtitle.")
                is_using_external_subtitle[0] = not is_using_external_subtitle[0]
                time.sleep(0.3)  # Hindari deteksi ganda
    except KeyboardInterrupt:
        print("\nKeyboard monitoring stopped.")

def extract_subtitle(video_path):
    """
    Ekstrak subtitle internal dari video menggunakan FFmpeg dan konversi ke format SRT.
    """
    try:
        # Buat nama file subtitle berdasarkan nama file video
        video_file = Path(video_path)
        output_subtitle_path = video_file.with_stem(f"extracted_{video_file.stem}").with_suffix('.srt')  # Mengganti ekstensi menjadi .srt

        # Ganti dengan jalur lengkap ke ffmpeg.exe
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

        subprocess.run(
            [ffmpeg_path, "-i", video_path, "-map", "0:s:0", "-c:s", "srt", str(output_subtitle_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Subtitle extracted to {output_subtitle_path}")
        return output_subtitle_path
    except FileNotFoundError:
        print("Error: ffmpeg executable not found. Check your installation and ffmpeg_path.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract subtitle: {e.stderr.decode('utf-8')}")
        return None
    
def validate_subtitle_file(file_path):
    """
    Memeriksa apakah file subtitle valid (tidak kosong).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if content:
                return True
            else:
                print("Subtitle file is empty.")
                return False
    except Exception as e:
        print(f"Failed to validate subtitle file: {e}")
        return False

# Memutar Video dengan Subtitle
def play_video_with_subtitles(video_path, subtitle_path=None):
    """
    Memutar video dengan kontrol keyboard dan membaca subtitle di latar belakang.
    """
    extracted_subtitle_path = extract_subtitle(video_path)
    if not extracted_subtitle_path or not validate_subtitle_file(extracted_subtitle_path):
        logging.error("Failed to validate extracted subtitle.")
        return

    extracted_subtitles = parse_srt_file(extracted_subtitle_path)
    if not extracted_subtitles:
        logging.error("Failed to parse extracted subtitles.")
        return

    subtitles = parse_srt_file(subtitle_path)
    if not subtitles:
        logging.error("Failed to parse selected subtitles.")
        return

    bot_token = my_bot_token
    chat_id = my_chat_id

    # Instance VLC
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(video_path)
    player.set_media(media)

    # Mainkan video
    player.play()
    time.sleep(1)
    logging.info("Video started.")

    threading.Thread(target=monitor_subtitles_with_queue, args=(subtitles, extracted_subtitles, player, bot_token, chat_id), daemon=True).start()

    is_subtitle_enabled = [True]
    is_using_external_subtitle = [False]

    threading.Thread(target=monitor_keyboard, args=(player, subtitles, is_subtitle_enabled, is_using_external_subtitle, subtitle_path), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Exiting program...")
        player.stop()

def send_telegram_message(bot_token, chat_id, message):
    """
    Fungsi untuk mengirim pesan ke grup Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Pesan terkirim ke Telegram: {message}")
        else:
            print(f"Error mengirim pesan: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengirim pesan: {e}")

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