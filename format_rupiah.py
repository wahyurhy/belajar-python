import locale

locale.setlocale(locale.LC_ALL, 'id-ID')

def format(uang):
    hasilFormat = locale.currency(uang, grouping=True).replace(',00', '')
    return hasilFormat