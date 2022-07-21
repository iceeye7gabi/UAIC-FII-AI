import nltk
from nltk import tokenize
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

with open('computer-science.txt', 'r') as f:
    text = ''
    for s in f.readlines():
        if s.strip():
            if "." in s:
                text += s
            else:
                text += s.replace('\n', '.\n')
    text = tokenize.sent_tokenize(text)
    with open('result.txt', 'w') as out:
        for t in text:
            tokens = nltk.word_tokenize(t)
            tagged = nltk.pos_tag(tokens)
            TEMP = 'NVN'
            i = 0
            for tag in tagged:
                if i == 3:
                    break
                if TEMP[i] in tag[1]:
                    i += 1
            if i == 3:
                out.write(t + '\n')
