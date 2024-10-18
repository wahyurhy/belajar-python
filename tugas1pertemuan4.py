import locale

locale.setlocale(locale.LC_ALL, 'id-ID')

borderLine = '=================================================='

print(borderLine)
print("{:<16}{:^10}{:>10}".format('', 'PT. DINGIN DAMAI', ''))
print("{:<10}{:^10}{:>10}".format('', 'PROGRAM HITUNG GAJI KARYAWAN', ''))
print(borderLine)
print(borderLine)

gajiPokok = 300000
uangLemburPerJam = 3500

namaKaryawan = str(input('Nama Karyawan: '))
golonganJabatan = str(input('Golongan (1/2/3): '))
pendidikan = str(input('Pendidikan (SMA/D1/D3/S1): ').upper())
jumlahJamKerja = int(input('Jumlah Jam Kerja: '))

if golonganJabatan == '1':
    tunjanganJabatan = 0.05 * gajiPokok
elif golonganJabatan == '2':
    tunjanganJabatan = 0.1 * gajiPokok
elif golonganJabatan == '3':
    tunjanganJabatan = 0.15 * gajiPokok
else:
    tunjanganJabatan = 0   

if pendidikan == 'SMA':
    tunjanganPendidikan = 0.025 * gajiPokok
elif pendidikan == 'D1':
    tunjanganPendidikan = 0.05 * gajiPokok
elif pendidikan == 'D3':
    tunjanganPendidikan = 0.2 * gajiPokok
elif pendidikan == 'S1':
    tunjanganPendidikan = 0.3 * gajiPokok
else:
    tunjanganPendidikan = 0

if jumlahJamKerja > 8:
    jamLembur = jumlahJamKerja - 8
    honorLembur = jamLembur * uangLemburPerJam

tunjangan = tunjanganJabatan + tunjanganPendidikan
totalGaji = gajiPokok + tunjangan + honorLembur

print(borderLine)
print(borderLine)
print(f"Karyawan yang bernama {namaKaryawan}")
print("Honor yang diterima:")
# print(f"Tunjangan Jabatan\t: {str(tunjanganJabatan).replace('.0', '')}")
print(f"Tunjangan Jabatan\t: {locale.currency(tunjanganJabatan, grouping=True).replace(',00', '')}")
# print(f"Tunjangan Pendidikan\t: {str(tunjanganPendidikan).replace('.0', '')}")
print(f"Tunjangan Pendidikan\t: {locale.currency(tunjanganPendidikan, grouping=True).replace(',00', '')}")
# print(f"Honor Lembur\t\t: {honorLembur}")
print(f"Honor Lembur\t\t: {locale.currency(honorLembur, grouping=True).replace(',00', '')}")
# print(f"Total Gaji\t\t: {str(totalGaji).replace('.0', '')}")
print(f"Total Gaji\t\t: {locale.currency(totalGaji, grouping=True).replace(',00', '')}")

print(borderLine)