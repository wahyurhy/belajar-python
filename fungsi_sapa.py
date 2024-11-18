def sapa(nama):
    """Fungsi ini untuk menyapa seseorang sesuai nama yang dimasukkan sebagai parameter"""
    print(f'Halo kenalin saya {nama}')

def sapa_dengan_return(nama):
    return f"Halo kenalin saya {nama} dari return"

# sapaan = sapa('revan')
sapaan = sapa_dengan_return('revan')
print(sapaan)
# print(sapa.__doc__)