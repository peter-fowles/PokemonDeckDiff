import pathlib
import re
from card import PokemonCard
from termcolor import colored

SOURCE = re.compile(r'(Source): (https://.+)')
CATEGORY = re.compile(r'(.+): ([\d]+)')
CARD = re.compile(r'([\d]+) ([\S\s]+) ([A-Z]{3}) ([\d]+)')

class Deck:
    def __init__(self, deck_file):
        self.__name = pathlib.Path(deck_file).name
        self.__pokemon = dict()
        self.__trainers = dict()
        self.__energy = dict()
        self.__num_pokemon = 0
        self.__num_trainers = 0
        self.__num_energy = 0
        self.__source = ''
        self.parse_file(deck_file)

    def parse_file(self, deck_file):
        f = open(deck_file, mode='r', encoding='utf-8')
        category_count = 0
        total_cards = 0
        curr_section = ''
        for line in f:
            if SOURCE.match(line.strip()):
                source = SOURCE.match(line.strip())
                self.__source = source.group(2)
            elif CATEGORY.match(line.strip()):
                if category_count != 0:
                    raise Warning(f'Number of cards in {curr_section} section is off by {category_count} in {self.get_name()}')
                category = CATEGORY.match(line.strip())
                curr_section = category.group(1)
                category_count = int(category.group(2))
            elif CARD.match(line.strip()):
                card_match = CARD.match(line.strip())
                count = card_match.group(1)
                name = card_match.group(2)
                set = card_match.group(3)
                set_num = card_match.group(4)
                card = PokemonCard(name, set, curr_section, int(set_num))
                for _ in range(int(count)):
                    category_count -= 1
                    total_cards += 1
                    match curr_section:
                        case 'Pokémon':
                            if card not in self.__pokemon:
                                self.__pokemon[card] = 0
                            self.__pokemon[card] += 1
                            self.__num_pokemon += 1
                        case 'Trainer':
                            if card not in self.__trainers:
                                self.__trainers[card] = 0
                            self.__trainers[card] += 1
                            self.__num_trainers += 1
                        case 'Energy':
                            if card not in self.__energy:
                                self.__energy[card] = 0
                            self.__energy[card] += 1
                            self.__num_energy += 1
        f.close()
        if total_cards != 60:
            raise Warning(f'There are {total_cards} cards in the deck {self.get_name()}!')
        if self.__num_pokemon == 0:
            raise Warning(f'There are no Pokémon in the deck! {self.get_name()}')

    def get_name(self):
        return self.__name
    
    def get_pokemon(self):
        return self.__pokemon
    
    def get_trainers(self):
        return self.__trainers
    
    def get_energy(self):
        return self.__energy
    
    def get_pokemon_count(self):
        return self.__num_pokemon
    
    def get_trainer_count(self):
        return self.__num_trainers
    
    def get_energy_count(self):
        return self.__num_energy
    
    def get_source(self):
        if self.__source == '':
            return 'unknown'
        return self.__source
    
    def __str__(self):
        s = []
        if self.get_source() != 'unknown':
            s.append(f'Source: {self.get_source()}\n')
        
        s.append(f'Pokémon: {self.get_pokemon_count()}')
        for pokemon, count in self.get_pokemon().items():
            s.append(f'{count} {pokemon}')
        s.append('')

        s.append(f'Trainer: {self.get_trainer_count()}')
        for trainer, count in self.get_trainers().items():
            s.append(f'{count} {trainer}')
        s.append('')

        s.append(f'Energy: {self.get_energy_count()}')
        for energy, count in self.get_energy().items():
            s.append(f'{count} {energy}')

        return '\n'.join(s)
    
    def __repr__(self):
        return str(self)
    
    def __and__(self, other):
        pokemon = dict()
        trainer = dict()
        energy = dict()
        for card, item in self.get_pokemon().items():
            if card in other.get_pokemon():
                pokemon[card] = min(item, other.get_pokemon()[card])
        for card, item in self.get_trainers().items():
            if card in other.get_trainers():
                trainer[card] = min(item, other.get_trainers()[card])
        for card, item in self.get_energy().items():
            if card in other.get_energy():
                energy[card] = min(item, other.get_energy()[card])
        result = {
            'Pokémon': pokemon,
            'Trainer': trainer,
            'Energy': energy
        }
        return result

    def __sub__(self, other):
        '''
        Returns the changes necessary to get from this deck to the other deck
        '''
        pokemon = dict()
        trainer = dict()
        energy = dict()
        for card, count in self.get_pokemon().items():
            if card in other.get_pokemon():
                pokemon[card] = -(count - other.get_pokemon()[card])
            else:
                pokemon[card] = -count
        for card, count in self.get_trainers().items():
            if card in other.get_trainers():
                trainer[card] = -(count - other.get_trainers()[card])
            else:
                trainer[card] = -count
        for card, count in self.get_energy().items():
            if card in other.get_energy():
                energy[card] = -(count - other.get_energy()[card])
            else:
                energy[card] = -count

        for card, count in other.get_pokemon().items():
            if card not in self.get_pokemon():
                pokemon[card] = count
        for card, count in other.get_trainers().items():
            if card not in self.get_trainers():
                trainer[card] = count
        for card, count in other.get_energy().items():
            if card not in self.get_energy():
                energy[card] = count
                
        result = {
            'Pokémon': pokemon,
            'Trainer': trainer,
            'Energy': energy
        }
        return result
    
    def diff(self, other):
        diff_1 = self - other
        output = []
        output.append(colored(f'-{self.get_name()}', 'red'))
        output.append(colored(f'+{other.get_name()}', 'green'))
        output.append('')
        total_diff = 0
        for category_name, cards in diff_1.items():
            removed_cards = []
            added_cards = []
            category_removed = 0
            category_added = 0
            for card, count in cards.items():
                if count < 0:
                    removed_cards.append(colored(f'-{abs(count)} {card}', 'red'))
                    category_removed += abs(count)
                if count > 0:
                    added_cards.append(colored(f'+{count} {card}', 'green'))
                    category_added += count
            total_diff += category_removed
            output.append(f'{category_name}: ' + colored(f'-{category_removed}', 'red') + ' ' + colored(f'+{category_added}', 'green'))
            output += [card for card in removed_cards + added_cards]
            output.append('')
        output.append(f'Total Difference: {total_diff} Cards')
        return '\n'.join(output)

        