import os
import re

def extract_japanese_text_from_srt(input_srt_path):
    # Pola regex untuk mendeteksi karakter Jepang
    japanese_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF\uFF66-\uFF9F\u3000-\u303F]+')

    # Tentukan path output dengan mengganti ekstensi file menjadi .txt
    output_txt_path = os.path.splitext(input_srt_path)[0] + "_japanese.txt"

    # Membaca file srt dan mengekstrak teks Jepang
    with open(input_srt_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    japanese_lines = []
    for line in lines:
        line = line.strip()
        if japanese_pattern.search(line):  # Jika baris mengandung karakter Jepang
            japanese_lines.append(line)

    # Menulis hasil ke file txt
    with open(output_txt_path, 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(japanese_lines))

    print(f"Proses selesai. File disimpan di: {output_txt_path}")

# Ganti path file SRT di sini
input_srt_path = r"E:\Anime\kitsunekko-mirror\subtitles\K-ON!\[Tsundere] K-On! - 01 [BDRip h264 1920x1080 FLAC][9CCE52EA].ja.srt"
extract_japanese_text_from_srt(input_srt_path)