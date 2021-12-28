import requests
import pprint
import json
pp = pprint.PrettyPrinter(indent=4)


class Pokemon:
    def __init__(self, name=None, abilities=None, types=None, height=None, weight=None):
        self.name = name
        if abilities is None:
            self.abilities = []
            if types is None:
                self.types = []
            self.height = height
            self.weight = weight

    def from_dict(self, data):
        for field in ['name', 'ability', 'type', 'height', 'weight']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f'<Pokemon>: {self.name}'

    def __str__(self):
        return f'{self.name}'


class Index:
    _list = []

    @classmethod
    def show(cls):
        print('!#' * 50)
        for idx, p in enumerate(cls._list):
            print(f'{idx+1}: {p}')
        print('!#' * 50)

    @classmethod
    def add(cls, pokemon_name):

        print(pokemon_name)

        if cls._list:
            for p in cls._list:
                if pokemon_name == p.name:
                    input("Please try again")
                    return
        try:
            print("Please wait")
            r = requests.get(
                f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}').json()
            print(r)
            p = Pokemon()
            data_dict = {
                'name': r['name'],
                'abilities': [a['ability']['name'] for a in r['ability']],
                'types': [t['type']['name'] for t in r['type']],
                'height': r['height'],
                'weight': r['weight'],
            }
            print("Complete")
            p.from_dict(data_dict)
            print("Pokemon added")
            cls._list.append(p)

        except Exception as error:
            print(error)
            input("Error please try again")

    @classmethod
    def sort(cls):
        sorted_dict = {}

        for p in cls._list:
            for t in p.type:
                if t not in sorted_dict:
                    sorted_dict[t] = {}
            for p in cls._list:
                for t in p.type:
                    if p.name not in sorted_dict[t]:
                        poke_data = {
                            p.name: {
                                'ability': p.ability,
                                'height': p.height,
                                'weight': p.weight,
                            }
                        }
                        sorted_dict[t].update(poke_data)
                    else:
                        print('Pokemon already included, please add another')
            pp.pprint(sorted_dict)

    @classmethod
    def run(cls):
        done = False

        while not done:

            cls.instructions()

            pokemon_choice = input(
                "Add pokemon to index.  Type 'end' to end the program")
            if pokemon_choice == 'end':
                done = True
            elif pokemon_choice == 'show':
                cls.show()
                input("Press 'Enter' to continue")
            else:

                cls.add(pokemon_choice)


Index.run()
