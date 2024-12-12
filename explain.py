from argparse import ArgumentParser
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
from sys import argv

from config import Config
from promptbuilder import PromptBuilder
from groqwrapper import GroqWrapper

def loadKG(filename):
    print(f'Loading {filename} as an RDFLib graph ...')

    graph = Graph()
    graph.parse(filename, format="turtle")

    return graph

def getPromptTriples(item, catalogKG, config):
    triples = []
    for pred in config.getPromptInputPredicates():
        for obj in catalogKG.objects(subject=URIRef(item), predicate=URIRef(pred)):
            if obj.startswith("http://"):
                triples.append(f'<{item}>\t<{pred}>\t<{obj}>\t. ')
            else:
                triples.append(f'<{item}>\t<{pred}>\t\"{obj}\"^^xsd:string\t. ')

    return triples

def explainFilteredRecos(filename, catalogKG, llmModel, llmTemp, config):
    print(f'Explaining filtered recos from {filename} ...')

    with open(filename, 'r') as input:
        split_filename = filename.split('.')
        output = open(f'{split_filename[0]}_explained_{llmModel}_temp{llmTemp}.txt', 'w')
        for line in input:
            contents = line.strip().split("\t")
            item = contents[0]
            if len(contents) > 2 :
                print(f'Generating explanation for {item} ...')
                prompt = PromptBuilder(config).build(getPromptTriples(item, catalogKG, config))
                explanation = GroqWrapper().query(content=prompt, model=llmModel, temp=llmTemp)
                print(f'-- {explanation}')
                output.write(f'{contents[0]}\t{contents[1]}\t*\t{explanation}\n')
            else:
                output.write(f'{contents[0]}\t{contents[1]}\n')
        output.close()

def main(args):
    arg_p = ArgumentParser('python explain.py', description='Explains a list of filtered recommendations using an LLM.')
    arg_p.add_argument('Catalog', metavar='catalog', type=str, default=None, help='catalog KG file (*.ttl)')
#    arg_p.add_argument('Profile', metavar='profile', type=str, default=None, help='user-profile KG file (*.ttl)')
    arg_p.add_argument('Filtered', metavar='filtered', type=str, default=None, help='filtered recomendations file (*.txt)')
    arg_p.add_argument('-m', '--model', type=str, default="llama3-70b-8192", help='LLM model.')
    arg_p.add_argument('-t', '--temperature', type=int, default=0, help='LLM temperature.')

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

    llmModel = args.model
    llmTemp = args.temperature

    catalogKG = loadKG(catalog)
#    userProfileKG = loadKG(profile)

    explainFilteredRecos(filtered, catalogKG, llmModel, llmTemp, Config())

if __name__ == '__main__':
    exit(main(argv))

