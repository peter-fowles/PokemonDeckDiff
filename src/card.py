# Ignore set names for basic energy types
BASIC_ENERGY = {'Fire Energy',
                  'Grass Energy', 
                  'Water Energy', 
                  'Psychic Energy', 
                  'Metal Energy', 
                  'Dark Energy', 
                  'Lightning Energy', 
                  'Fighting Energy'}

class PokemonCard:
    def __init__(self, name, set_id, type, set_num):
        self.__name = name
        self.__set = set_id
        self.__type = type
        self.__set_num = set_num

    def get_name(self):
        return self.__name
    
    def get_set(self):
        return self.__set
    
    def get_type(self):
        return self.__type
    
    def get_set_num(self):
        return self.__set_num

    def __eq__(self, other):
        result = True
        result &= self.get_type() == other.get_type()
        if self.get_type() != 'Pokémon':
            result &= self.get_set() == other.get_set()
        result &= self.get_name() == other.get_name()
        return result
    
    def __hash__(self):
        if self.get_type() == 'Energy' and self.get_name() in BASIC_ENERGY:
            return hash(self.get_name())
        return hash(f'{self.get_name()} {self.get_set()}')
    
    def __str__(self):
        return f'{self.get_name()} {self.get_set()} {self.get_set_num()}'
    
    def __lt__(self, other):
        return self == other and self.get_set_num() < other.get_set_num()
    
    def __repr__(self):
        return str(self)
    
    