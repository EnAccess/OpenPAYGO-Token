import codecs, os

if __name__ == '__main__':

    this_key = os.urandom(16)

    print('Hex Key: ' + codecs.encode(this_key, 'hex').decode('utf-8'))
    print('Python Key: ' + str(this_key))

    string = '{'
    for o in this_key:
        string += hex(o) + ', '
    string = string[:len(string) - 2]
    string += '}'
    print('C Key: ' + string)
