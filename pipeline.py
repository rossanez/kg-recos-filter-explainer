from argparse import ArgumentParser
from sys import argv

from config import Config
from explain import explainFilteredRecos
from filter import loadKG, filterRecos
from rerank import rerankRecos

def main(args):
    arg_p = ArgumentParser('python pipeline.py', description='Runs the entire pipeline')
    arg_p.add_argument('Catalog', metavar='catalog', type=str, default=None, help='catalog KG file (*.ttl)')
#    arg_p.add_argument('Profile', metavar='profile', type=str, default=None, help='user-profile KG file (*.ttl)')
    arg_p.add_argument('Recos', metavar='recos', type=str, default=None, help='recomendations file (*.txt)')
    arg_p.add_argument('-m', '--models', type=str, default="llama3-70b-8192", help='Comma-separated list of LLM models (e.g. \'llama3-70b-8192,mixtral-8x7b-32768,gemma2-9b-it\').')
    arg_p.add_argument('-t', '--temperatures', type=str, default="0", help='Comma-separated list of LLM temperatures (e.g. \'0,1,2\').')

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

    cfg = Config()
    reRankedFileName = rerankRecos(recos, catalogKG, cfg.getRerankerQuery())
    filteredFileName = filterRecos(reRankedFileName, catalogKG, cfg.getFilterQuery())

    models = args.models.split(',')
    temperatures = args.temperatures.split(',')

    for model in models:
        for temp in temperatures:
            print(f'\n\nProcessing {model} model, with temperature {temp} ...')
            explainFilteredRecos(filteredFileName, catalogKG, model, int(temp), cfg)

if __name__ == '__main__':
    exit(main(argv))

