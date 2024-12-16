from argparse import ArgumentParser
from rdflib import Graph, URIRef
from sys import argv

from config import Config

def loadKG(filename):
    print(f'Loading {filename} as an RDFLib graph ...')

    graph = Graph()
    graph.parse(filename, format="turtle")

    return graph

def getEntries(userProfileKG, predicates):
    print(f'Querying user-profike KG ...')

    descriptions = []
    for entry, title in userProfileKG.subject_objects(predicate=URIRef(predicates[0])):
        ratings = [g for g in userProfileKG.objects(subject=URIRef(entry), predicate=URIRef(predicates[1]))]
        rating = ratings[0].split('#')
        descriptions.append((title, rating[1]))

    descriptions.sort(key=lambda tup: tup[1])

    return descriptions

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
    entries = getEntries(userProfileKG, cfg.getUserPredicates())
    
    with open(f'user_description.txt', 'w') as output:
        output.write(f"This user has {len(entries)} items in his/her history.\nThey are the following, grouped by rating:\n\n")
        for entry in entries:
            output.write(f"\"{entry[0]}\"\t{entry[1]}\n")

if __name__ == '__main__':
    exit(main(argv))

