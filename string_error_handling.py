def handling(info, *args):
    isTrue = True
    while isTrue:
        try:
            result = str(input(info).capitalize())
            if result in args:
                isTrue = False
            else:
                print(f'Hanya Boleh diinputkan dengan {info}')
        except:
            print(f'Hanya Boleh diinputkan dengan {info}')
            isTrue = True
    return result