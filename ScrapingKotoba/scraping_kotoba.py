import requests
from bs4 import BeautifulSoup
import json
import sys
import io

# Pastikan terminal mendukung UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# URL halaman yang akan di-scrape
url = "https://japanesetest4you.com/jlpt-n5-vocabulary-list/"

def scrape_and_convert_to_json(url):
    try:
        # Mengirim permintaan GET ke URL
        response = requests.get(url)
        response.raise_for_status()  # Memeriksa apakah permintaan berhasil

        # Parsing HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Menemukan semua tag <p>
        p_tags = soup.find_all("p")

        # Menyimpan data dalam format JSON
        vocabulary_list = []
        for p in p_tags:
            text = p.get_text().strip()  # Mengambil teks dari tag <p>
            if "):" in text:  # Memastikan format yang valid
                try:
                    # Memisahkan teks menjadi komponen
                    kotoba, rest = text.split(" (", 1)
                    yomikata, imi = rest.split("): ", 1)
                    vocabulary_list.append({
                        "kotoba": kotoba.strip(),
                        "yomikata": yomikata.strip(),
                        "imi": imi.strip()
                    })
                except ValueError:
                    # Lewati jika format tidak sesuai
                    continue

        # Menyimpan hasil dalam file JSON
        output_file = "jlpt_n5_vocabulary.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(vocabulary_list, f, ensure_ascii=False, indent=4)

        print(f"Scraping selesai! Data disimpan dalam file: {output_file}")
        return vocabulary_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

# Jalankan fungsi scraping
vocabulary_data = scrape_and_convert_to_json(url)

# Tampilkan beberapa hasil
print(json.dumps(vocabulary_data[:5], ensure_ascii=False, indent=4))