import locale
locale.setlocale(locale.LC_ALL, 'id-ID')

print('{:<20}{:^10}{:>20}'.format('','Toko Mainan Anak',''))
print('{:<15}{:^10}{:>15}'.format('','***************************',''))

namaPembeli = str(input('Masukan nama pembeli: '))
kodeMainan = str(input('Masukan kode mainan: '))
harga = int(input('Masukan harga: '))
jumlahBeli = int(input('Masukan jumlah beli: '))

total = jumlahBeli * harga

print('===========================================')

print(f'Nama Pembeli\t= {namaPembeli}')
print(f'Kode Mainan\t= {kodeMainan}')
print(f'Harga\t\t= {locale.currency(harga, grouping=True)}')
print(f'Jumlah Beli\t= {jumlahBeli}')
print(f'Total\t\t= {locale.currency(total, grouping=True)}')