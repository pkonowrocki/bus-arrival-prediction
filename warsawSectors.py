from math import ceil, floor

# Center of the city of Warsaw
center_lon = 20.9211124
center_lat = 52.2330653

edge_lon = 20.8675894 # lat edge of the city - here assumed to be Ursus
edge_lat = 52.1292396 # lon edge of the city - here assumed to be Metro Kabaty

class WarsawSectors:

    def __init__(self, debug, number_of_sectors):
        self.debug = debug
        number_of_sectors = number_of_sectors * 2 # because we will have also negative sectors
        distance_lon = center_lon - edge_lon
        distance_lat = center_lat = edge_lat
        self.sector_length_lon = distance_lon / number_of_sectors
        self.sector_length_lat = distance_lat / number_of_sectors
        if self.debug:
            print(f'distance_lon: {distance_lon}')
            print(f'distance_lat: {distance_lat}')
            print(f'self.sector_length_lon: {self.sector_length_lon}')
            print(f'self.sector_length_lon: {self.sector_length_lon}')

    def get_sector(self, lon, lat):
        value_lon = lon - center_lon
        value_lat = lat - center_lat
        if value_lon > 0:
            sector_lon = int(ceil(value_lon / self.sector_length_lon))
        else:
            sector_lon = int(floor(value_lon / self.sector_length_lon))
        if value_lat > 0:
            sector_lat = int(ceil(value_lat / self.sector_length_lat))
        else:
            sector_lat = int(floor(value_lat / self.sector_length_lat))
        if self.debug:
            print(f'center_lon: {center_lon}')
            print(f'center_lat: {center_lat}')
            print(f'lon: {lon}')
            print(f'lat: {lat}')
            print(f'value_lon: {value_lon}')
            print(f'value_lat: {value_lat}')
            print(f'sector_lon: {sector_lon}')
            print(f'sector_lat: {sector_lat}')
        return f"{sector_lon}:{sector_lat}"