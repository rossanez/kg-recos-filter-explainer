from argparse import ArgumentParser
from rdflib import Graph
from sys import argv

from config import Config
from user import genDescription

def loadKG(filename):
    print(f'Loading {filename} as an RDFLib graph ...')

    graph = Graph()
    graph.parse(filename, format="turtle")

    return graph

def main(args):
    arg_p = ArgumentParser('python describe_user.py', description='Generates a brief description on an userprofile KG.')
#    arg_p.add_argument('Catalog', metavar='catalog', type=str, default=None, help='catalog KG file (*.ttl)')
    arg_p.add_argument('Profile', metavar='profile', type=str, default=None, help='user-profile KG file (*.ttl)')

    args = arg_p.parse_args(args[1:])

#    catalog = args.Catalog
#    if catalog is None:
#        print('No catalog KG provided.')
#        exit(1)

    profile = args.Profile
    if profile is None:
        print('No user-profile KG provided.')
        exit(1)

#    catalogKG = loadKG(catalog)
    userProfileKG = loadKG(profile)
    
    cfg = Config()
    genDescription(userProfileKG, cfg.getUserPredicates())

if __name__ == '__main__':
    exit(main(argv))

