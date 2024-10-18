borderline = "============================================================="
print(borderline)
print("{:<20}{:^10}{:>20}".format('',"Penjualan Tiket Bus",''))
print("{:<20}{:^20}{:>20}".format('',"XYZ",''))
print(borderline)
print("Jurusan Surabaya (SBY)\t| Rp 300000")
print("Jurusan Bali (BL)\t| Rp 350000")
print("Jurusan Lampung (LMP)\t| Rp 500000")
pembeli = input("Masukkan Nama Pembeli : ")
noHP = input("Masukka Nomor HP : ")
jurusan = input("Maukkan Jurusan (SBY/BL/LMP) :")
jumlahBeli = int(input("Masukkan Jumlah Beli : "))


if jurusan =="SBY":
    namaJurusan = "Surabaya"
    harga = 300000
elif jurusan =="BL":
    namaJurusan = "Bali"
    harga = 350000
else :
    namaJurusan = "LMP"
    harga = 500000

if jumlahBeli>=3 :
    potongan = (jumlahBeli*harga)*0.1
else : 
    potongan = 0

total = (jumlahBeli*harga)-potongan

print(borderline)
print(f"Nama Pembeli : {pembeli}")
print(f"No Handphone : {noHP}")
print(f"Nama Kota Tujuan : {jurusan}")
print(f"Harga : {harga}")
print(f"Jumlah Beli : {jumlahBeli}")
print(borderline)
print(f"Potongan Yang Didapat : {str(potongan).replace(".0", "")}")
print(f"Total Bayar : {str(total).replace(".0", "")}")
uangBayar = int(input("Masukkan Uang Bayar : "))
uangKembali = uangBayar-total
print(f"Uang Kembali : {str(uangKembali).replace(".0", "")}")

print("Terimakasih dan selamat jalan~")