import nltk
import re
import string
import codecs
from collections import Counter
import spacy


def worthaeufigkeiten_berechnen(text):
    # text = String
    # haeufigkeiten berechnen
    haeufigkeiten_dict = dict(Counter(text.split()))

    # dict sortieren
    haeufigkeiten_list_sorted = sorted(haeufigkeiten_dict.items(), key=lambda kv: kv[1], reverse=True)

    return haeufigkeiten_dict, haeufigkeiten_list_sorted


def remove_stopwords(text
                     , custom_stopwords_file='industry_classifier_custom_stopword_list'
                     , default_stopwords_language='german'):
    """

    :param default_stopwords_language:
    :param text:
    :param custom_stopwords_file: string, optional
        Voller Pfad zu einer benutzerdefinierten Datei mit Stoppwörtern.
        Dateiformat muss .csv sein.
        Inhalt der .csv-Datei: jede Zeile ist eine Stoppwort.

        Beispiel für Inhalt einer .csv-Datei:

        070316umschlagfu
        100prozentzielwert
        12f
        132r1


    :return:
    """
    default_stopwords = set(nltk.corpus.stopwords.words(default_stopwords_language))
    all_stopwords = default_stopwords

    if custom_stopwords_file:
        custom_stopwords = set(codecs.open(custom_stopwords_file, 'r', 'utf-8').read().splitlines())
        all_stopwords = default_stopwords | custom_stopwords
    else:
        pass
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token not in all_stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def tokenize_text(text):
    """
    Returns text tokenized as words
    :param str text: Text to be tokenized
    :return: Words
    :rtype: String


    Examples
    --------
    text = ' drehmomentwandlervorrichtung, insbesondere für einen antriebsstrang eines kraftfahrzeugs  '

    print(tokenize_text(titel[0]))
    ['drehmomentwandlervorrichtung',
    ',',
    'insbesondere',
    'für',
    'einen',
    'antriebsstrang',
    'eines',
    'kraftfahrzeugs']

    """
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens


def replace_special_characters(text, substitutionsstring=' '):
    """Entfernt special_characters gänzlich.

    special_characters = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' - siehe <pattern>
    Beispiele:
    Vorher: http //www.linkedin.com/company/daimler/
    Nachher: wwwlinkedincomcompanydaimler
    """
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub(substitutionsstring, token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def stem_words(text, model_name='de_core_news_sm'):
    nlp = spacy.load(model_name, disable=['ner', 'parser'])
    nlp.max_length = 2000000
    spacy_doc = nlp(text)
    stemmed_tokens = [token.lemma_ for token in spacy_doc]
    stemmed_text = ' '.join(stemmed_tokens)
    return stemmed_text


def keep_text_characters(text):
    filtered_tokens = []
    tokens = tokenize_text(text)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def remove_digits_from_text(text):
    # make this '49die' into this 'die'
    pattern = '[0-9]'
    tokens_original = tokenize_text(text)
    tokens = [re.sub(pattern, '', token) for token in tokens_original]
    text = ' '.join(tokens)
    return text


def remove_links(text):
    text = re.sub(r'http\S+', '', text)
    return text


def normalize_text(text
                    , tokenize=True
                    , only_text_chars=True
                    , filter_stopwords=True
                    , custom_stopwords_file_name=''
                    , word_stemming=True
                    , rm_special_char=True
                    , rm_links=True
                    , rm_digits_from_text=True
                    , spacy_model_name='de_core_news_sm'
                    , default_stopwords_language='german'
                   ):
    """

    :param default_stopwords_language:
    :param spacy_model_name:
    :type rm_links: bool
    :param rm_digits_from_text: bool
    :type rm_special_char: bool
    :param text:
    :param tokenize:
    :param only_text_chars:
    :param filter_stopwords:
    :param custom_stopwords_file_name:
    :param word_stemming:
    :return: Die Tokens des Textes, getrennt durch Abstand (' ')
    """
    # Lowercase all words
    text = text.lower()
    if word_stemming:
        text = stem_words(text, spacy_model_name)
    if rm_special_char:
        text = replace_special_characters(text)
    if only_text_chars:
        text = keep_text_characters(text)
    if filter_stopwords:
        text = remove_stopwords(text, custom_stopwords_file_name, default_stopwords_language)
    else:
        pass
    if rm_digits_from_text:
        text = remove_digits_from_text(text)
    if rm_links:
        text = remove_links(text)
    if tokenize:
        text = tokenize_text(text)

    return text
