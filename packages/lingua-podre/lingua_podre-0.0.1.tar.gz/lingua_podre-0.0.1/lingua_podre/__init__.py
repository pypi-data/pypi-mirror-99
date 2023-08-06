from os.path import dirname, join
from os import listdir
import json

langs_json = join(dirname(__file__), "res", "languages.json")

try:
    with open(langs_json) as f:
        langs = json.load(f)
except:
    langs = {'ar': 'arabic', 'bg': 'bulgarian', 'ca': 'catalan', 'cs': 'czech',
             'da': 'danish', 'nl': 'dutch', 'en': 'english', 'fi': 'finnish',
             'fr': 'french', 'de': 'german', 'gu': 'gujarati', 'he': 'hebrew',
             'hi': 'hindi', 'hu': 'hungarian', 'id': 'indonesian',
             'ms': 'malaysian', 'it': 'italian', 'nb': 'norwegian',
             'pl': 'polish',  'pt': 'portuguese', 'ro': 'romanian',
             'ru': 'russian', 'sk': 'slovak', 'es': 'spanish',
             'sv': 'swedish', 'tr': 'turkish', 'uk': 'ukrainian',
             'vi': 'vietnamese'}

lang_codes = {v: k for k, v in langs.items()}


def load_wordlist(paths):
    words = {}
    if isinstance(paths, str):
        paths = [paths]
    for path in paths:
        for f in listdir(path):
            if f.endswith(".txt"):
                lang_name = f.rstrip(".txt")
                if lang_name not in lang_codes:
                    continue
                with open(join(path, f)) as wrdlist:
                    lang_code = lang_codes[lang_name]
                    words[lang_code] = wrdlist.read().split("\n")
    return words


wordlists = [join(dirname(__file__), "res", "stopwords"),
             join(dirname(__file__), "res", "1000")]
stopwords = load_wordlist(wordlists)


def get_word_counts(text):
    if isinstance(text, str):
        text = text.split(" ")
    count = {}
    for w in text:
        for l in stopwords:
            if w in stopwords[l]:
                if l not in count:
                    count[l] = 1
                else:
                    count[l] += 1
    return count


def get_lang_scores(text):
    count = get_word_counts(text)
    # make scores sum up to 1
    total = sum(v for k, v in count.items())
    return {k: v / total for k, v in count.items()}


def predict_lang(text):
    scores = get_lang_scores(text)
    top = max(v for k, v in scores.items())
    return [k for k, v in scores.items() if v == top]

