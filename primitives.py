import re 

'''
Una entidad armonica es un objeto que sirve para modelar 
ideas fundamentales de teoria musical como notas, intervalos 
y formas de combinar estos primitivos.
'''

class HarmonicEntity:
    '''
    TODO: doc
    '''
    def __init__(self, diatonic: int, chromatic: int):
        self._diatonic  = diatonic
        self._chromatic = chromatic
    
    @property
    def diatonic(self):
        '''
        Esta propiedad y las dos que le siguen modelan 
        el indice diatonico del objeto 
        '''
        return self._diatonic
    @property
    def diatonic_normalized(self):
        return self.diatonic % 7
    @property
    def diatonic_octave(self):
        return self.diatonic // 7
    
    @property
    def chromatic(self):
        '''
        Esta propiedad y las dos que le siguen modelan
        el indice diatonico del objeto
        '''
        return self._chromatic
    @property 
    def chromatic_normalized(self):
        return self.chromatic % 12
    @property
    def chromatic_octave(self):
        return self.chromatic // 12
    
    @property 
    def offset(self):
        '''
        El offset es un entero k, de mod que 
        chromatize(self.diatonic) + offset = self.chromatic 
        '''
        return self.chromatic - chromatize(self.diatonic)
    
    @classmethod
    def from_str(cls, candidate):
        '''
        Construye una entidad armonica para el intervalo 
        o nota que se pase como arguemento a partir de una cadena
        '''
        note_names = '(C|D|E|F|G|A|B)'
        
        # TODO combina todos los casos en uno solo

        # prueba si es una nota escrita de forma convencional
        if matches := re.fullmatch(f'{note_names}(|#|##|b|bb)', candidate):
            note_name, accidentals = matches.groups()
            diatonic = 'CDEFGAB'.index(note_name)
            offset = len(accidentals) * (-1 if 'b' in accidentals else 1)
            return cls(diatonic, chromatize(diatonic) + offset)

        # prueba si es una nota generalizada 
        if matches := re.fullmatch(f'{note_names}(|#+|b+)(-?[1-9][0-9]*)', candidate):
            note_name, accidentals, octave = matches.group()
            diatonic = 'CDEFGAB'.index(note_name) + 7 * int(octave)
            offset = len(accidentals) * (-1 if 'b' in accidentals else 1)
            return cls(diatonic,  chromatize(diatonic) + offset)

        # prueba si es un intervalo
        if matches := re.fullmatch('(-?)(|#+|b+)([1-9][0-9]*)', candidate):
            inverted, accidentals, interv_type = matches.groups()

            offset = len(accidentals) * (-1 if 'b' in accidentals else 1)
            diatonic = int(interv_type)-1
            chromatic = chromatize(diatonic) + offset
            entity = cls(diatonic, chromatic)
            return -entity if inverted else entity 

        raise ValueError(f'"{candidate}" no representa ninguna entidad armonica')     

    def as_interval(self):
        '''
        Retorna una cadena representando a la entidad 
        como un intervalo
        '''
        # TODO implementa la opcion de simplificar
        if self.diatonic < 0:
            return '-' + (-self).as_interval(simplify)

        return f'{get_accidentals(self)}{self.diatonic+1}'
    
    def as_note(self, show_register=False):
        '''
        Retorna una cadena representando a la entidad 
        como una nota musical
        '''
        letter   = 'CDEFGAB'[self.diatonic_normalized]
        register = str(self.diatonic_octave) if show_register else ''

        return letter + get_accidentals(self) + register



    def __add__(self, other):
        if isinstance(other, HarmonicEntity):
            final_diatonic  = self.diatonic + other.diatonic
            final_chromatic = self.chromatic + other.chromatic
            return HarmonicEntity(final_diatonic, final_chromatic) 
        raise ValueError('Solo se puede sumar a otras entidades armonicas')
    
    def __neg__(self):
        return HarmonicEntity(-self.diatonic, -self.chromatic)

    def __sub__(self, other):
        if isinstance(other, HarmonicEntity):
            return self + (-other)
        raise ValueError('Solo se puede restar con otras entidades armonicas')

    def __mul__(self, other):
        if isinstance(other, int):
            final_diatonic = self.diatonic * other
            final_chromatic = self.chromatic * other
            return HarmonicEntity(final_diatonic, final_chromatic)
        raise ValueError('Solo se puede escalar por un entero')
    
    def __rmul__(self, other):
        return self * other

HE = HarmonicEntity

Entity = HarmonicEntity.from_str

def chromatize(diatonic: int):
    '''
    Computa el mapeo de indices diatonicos a
    indices cromaticos
    '''
    q, r = divmod(diatonic, 7)
    return 12 * q + (0, 2, 4, 5, 7, 9, 11)[r]

def get_accidentals(entity):
    return ('#' if entity.offset > 0 else 'b') * abs(entity.offset)


def make_major(key):
    return ' '.join(map(lambda entity: entity.as_note(), [Entity(key) + Entity(degree) for degree in '1 2 3 4 5 6 7'.split()]))

if __name__ == '__main__':
    # experiment and fool around uwu
    ...