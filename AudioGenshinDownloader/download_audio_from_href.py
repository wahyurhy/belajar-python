import os
import requests
from bs4 import BeautifulSoup

# Baca file HTML
file_path = r"E:\日本語\Genshin\Bennett\Bennett_Voice-Overs_Japanese _ Genshin Impact Wiki _ Fandom.html"

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parsing HTML menggunakan BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Filter link yang sesuai dengan pola static.wikia.nocookie.net, berakhiran .ogg, dan memiliki cb=
href_links = [
    link['href'] for link in soup.find_all('a', href=True)
    if link['href'].startswith('https://static.wikia.nocookie.net')
    and '.ogg' in link['href']
    and 'cb=' in link['href']
]

# Periksa apakah href_links tidak kosong
if not href_links:
    print("Tidak ada URL href yang ditemukan sesuai kriteria.")
else:
    print(f"Ditemukan {len(href_links)} file audio untuk didownload.")

# Membuat folder untuk menyimpan file yang didownload
output_folder = 'downloaded_audio'
os.makedirs(output_folder, exist_ok=True)

# Fungsi untuk membersihkan nama file
def sanitize_filename(filename):
    invalid_chars = '<>:\"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

# Mendownload setiap file audio dari href
for href_link in href_links:
    print(f"Mendownload: {href_link}")
    try:
        # Mengambil nama file dari URL sebelum "/revision"
        file_name = href_link.split('/')[-3]  # Ambil nama file sebelum "/revision"
        file_name = sanitize_filename(file_name)  # Bersihkan nama file
        file_path = os.path.join(output_folder, file_name)

        # Mendownload file audio
        response = requests.get(href_link, stream=True)
        response.raise_for_status()  # Memastikan tidak ada error

        # Menulis konten file audio
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Berhasil mendownload: {file_name}")

    except Exception as e:
        print(f"Gagal mendownload {href_link}: {e}")

print(f"Semua file audio telah disimpan di folder: {output_folder}")