def hitung_gaji(gaji_pokok, jam_kerja):
    tunjangan = 0.2 * gaji_pokok
    if jam_kerja > 200:
        lembur = (jam_kerja - 200) * 20000
    else:
        lembur = 0
    gaji_kotor = gaji_pokok + tunjangan + lembur
    pajak = 0.1 * gaji_kotor
    gaji_bersih = gaji_kotor - pajak
    return gaji_bersih

# Contoh penggunaan
gaji_pokok = int(input("Masukkan gaji pokok: "))
jam_kerja = int(input("Masukkan total jam kerja: "))
gaji = hitung_gaji(gaji_pokok, jam_kerja)
print(f"Gaji bersih pegawai adalah: Rp {gaji}")