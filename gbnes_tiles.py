# prodecimientos para trabajar con graficos de nes/gameboy
# TODAVIA ESTA INCOMPLETO

def get_bit(num, i):
    '''
    Retorna el i-esimo bit de la representacion
    en binario de num
    '''
    return (num & (1 << i)) >> i

def set_bit(num, i, bit):
    '''
    Retorna el entero que resulta de cambiar el 
    i-esimo bit de la representacion binaria de num
    al valor <bit> que se tiene de parametro
    '''
    if bit == 1:
        # set bit
        return num |  (1 << i)
    else:
        # clear bit
        return num & ~(1 << i)


    return  num | (~(bit << i))

def encode_row(row):
    '''
    Toma un renglon de un Tile de gameboy/nes, que son 8 
    indices de colores en una de las paletas del sistema
    y retorna el par de bytes que lo representa.
    '''
    # los bytes que representan el renglon
    first = second = 0
    for i, color_index in enumerate(row):
        lsbit = get_bit(color_index, 0)
        msbit = get_bit(color_index, 1)

        first  = set_bit(first,  7-i, lsbit)
        second = set_bit(second, 7-i, msbit)

    return (first, second)

def decode_row(first, second):
    '''
    Toma dos bytes que codifican un renglon de 
    un Tile de gameboy/nes y retorna el renglon
    que representan.
    '''
    row = [0] * 8
    for i in range(8):
        lsbit = get_bit(first,  7-i)
        msbit = get_bit(second, 7-i)

        row[i] = 2 * msbit + lsbit

    return row

def encode_tile(tile):
    byte_pairs = []

    return byte_pairs

def decode_tile(byte_pairs):
    tile = None

    return tile