borderLine = "=============================="

nama = "Wahyu Rahayu"
panggilanRumah = "Abang"
panggilanSekolah = "Cuy"
panggilanKantor = "Pak"
panggilanGaul = "Bro"
kelas = "12.A"
jurusan = "Informatika"

lokasi = "Cafe"

if lokasi == "Sekolah":
    print(borderLine)
    print("Nama : " + nama)
    print("Panggilan : " + panggilanSekolah)
    print("Kelas : " + kelas)
    print("Jurusan " + jurusan)
    print(borderLine)
elif lokasi == "Kantor":
    print(borderLine)
    print("Nama : " + nama)
    print("Panggilan : " + panggilanKantor)
    print("Kelas : " + kelas)
    print("Jurusan " + jurusan)
    print(borderLine)
elif lokasi == "Rumah":
    print(borderLine)
    print("Nama : " + nama)
    print("Panggilan : " + panggilanRumah)
    print("Kelas : " + kelas)
    print("Jurusan " + jurusan)
    print(borderLine)
else:
    print(borderLine)
    print("Nama : " + nama)
    print("Panggilan : " + panggilanGaul)
    print("Kelas : " + kelas)
    print("Jurusan " + jurusan)
    print(borderLine)