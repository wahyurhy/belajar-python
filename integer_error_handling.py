def handling(info):
    isTrue = True
    while isTrue:
        try:
            result = int(input(info))
            isTrue = False
        except:
            print('Hanya Boleh diinputkan dengan angka!')
            isTrue = True
    return result