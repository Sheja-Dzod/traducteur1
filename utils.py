windows_lsep = ' '


def normalize(string):
    string = string.replace(windows_lsep, '\n')
    return string
