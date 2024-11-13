print('================= Segitiga Sama Kaki =================')

bil = int(input("Masukkan Jumlah Perulangan: "))
kar = input("Masukkan Karakter: ")

s = bil  - 1 # for spaces

for i in range(0, bil):
    for j in range(0, s):
        print('s', end='')
    s -= 1
    for j in range(0, i + 1):
        print(kar, end='j2')

    print('')

