import subprocess
from tkinter import Tk, filedialog

def select_file():
    """
    Menampilkan file dialog untuk memilih file video.
    """
    root = Tk()
    root.withdraw()  # Menyembunyikan jendela utama Tkinter
    file_path = filedialog.askopenfilename(
        title="Pilih file video",
        filetypes=[("Video files", "*.mkv *.mp4 *.avi *.flv *.mov"), ("All files", "*.*")]
    )
    return file_path

def extract_subtitle(video_file, output_subtitle="output_subtitle.srt"):
    """
    Mengekstrak subtitle internal dari file video menggunakan ffmpeg.
    """
    try:
        # Gunakan jalur penuh ke ffmpeg jika tidak ada di PATH
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Ganti dengan jalur lengkap ke ffmpeg.exe jika diperlukan

        # Perintah ffmpeg untuk mengekstrak subtitle internal
        command = [
            ffmpeg_path,  # Gunakan jalur penuh
            "-i", video_file,
            "-map", "0:s:0",  # Subtitle stream pertama
            output_subtitle,
            "-y"
        ]

        # Jalankan perintah ffmpeg
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print(f"Subtitle berhasil diekstrak ke file: {output_subtitle}")
        else:
            print(f"Error saat mengekstrak subtitle:\n{result.stderr}")
    except FileNotFoundError:
        print("Error: ffmpeg tidak ditemukan. Pastikan ffmpeg sudah diinstal dan ditambahkan ke PATH.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    print("Pilih file video untuk ekstrak subtitle:")
    video_file = select_file()

    if not video_file:
        print("Tidak ada file yang dipilih. Program dihentikan.")
    else:
        print(f"File video yang dipilih: {video_file}")
        extract_subtitle(video_file)