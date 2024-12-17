from rdflib import URIRef

def getEntries(userProfileKG, predicates):
    print(f'Querying user-profike KG ...')

    descriptions = []
    for entry, title in userProfileKG.subject_objects(predicate=URIRef(predicates[0])):
        ratings = [g for g in userProfileKG.objects(subject=URIRef(entry), predicate=URIRef(predicates[1]))]
        rating = ratings[0].split('#')
        descriptions.append((title, rating[1]))

    descriptions.sort(key=lambda tup: tup[1])

    return descriptions

def genDescription(userProfileKG, predicates):
    print(f'Generating user description ...')

    entries = getEntries(userProfileKG, predicates)
    with open(f'user_description.txt', 'w') as output:
        output.write(f"This user has {len(entries)} items in his/her history.\nThey are the following, grouped by rating:\n\n")
        for entry in entries:
            output.write(f"\"{entry[0]}\"\t{entry[1]}\n")

