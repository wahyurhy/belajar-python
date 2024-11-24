import os
import shutil
import sys
import io

# Atur stdout ke UTF-8 untuk mendukung karakter Unicode di terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Direktori utama
base_path = r"E:\日本語\Genshin"

# Folder pertama yang diproses
current_folder = "Chasca"

# Dapatkan daftar semua folder dalam base_path
all_folders = sorted([f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))])

# Periksa apakah current_folder ada di all_folders
if current_folder in all_folders:
    # Mulai dari indeks folder saat ini
    start_index = all_folders.index(current_folder)

    # Proses semua folder dari current_folder hingga folder terakhir
    for folder in all_folders[start_index:]:
        print(f"Memproses folder: {folder}")
        folder_path = os.path.join(base_path, folder)

        # Folder untuk menyimpan file kecil dari folder saat ini
        small_files_folder = os.path.join(folder_path, "small_files")
        os.makedirs(small_files_folder, exist_ok=True)

        # Ukuran batas (70 KB dalam byte)
        size_limit = 70 * 1024  # 70 KB

        # Memindahkan file yang ukurannya di bawah 70 KB
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            # Periksa apakah itu file (bukan folder)
            if os.path.isfile(file_path):
                # Periksa ukuran file
                file_size = os.path.getsize(file_path)
                if file_size < size_limit:
                    # Pindahkan file ke folder small_files
                    shutil.move(file_path, os.path.join(small_files_folder, file_name))
                    print(f"Memindahkan file: {file_name} ({file_size} bytes) ke folder 'small_files'.")

        print(f"Semua file kecil dari folder {folder} telah dipindahkan ke folder 'small_files'.")
else:
    print(f"Folder {current_folder} tidak ditemukan di daftar folder.")

print("Proses selesai untuk semua folder.")