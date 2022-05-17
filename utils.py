windows_lsep = "\r\n"


def normalize(string):
    if string.startswith('\ufeff'):
        string = string[1:]
    string = string.replace(windows_lsep, '\n')
    return string
