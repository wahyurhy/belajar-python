mapel = ['Matematika', 'Fisika', 'Kimia']

# print(mapel[0])
# print(mapel[1])
# print(mapel[2])

for i in range(len(mapel)):
    if mapel[i] == 'Fisika':
        print(f'waduh ada {mapel[i]}!!!')
        break
    else:
        print(f'Saya suka {mapel[i]}')

for mataPelajaran in mapel:
    if mataPelajaran == 'Fisika':
        print(f'waduh ada {mataPelajaran}!!!')
        break
    else:
        print(f'Saya belajar {mataPelajaran}')