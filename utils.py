windows_lsep = "\r\n"


def normalize(string):
    string = string.replace(windows_lsep, '\n')
    return string
