import pygame, json


class Map_Loader:
    def __init__(self):
        self.spawn_point = None
        self.edges = None
        self.tiles = []
        self.entities = []

    def Load(self,map_name):
        with open(f'map/{map_name}') as file:
            map_data = json.load(file)

        for key in map_data:
            for list in map_data[key]:
                for data in list:
                    if data != [-1]:
                        if data[1] == 'foliage' or data[1] == 'entity':
                            self.entities.append(data)
                        else:
                            self.tiles.append(data)

        self.spawn_point = [448,375]
        self.edges = [320,848,80,496]
        
        return map_data


map_loader = Map_Loader()