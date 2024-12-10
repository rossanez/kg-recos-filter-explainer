from argparse import ArgumentParser
from groq import Groq
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
from sys import argv

from config import Config

GROQ_TOKEN="<insert your token here>"

def loadKG(filename):
    print(f'Loading {filename} as an RDFLib graph ...')

    graph = Graph()
    graph.parse(filename, format="turtle")

    return graph

def obtainLLMInputTriples(item, catalogKG, config):
    print(f'Obtaining input for LLM ...')

    content = "Triples: "
    for pred in config.getPromptInputPredicates():
        for o in catalogKG.objects(subject=URIRef(item), predicate=URIRef(pred)):
            if o.startswith("http://"):
                content += f'<{item}>\t<{pred}>\t<{o}>\t. '
            else:
                content += f'<{item}>\t<{pred}>\t\"{o}\"^^xsd:string\t. '
    return f"{content}\nDescription: "

def getBasePrompt(config):
    print(f'Fetching base prompt ...')

    fewshots = config.getPromptFewShotExamples()
    prompt = config.getPromptInstruction()
    for ex in fewshots:
        prompt += f"\n{ex}\n\n\n"
    return prompt

def buildPrompt(input, config):
    return f'{getBasePrompt(config)}\n{input}'

def groqQuery(content):
    client = Groq(
              api_key=GROQ_TOKEN,
    )

    chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": content,
                }], model="llama3-70b-8192", temperature=1)

    return chat_completion.choices[0].message.content

def explainFilteredRecos(filename, catalogKG, config):
    print(f'Explaining filtered recos from {filename} ...')

    with open(filename, 'r') as input:
        split_filename = filename.split('.')
        output = open(f"{split_filename[0]}_explained.txt", 'w')
        for line in input:
            contents = line.strip().split("\t")
            item = contents[0]
            if len(contents) > 2 :
                print(f'Generating explanation for {item}')
                llmInput = obtainLLMInputTriples(item, catalogKG, config)
                prompt = buildPrompt(llmInput, config)
                explanation = groqQuery(prompt)
                output.write(f'{contents[0]}\t{contents[1]}\t*\t{explanation}\n')
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

    explainFilteredRecos(filtered, catalogKG, Config())

if __name__ == '__main__':
    exit(main(argv))

