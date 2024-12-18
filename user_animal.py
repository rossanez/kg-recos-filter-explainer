from rdflib import URIRef

def getEntries(userProfileKG, predicates):
    print(f'Querying user-profike KG ...')

    descriptions = []
    for animal, id in userProfileKG.subject_objects(predicate=URIRef(predicates[0])):
        ages = [g for g in userProfileKG.objects(subject=URIRef(animal), predicate=URIRef(predicates[1]))]
        descriptions.append((predicates[1], ages[0]))
        conditions = [c for c in userProfileKG.objects(subject=URIRef(animal), predicate=URIRef(predicates[2]))]
        for condition in conditions:
            descriptions.append((predicates[2], condition))
        allergies = [a for a in userProfileKG.objects(subject=URIRef(animal), predicate=URIRef(predicates[3]))]
        for allergy in allergies:
            descriptions.append((predicates[3], allergy))

    descriptions.sort(key=lambda tup: tup[1])

    return descriptions

def genDescription(userProfileKG, predicates):
    print(f'Generating user description ...')

    entries = getEntries(userProfileKG, predicates)
    with open(f'user_description.txt', 'w') as output:
        output.write(f"This cow has the following characteristics:\n\n")
        for entry in entries:
            if entry[0].endswith('age'):
                output.write(f'It is {entry[1]} years old.\n')
            elif entry[0].endswith('condition'):
                condition = entry[1].split('#')
                condition = condition[1].replace('_', ' ')
                output.write(f'It suffers from {condition}.\n')
            elif entry[0].endswith('allergy'):
                allergy = entry[1].split('#')
                allergy = allergy[1].replace('_', ' ')
                output.write(f'It is allergic to {allergy}.\n')

