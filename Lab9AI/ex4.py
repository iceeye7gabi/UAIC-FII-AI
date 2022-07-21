import lightrdf

parser = lightrdf.xml.Parser()

f = open('result.txt', 'r')
text = f.readlines()
f.close()
values = list()
with open("ontology.owl", "rb") as ont:
    for triple in parser.parse(ont, base_iri=None):
        value = triple[0].split('/')[-1].split('#')[-1]
        if value not in values:
            values.append(value)
with open("result1.txt", "w") as out:
    for word in values:
        for t in text:
            t = t.strip()
            arr = t.split(' ')
            try:
                index = arr.index(word)
                phrase = arr[max(index - 5, 0): min(index + 5, len(t) - 1)]
                if len(phrase):
                    for p in phrase:
                        out.write(p + ' ')
                    out.write('\n')
            except ValueError:
                continue
