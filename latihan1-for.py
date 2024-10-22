
ulangi = 3

for i in range(ulangi):
    print(f'Data ke - {i + 1}')
    print('==========================')
    nim = str(input('Masukkan NIM : '))
    uts = float(input('Masukan Nilai UTS: '))
    uas = float(input('Masukan Nilai UAS: '))

    # print(f'Mahasiswa dengan NIM ({nim}) memiliki UTS sebesar {uts} dan UAS sebesar {uas}')
    print('Mahasiswa dengan NIM (%s) memiliki UTS sebesar {%.1f} dan UAS sebesar {%.1f}' % (nim, uts, uas))