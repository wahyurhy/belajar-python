borderLine = "-----------------------------------------------------------------"
titleApp = "Grobak Fried Chicken"

produk = {
    'D': 2500,
    'P': 1500,
    'S': 1000
}

namaProduk = {
    'D': 'Dada',
    'P': 'Paha',
    'S': 'Sayap'
}

jenisPotongYangDibeli = []
banyakYangDibeli = []
jumlahHarga = []

banyakJenis = int(input('Banyak Jenis:'))

for i in range(banyakJenis):
    print('{:<20} {:^10} {:>10}'.format('', titleApp.upper(), ''))
    print(borderLine)
    print('{:<10} {:^10} {:>10}'.format('Kode', 'Jenis Potongan', 'Harga'))
    print('{:<10} {:^14} {:>10}'.format(' D', 'Dada', str(produk['D'])))
    print('{:<10} {:^14} {:>10}'.format(' P', 'Paha', str(produk['P'])))
    print('{:<10} {:^14} {:>10}'.format(' S', 'Sayap', str(produk['S'])))
    print(borderLine + '\n\n')
    print(f'Banyak Jenis: {banyakJenis}')
    print(f'Jenis Ke-{i + 1}')
    potonganYangDipilih = str(input('Kode Potongan [D/P/S]: '))
    jumlahYangDibeli = int(input('Banyak Potong: '))

    jenisPotongYangDibeli.append(potonganYangDipilih)
    banyakYangDibeli.append(jumlahYangDibeli)
    jumlahHarga.append(jumlahYangDibeli * produk[potonganYangDipilih])

print('{:<20} {:^10} {:>10}'.format('', titleApp.upper(), ''))
print(borderLine)
print(f'No.     Jenis Potong    Harga Satuan   Banyak Beli   Jumlah Harga')
print(borderLine)
for i in range(len(banyakYangDibeli)):
    print(f'{i + 1}          {namaProduk[jenisPotongYangDibeli[i]]}              {produk[jenisPotongYangDibeli[i]]}          {banyakYangDibeli[i]}           Rp{jumlahHarga[i]}')

print(borderLine)

print(f'                                        Jumlah Bayar Rp{sum(jumlahHarga)}')

pajak = (10/100) * sum(jumlahHarga)
totalBayar = sum(jumlahHarga) - pajak
print(f'                                        Pajak 10%    Rp{pajak}')
print(f'                                        Total Bayar  Rp{totalBayar}')