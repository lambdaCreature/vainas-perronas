import os
clear = lambda: os.system('clear')


def get_optimal_repr(k, base):
    # k non-negative integer
    # base, integer >= 2
    if k == 0: return [0]

    digitmap = list()

    u = k
    while u:
        q, r = divmod(u, base)

        u = q
        digitmap.insert(0, r)

    return digitmap 


def pprint_num(n, k=0, pad=5):
    '''
    Imprime las representaciones bonitas en binario 
    y hexadecimal del entero no negativo n.

    Retorna i, donde 2**i es la cantidad de bytes
    que se usaron  para imprimir el numero.

    Agrega pad espacios antes de cada representacion.

    La representacion se hara con al menos 2**k bytes.
    k es un entero no negativo.
    '''
    standard_digits = '0123456789ABCDEF'
    bin_repr = get_optimal_repr(n,  2)
    hex_repr = get_optimal_repr(n, 16)

    # inicialmente se intenta reresentar con 2**k bytes
    number_of_bits = 8 * (2 ** k) 
    
    # encuentra la minima cantidad de bytes suficientes 
    # que es una potencia de dos
    i = k
    while len(bin_repr) > number_of_bits:
        number_of_bits = number_of_bits * 2
        i = i + 1
    
    # agrega la la cantidad de ceros necesaria al inicio
    # para que len(bin_repr) == number_of_bits
    # y len(hex_repr) == number_of_bits // 4
    bin_repr = [0]*(number_of_bits    - len(bin_repr)) + bin_repr
    hex_repr = [0]*(number_of_bits//4 - len(hex_repr)) + hex_repr

    print('dec:' + ' '*pad + str(n))

    print('hex:', end=' '*pad)
    for i in range(0, number_of_bits//4, 2):
        first_nibble  = standard_digits[hex_repr[i]]
        second_nibble = standard_digits[hex_repr[i+1]]
        print(f'   {first_nibble}   {second_nibble}', end=' ')
    print()

    print('bin:', end=' '*pad)
    for i in range(0, number_of_bits, 8):
        byte = ''.join(standard_digits[bit] for bit in bin_repr[i:i+8])
        print(byte, end=' ')
    print()
p = pprint_num

addr16 = lambda num: pprint_num(num, 1)
addr32 = lambda num: pprint_num(num, 2)
addr64 = lambda num: pprint_num(num, 3)0