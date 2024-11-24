import os
import shutil
import sys
import io

# Atur stdout ke UTF-8 untuk mendukung karakter Unicode di terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Path direktori
path = r"E:\日本語\Genshin\Migrasi"

# Folder untuk menyimpan file yang ukurannya di bawah 70 KB
small_files_folder = os.path.join(path, "small_files")
os.makedirs(small_files_folder, exist_ok=True)

# Ukuran batas (70 KB dalam byte)
size_limit = 70 * 1024  # 70 KB

# Memindahkan file yang ukurannya di bawah 70 KB
for file_name in os.listdir(path):
    file_path = os.path.join(path, file_name)
    
    # Periksa apakah itu file (bukan folder)
    if os.path.isfile(file_path):
        # Periksa ukuran file
        file_size = os.path.getsize(file_path)
        if file_size < size_limit:
            # Pindahkan file ke folder small_files
            shutil.move(file_path, os.path.join(small_files_folder, file_name))
            print(f"Memindahkan file: {file_name} ({file_size} bytes) ke folder 'small_files'.")

print(f"Semua file di bawah 70 KB telah dipindahkan ke folder: {small_files_folder}")