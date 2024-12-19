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

def filterRecos(filename, catalogKG, userProfileKG, queryStr, userProps):
    print(f'Filtering recos from {filename} ...')

    split_filename = filename.split('.')
    output_filename = f'{split_filename[0]}_filtered.txt'

    with open(filename, 'r') as input:
        output = open(output_filename, 'w')
        for line in input:
            contents = line.strip().split("\t")
            item = contents[0]

            if userProfileKG is not None:
                conds = [o for o in userProfileKG.objects(predicate=URIRef(userProps[0]))]
                results = catalogKG.query(queryStr.replace("subj", item).replace("obj", conds[0]))
                if len(results) > 0 :
                    print(f'{item} is not suitable!')
                    output.write(f'{contents[0]}\t{contents[1]}\t*\n')
                else:
                    allergies = [o for o in userProfileKG.objects(predicate=URIRef(userProps[1]))]
                    if len(allergies) > 0:
                        for allergy in allergies:
                            deriveds = [s for s in catalogKG.subjects(predicate=RDF.type, object=URIRef(allergy))]
                            if len(deriveds) > 0:
                                print(f'{item} is not suitable, as it is related to {result[0]}!')
                                output.write(f'{contents[0]}\t{contents[1]}\t*\n')
                            else:
                                output.write(f'{contents[0]}\t{contents[1]}\n')
                    else:
                        output.write(f'{contents[0]}\t{contents[1]}\n')
            else: # No user-profile required
                results = catalogKG.query(queryStr.replace("subj", item))
                if len(results) > 0 :
                    print(f'{item} is not suitable!')
                    output.write(f'{contents[0]}\t{contents[1]}\t*\n')
                else:
                    output.write(f'{contents[0]}\t{contents[1]}\n')
        output.close()

    return output_filename

def main(args):
    arg_p = ArgumentParser('python filter.py', description='Filters a list of recommendations according to a predefined SPARQL query.')
    arg_p.add_argument('Catalog', metavar='catalog', type=str, default=None, help='catalog KG file (*.ttl)')
    arg_p.add_argument('Recos', metavar='recos', type=str, default=None, help='recomendations file (*.txt)')
    arg_p.add_argument('Profile', metavar='profile', type=str, default=None, help='user-profile KG file (*.ttl)')

    args = arg_p.parse_args(args[1:])

    catalog = args.Catalog
    if catalog is None:
        print('No catalog KG provided.')
        exit(1)

    recos = args.Recos
    if recos is None:
        print('No recommendations file provided.')
        exit(1)

    catalogKG = loadKG(catalog)

    profile = args.Profile
    if profile is not None:
        userProfileKG = loadKG(profile)

    cfg = Config()
    filterRecos(recos, catalogKG, userProfileKG, cfg.getFilterQuery(), cfg.getFilterUserProps())

if __name__ == '__main__':
    exit(main(argv))

