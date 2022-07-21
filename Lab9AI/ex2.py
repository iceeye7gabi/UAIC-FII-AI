import lightrdf


def get_element(t, i):
    return t[i].split('/')[-1].split('#')[-1]


parser = lightrdf.xml.Parser()
strng = input("Word:")
strng = strng.replace(' ', '_')
print(strng)
with open("ontology.owl", "rb") as f:
    for triple in parser.parse(f, base_iri = None):
        word = get_element(triple, 0)
        relation = get_element(triple, 1)
        withWho = get_element(triple, 2)
        if word == strng and relation == 'superTopicOf':
            print(word + ' superTopicOf ' + withWho)