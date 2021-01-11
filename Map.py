import os
import pygame

maps = []


class Map():  # класс карты
    def __init__(self, foldername, filename):
        # загрузка информации о карте из файла .osu
        file = open(f'maps\\{foldername}\\{filename}', encoding="utf-8").read().split('\n')
        self.dir = foldername
        general_line = file.index('[General]')
        self.general = {}
        cur_line = general_line + 1
        while file[cur_line].lstrip() != '':
            current = file[cur_line]
            tag = current[:current.find(':')]
            info = current[current.find(':') + 1:]
            self.general[tag] = info.lstrip()
            cur_line += 1

        difficulty_line = file.index('[Difficulty]')
        self.difficulty = {}
        cur_line = difficulty_line + 1
        while file[cur_line].lstrip() != '':
            current = file[cur_line]
            tag = current[:current.find(':')]
            info = current[current.find(':') + 1:]
            self.difficulty[tag] = info.lstrip()
            cur_line += 1

        metadata_line = file.index('[Metadata]')
        self.metadata = {}
        cur_line = metadata_line + 1
        while file[cur_line].lstrip() != '':
            current = file[cur_line]
            tag = current[:current.find(':')]
            info = current[current.find(':') + 1:]
            self.metadata[tag] = info.lstrip()
            cur_line += 1

        events_line = file.index('[Events]')
        self.events = []
        cur_line = events_line + 1
        while file[cur_line].lstrip() != '':
            current = file[cur_line]
            current = current.split(',')
            current = [i.lstrip() for i in current]
            self.events.append(current)
            cur_line += 1
        # внесение информации в атрибуты элемента класса
        self.audio_file_name = self.general['AudioFilename']
        self.mode = self.general['Mode']
        self.audio_lead_in = self.general['AudioLeadIn']

        self.title = self.metadata['Title']
        self.artist = self.metadata['Artist']
        self.creator = self.metadata['Creator']
        self.version = self.metadata['Version']
        self.map_id = self.metadata['BeatmapID']
        self.mapset_id = self.metadata['BeatmapSetID']

        self.HP = self.difficulty['HPDrainRate']
        self.OD = self.difficulty['OverallDifficulty']
        # загрузка сладеров, нот с карты
        objects_line = file.index('[HitObjects]')
        self.objects = []
        cur_line = objects_line + 1
        while cur_line < len(file) and file[cur_line].lstrip() != '':
            current = file[cur_line]
            current = current[:current.find(':')]
            current = current.split(',')
            current = [i.lstrip() for i in current]
            self.objects.append(current)
            cur_line += 1
        for i, elem in enumerate(self.objects):
            x, y, time, type, *another = elem
            if int(type) == 128:
                end_time = int(elem[5])
            else:
                end_time = 0
            self.objects[i] = [int(x) // (512 // 4), int(time), int(type), int(end_time)]
        # загрузка фона карты
        for elem in self.events:
            event_type, *another = elem
            if event_type == '0':
                c, background_file, x_offset, y_offset = another
                self.x_offset = int(x_offset)
                self.y_offset = int(y_offset)
                self.background_file = background_file.rstrip('"').lstrip('"')
                self.background = pygame.transform.smoothscale(
                    pygame.image.load(f'maps/{self.dir}/{self.background_file}'), (1120, 720))
                self.small_background = pygame.transform.smoothscale(self.background, (120, 80))


def import_maps():  # создает объекты класса Map, помещает их в maps
    songs = os.listdir(path="maps")
    maps = []
    for song in songs:
        file_names = os.listdir(path=f'maps/{song}')
        diffs = [diff for diff in file_names if diff.endswith('.osu')]
        for diff in diffs:
            map = Map(song, diff)
            if map.mode == '3':
                maps.append(map)
    return maps
