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

def filterRecos(filename, catalogKG, queryStr):
    print(f'Filtering recos from {filename} ...')

    with open(filename, 'r') as input:
        output = open("filtered.txt", 'w')
        for line in input:
            contents = line.strip().split("\t")
            item = contents[0]
            results = catalogKG.query(queryStr.replace("subj", item))
            if len(results) > 0 :
                print(f'{item} is not suitable!')
                output.write(f'{contents[0]}\t{contents[1]}\t*\n')
            else:
                output.write(f'{contents[0]}\t{contents[1]}\n')
        output.close()

def main(args):
    arg_p = ArgumentParser('python filter.py', description='Filters a list of recommendations according to a predefined SPARQL query.')
    arg_p.add_argument('Catalog', metavar='catalog', type=str, default=None, help='catalog KG file (*.ttl)')
#    arg_p.add_argument('Profile', metavar='profile', type=str, default=None, help='user-profile KG file (*.ttl)')
    arg_p.add_argument('Recos', metavar='recos', type=str, default=None, help='recomendations file (*.txt)')

    args = arg_p.parse_args(args[1:])

    catalog = args.Catalog
    if catalog is None:
        print('No catalog KG provided.')
        exit(1)

#    profile = args.Profile
#    if profile is None:
#        print('No user-profile KG provided.')
#        exit(1)

    recos = args.Recos
    if recos is None:
        print('No recommendations file provided.')
        exit(1)

    catalogKG = loadKG(catalog)
#    userProfileKG = loadKG(profile)

    cfg = Config()
    filterRecos(recos, catalogKG, cfg.getFilterQuery())

if __name__ == '__main__':
    exit(main(argv))

