# pip install beautifulsoup4
# pip install requests beautifulsoup4

import webbrowser
from bs4 import BeautifulSoup

# Baca file HTML
file_path = r'E:\日本語\Yelan\Yelan_Voice-Overs_Japanese _ Genshin Impact Wiki _ Fandom.html'

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
    print(f"Ditemukan {len(href_links)} href yang akan dibuka di browser.")

# Membuka setiap link di tab baru browser default
for href_link in href_links:
    print(f"Membuka: {href_link}")
    webbrowser.open_new_tab(href_link)

print("Semua URL telah dibuka di browser.")