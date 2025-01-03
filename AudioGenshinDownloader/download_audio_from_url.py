# pip install aiohttp beautifulsoup4

import os
import asyncio
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

# Tautan URL ke website
url = "https://honkai-star-rail.fandom.com/wiki/Xueyi/Voice-Overs/Japanese"

# Membuat folder untuk menyimpan file yang didownload
output_folder = 'downloaded_audio'
os.makedirs(output_folder, exist_ok=True)

# Fungsi untuk membersihkan nama file
def sanitize_filename(filename):
    invalid_chars = '<>:\"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

# Fungsi asynchronous untuk mendownload file
async def download_file(session: ClientSession, href_link: str):
    try:
        # Mengambil nama file dari URL sebelum "/revision"
        file_name = href_link.split('/')[-3]  # Ambil nama file sebelum "/revision"
        file_name = sanitize_filename(file_name)  # Bersihkan nama file
        file_path = os.path.join(output_folder, file_name)

        print(f"Mendownload: {href_link}")
        async with session.get(href_link) as response:
            response.raise_for_status()  # Memastikan tidak ada error
            with open(file_path, 'wb') as file:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    file.write(chunk)
        print(f"Berhasil mendownload: {file_name}")
    except Exception as e:
        print(f"Gagal mendownload {href_link}: {e}")

# Fungsi utama untuk mengambil konten halaman dan mendownload file audio
async def main():
    async with aiohttp.ClientSession() as session:
        try:
            # Ambil konten dari URL
            async with session.get(url) as response:
                response.raise_for_status()  # Memastikan tidak ada error HTTP
                html_content = await response.text()

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
                return

            print(f"Ditemukan {len(href_links)} file audio untuk didownload.")

            # Download semua file audio secara asynchronous
            tasks = [download_file(session, href_link) for href_link in href_links]
            await asyncio.gather(*tasks)

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

# Menjalankan event loop untuk memulai download
asyncio.run(main())

print(f"Semua file audio telah disimpan di folder: {output_folder}")