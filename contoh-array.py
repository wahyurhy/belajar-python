

panjang1 = 10
panjang2 = 20
panjang3 = 30
panjang4 = 40

a = panjang1 + panjang2 + panjang3 + panjang4 + \
    panjang1 + panjang2 + panjang3 + panjang4 + \
    panjang1 + panjang2 + panjang3 + panjang4 + \
    panjang1 + panjang2 + panjang3 + panjang4

print(a)

print("=====================================")

absensiKelasE = ['Ahmad', 'Bagus', 
            'Candra', 'Dadang', 
            'Eka', 'Ferry', 'Galuh',
            'Halim', 'Ijat', 'Jarot',
            'Kamal', 'Linda']

print(absensiKelasE)

for index, absen in enumerate(absensiKelasE, 1):
    print("Absen ke " + str(index) + " adalah absen " + absen)


# sloganIndonesiaEmas = """Maju Indonesia
# Hapus Koruptor
# Berantas Nepotisme"""

sloganIndonesiaEmas = "Maju Indonesia\n" + \
"Hapus Koruptor\n" + \
"Berantas Nepotisme\n"

print(sloganIndonesiaEmas)