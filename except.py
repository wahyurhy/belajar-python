try:
    a = int(input("Masukan angka pertama: "))
    b = int(input("Masukan angka ke dua: "))
    hasil = a / b
    print(f'Hasilnya dari {a} / {b} adalah {hasil}')
    if b == 0:
        raise ZeroDivisionError('Tidak boleh pembagian dengan NOL')
except ZeroDivisionError as e:
    print(e)