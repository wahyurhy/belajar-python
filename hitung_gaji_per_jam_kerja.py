import format_rupiah

def hitungGajiPerJamKerja(gajiPokok, jamKerja):
    tunjangan = 0.2 * gajiPokok
    lembur = jamKerja - 200

    if jamKerja > 200:
        komisi = lembur * 20000
    else:
        komisi = 0

    gajiKotor = gajiPokok + tunjangan + komisi
    pajak = gajiKotor * 0.1
    totalGaji =  gajiKotor - pajak

    print(f'Gaji pokok = {format_rupiah.format(gajiPokok)}')
    print(f'Jam Kerja = {jamKerja} Jam')
    print(f'Tunjangan = {format_rupiah.format(tunjangan)}')
    print(f'Lembur = {lembur} Jam')
    print(f'Komisi = {format_rupiah.format(komisi)}')
    print(f'Pajak = {format_rupiah.format(pajak)}')
    print(f'Total Gaji = {format_rupiah.format(totalGaji)}')
    
    return totalGaji

