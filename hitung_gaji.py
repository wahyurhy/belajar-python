import locale

locale.setlocale(locale.LC_ALL, 'id-ID')

def hitung(banyak_produk, harga_satuan):
    gaji_pokok = 5000000
    omset_penjualan = banyak_produk * harga_satuan
    
    if banyak_produk > 100:
        komisi = 0.2 * omset_penjualan
    else:
        komisi = 0.1 * omset_penjualan
    
    total_gaji = gaji_pokok + komisi
    
    print(f'Bonus yang didapatkan = {locale.currency(komisi, grouping=True).replace(',00', '')}')
    print(f'Banyak produk yang terjual = {banyak_produk}')
    print(f'Total Gaji (Bersih) = {locale.currency(total_gaji, grouping=True).replace(',00', '')}')

    return total_gaji