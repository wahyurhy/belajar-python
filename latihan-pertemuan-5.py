import format_rupiah
import integer_error_handling
import string_error_handling

borderLine = "-----------------------------------------------------------------------------"
titleApp = "Grobak Fried Chicken"

produk = {
    'D': 2500,
    'P': 1500,
    'S': 1000,
    'K': 500
}

namaProduk = {
    'D': 'Dada',
    'P': 'Paha',
    'S': 'Sayap',
    'K': 'Kepala'
}

jenisPotongYangDibeli = []
banyakYangDibeli = []
jumlahHarga = []

banyakJenis = integer_error_handling.handling('Banyak Jenis:')

for i in range(banyakJenis):
    print('{:<25} {:^10} {:>10}'.format('', titleApp.upper(), ''))
    print(borderLine)
    print('{:<10} {:^10} {:>10}'.format('Kode', 'Jenis Potongan', 'Harga'))
    print('{:<10} {:^14} {:>10}'.format(' D', str(namaProduk['D']), str(produk['D'])))
    print('{:<10} {:^14} {:>10}'.format(' P', str(namaProduk['P']), str(produk['P'])))
    print('{:<10} {:^14} {:>10}'.format(' S', str(namaProduk['S']), str(produk['S'])))
    print('{:<10} {:^14} {:>10}'.format(' K', str(namaProduk['K']), str(produk['K'])))
    print(borderLine + '\n\n')
    print(f'Banyak Jenis: {banyakJenis}')
    print(f'Jenis Ke-{i + 1}')
    potonganYangDipilih = string_error_handling.handling('Kode Potongan [D/P/S/K]: ', 'D', 'P', 'S', 'K')
    jumlahYangDibeli = integer_error_handling.handling('Banyak Potong: ')

    jenisPotongYangDibeli.append(potonganYangDipilih)
    banyakYangDibeli.append(jumlahYangDibeli)
    jumlahHarga.append(jumlahYangDibeli * produk[potonganYangDipilih])

print('{:<25} {:^10} {:>10}'.format('', titleApp.upper(), ''))
print(borderLine)
print('No. {:^2} Jenis Potong  {:^5}  Harga Satuan {:^5} Banyak Beli {:^5} Jumlah Harga'.format('','','',''))
print(borderLine)
for i in range(len(banyakYangDibeli)):
    print('{} {:^20} {:^20} {:^17} {:<5} {}'.format(i + 1, namaProduk[jenisPotongYangDibeli[i]], format_rupiah.format(produk[jenisPotongYangDibeli[i]]), banyakYangDibeli[i], '', format_rupiah.format(jumlahHarga[i])))

print(borderLine)

print('{:<55}Jumlah Bayar {}'.format('', format_rupiah.format(sum(jumlahHarga))))

pajak = (10/100) * sum(jumlahHarga)
totalBayar = sum(jumlahHarga) + pajak
print('{:<55}Pajak 10%    {}'.format('', format_rupiah.format(pajak)))
print('{:<55}Total Bayar  {}'.format('', format_rupiah.format(totalBayar)))