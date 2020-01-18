import os 
import json
import csv
import statistics
import sys
from argparse import ArgumentParser

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'converters'))
sys.path.insert(1, os.path.join(FILE, '..', 'util'))
from gameIO import *
from GameConverter import Converter
from CityMapper import CityMapper


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", required=True, help="Path to json-files folder")

    return parser.parse_args()

def convert_json_to_excel(json_file):
    print('converting file {} ...'.format(json_file))
    game = loadGameFromFile(json_file)
    cityMapper = CityMapper(game.getCityNamesAsList())

    metadata = ['round: ' + game.round, 'outcome: ' + game.outcome,
                'points: ' + game.points]
    stats_labels = ['ID', 'CONNECTIONS', 'LATITUDE', 'LONGITUDE', 'POPULATION', 'ECONOMY',
              'GOVERNMENT', 'HYGIENE', 'AWARENESS']
    events_labels = ['TYPE', 'NAME', 'INFECTIVITY', 'MOBILITY', 'DURATION', 'LETHALITY', 
                    'ROUND', 'SINCEROUND', 'PARTICIPANTS', 'PREVALENCE']

    # preparing results
    cities_list = []
    pathogens_list = []
    numbers_of_connections = []

    with open(os.path.join(os.path.splitext(json_file)[0] + '.csv'), 'w', encoding='utf-8', newline='\n') as csv_file1, open(os.path.join(os.path.splitext(json_file)[0] + '_events.csv'), 'w', encoding='utf-8', newline='\n') as csv_file2:
        stats_writer = csv.writer(csv_file1, delimiter=',')
        events_writer = csv.writer(csv_file2, delimiter=',')

        # writing metadata and labels
        stats_writer.writerow(metadata)
        stats_writer.writerow(stats_labels)
        events_writer.writerow(events_labels)

        # writing overall events
        for event in game.events:
            events_writer.writerow([event.type, event.pathogen.name, event.pathogen.infectivity,
                        event.pathogen.mobility, event.pathogen.duration, event.pathogen.lethality,
                        event.round, event.sinceRound, event.participants, event.prevalence])
            pathogens_list.append({'name': event.pathogen.name,
                                    'infectivity': event.pathogen.infectivity,
                                    'mobility': event.pathogen.mobility,
                                    'duration': event.pathogen.duration,
                                    'lethality': event.pathogen.lethality})

        events_writer.writerow([])
        events_writer.writerow(['ID'] + events_labels)

        # writing actual data
        for city in game.cities:
            mappedConnections = [str(cityMapper.getIdUsingCity(connection)) for connection in city.connections]
            stats_writer.writerow([cityMapper.getIdUsingCity(city.name), ','.join(sorted(mappedConnections)), city.latitude, city.longitude,
                            city.population, city.economy, city.government, city.hygiene, city.awareness])

            for event in city.events:
                events_writer.writerow([cityMapper.getIdUsingCity(city.name), event.type, event.pathogen.name,
                                        event.pathogen.infectivity, event.pathogen.mobility,
                                        event.pathogen.duration, event.pathogen.lethality,
                                        event.round, event.sinceRound, event.participants,
                                        event.prevalence])
                pathogens_list.append({'name': event.pathogen.name,
                                    'infectivity': event.pathogen.infectivity,
                                    'mobility': event.pathogen.mobility,
                                    'duration': event.pathogen.duration,
                                    'lethality': event.pathogen.lethality})

            cities_list.append(city.name)
            numbers_of_connections.append(len(city.connections))

    return cities_list, pathogens_list, max(numbers_of_connections), statistics.median(numbers_of_connections), statistics.stdev(numbers_of_connections)

def write_summary(summary, dir_path):
    print('writing summary ...')
    with open(os.path.join(dir_path, 'summary.json'), 'w',  encoding='utf-8') as json_file:
         json.dump(summary, json_file, indent=4)

    with open(os.path.join(dir_path, 'summary.csv'), 'w',  encoding='utf-8', newline='\n') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        overall_cities = []
        overall_pathogens = []

        writer.writerow(['game', 'max_connections', 'median_connections', 'sdv_connections'])

        for game in summary.keys():
            writer.writerow([game, summary[game]['max_connections'],
                            summary[game]['median_connections'], summary[game]['sdv_connections']])
            overall_cities += summary[game]['cities']
            overall_pathogens += summary[game]['pathogens']

        writer.writerow(['City'])
        overall_cities = list(set(overall_cities))
        for city in overall_cities:
            writer.writerow([city])

        writer.writerow([])
        writer.writerow(['Pathogen', 'Infectivity', 'Mobility', 'Duration', 'Lethality'])
        overall_pathogens = list({v['name']:v for v in overall_pathogens}.values())
        for pathogen in overall_pathogens:
            writer.writerow([pathogen['name'], pathogen['infectivity'], pathogen['mobility'], 
                            pathogen['duration'], pathogen['lethality']])

def main():
    args = parse_args()

    summary = {}

    # getting json filenames joined with the directory name
    files = getJsonFilesInDirectory(args.path)

    for json_file in files:
        # convertinng each json-file to csv-file
        cities, pathogens, max_connections, median_connections, sdv_connections = convert_json_to_excel(json_file)
        
        # preparing to write summary file
        game_number = getGameNumber(json_file)
        if game_number not in summary:
            summary[game_number] = {'cities': cities, 'pathogens': pathogens, 'max_connections': max_connections,
                                    'median_connections': median_connections, 'sdv_connections': sdv_connections}
        
    # writing summary file
    write_summary(summary, args.path)

if __name__ == "__main__":
    main()