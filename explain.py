from argparse import ArgumentParser
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
from sys import argv

from config import Config

def loadKG(filename):
    print(f'Loading {filename} as an RDFLib graph ...')

    graph = Graph()
    graph.parse(filename, format="turtle")

    return graph

def explainFilteredRecos(filename, catalogKG):
    print(f'Explaining filtered recos from {filename} ...')

    with open(filename, 'r') as input:
        output = open("explained.txt", 'w')
        for line in input:
            contents = line.strip().split("\t")
            item = contents[0]
            if len(contents) > 2 :
                print(f'Found: {item} is not suitable!')
                output.write(f'{contents[0]}\t{contents[1]}\t*\texplanation\n')
            else:
                output.write(f'{contents[0]}\t{contents[1]}\n')
        output.close()

def main(args):
    arg_p = ArgumentParser('python explain.py', description='Explains a list of filtered recommendations using an LLM.')
    arg_p.add_argument('Catalog', metavar='catalog', type=str, default=None, help='catalog KG file (*.ttl)')
#    arg_p.add_argument('Profile', metavar='profile', type=str, default=None, help='user-profile KG file (*.ttl)')
    arg_p.add_argument('Filtered', metavar='filtered', type=str, default=None, help='filtered recomendations file (*.txt)')

    args = arg_p.parse_args(args[1:])

    catalog = args.Catalog
    if catalog is None:
        print('No catalog KG provided.')
        exit(1)

#    profile = args.Profile
#    if profile is None:
#        print('No user-profile KG provided.')
#        exit(1)

    filtered = args.Filtered
    if filtered is None:
        print('No filtered recommendations file provided.')
        exit(1)

    catalogKG = loadKG(catalog)
#    userProfileKG = loadKG(profile)

    cfg = Config()
    explainFilteredRecos(filtered, catalogKG)

if __name__ == '__main__':
    exit(main(argv))

