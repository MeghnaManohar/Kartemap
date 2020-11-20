from algorithms.shortest_path import Dijkstra
from graph.network import Network


def read_network_from_file(file_name, delimeter=','):
    """ Read from a file and build a network
    file_name: file to read from
    delimeter: delimeter that separates fields
    """
    cities = list()
    distances = dict()

    f = open(file_name, 'r')
    f = f.readlines()
    #Skip first line
    f.pop(0)
    for line in f:
        fields = line.rstrip().split(delimeter)
        city_1 = fields[11].strip('\"')
        city_2 = fields[16].strip('\"')
        distance = float(fields[24])
        # build the list of cities
        if city_1 not in cities:
            cities.append(city_1)
        if city_2 not in cities:
            cities.append(city_2)

        # build the dictionary based on city distances
        if cities.index(city_1) not in distances.keys():
            distances[cities.index(city_1)] = {cities.index(city_2): distance}
        if cities.index(city_2) not in distances[cities.index(city_1)].keys():
            distances[cities.index(city_1)][cities.index(city_2)] = distance

    return cities, distances


def main(start_city_index, end_city_index):
    # read network from file
    file_name = 'finaldata.csv'
    cities, distances = read_network_from_file(file_name)

    # build the network
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])

    start_city = network.get_nodes()[start_city_index]
    end_city = network.get_nodes()[end_city_index]

    # using Dijkstra's algorithm, compute smallest distance from start to end city
    Dijkstra.compute(network, network.get_node(start_city))

    for target_node in network.get_nodes():
        target_city = network.get_node(target_node)
        path = [target_city.get_name()]
        Dijkstra.compute_shortest_path(target_city, path)
     
        if path[0] == end_city:
            start_end_path = path[::-1] 
            #distance = target_city.get_weight()
    #translation = {39: None}
    return(start_end_path)
    print(start_end_path)
    #print(str(start_end_path).translate(translation)) 
    #print(f'{start_end_path}')

if __name__ == '__main__':
    main()
