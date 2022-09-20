import pygame, json


class Map_Loader:
    def Load(self,map_name):
        with open(f'map/{map_name}') as file:
            map_data = json.load(file)

        # map_data['SPAWN'] = [448,384]
        # map_data['EDGES'] = [320,848,80,496]

        return map_data


map_loader = Map_Loader()