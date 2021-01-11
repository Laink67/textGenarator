import random
import re
import codecs


def clear_text(text):
    regex = re.compile('[^a-zA-Zа-яА-Я]')
    res_text = regex.sub('', text)

    return res_text.lower()


def get_text_from_dir(dir):
    with codecs.open(dir, 'r', 'utf_8_sig') as file:
        text = file.read()

    return text


def gen_prev_next(tokens):
    corp = dict()

    for i in range(len(tokens) - 1):

        if tokens[i] in corp.keys():
            corp[tokens[i]].append(tokens[i + 1])
        else:
            corp[tokens[i]] = [tokens[i + 1]]

    return corp


def gen_bigrams(text):
    res = []

    for i in range(len(text) - 1):
        res.append((text[i], text[i + 1]))

    return res


def count_bigrams(bigrams):
    dictionary = dict()

    for pair in bigrams:
        if pair in dictionary:
            dictionary[pair] += 1.0
        else:
            dictionary[pair] = 1.0

    return dictionary


class Train:

    def __init__(self):
        self.bigrams_counts = dict()
        self.prev_next_words = dict()

    def fit(self, init_dir):
        text = input() if init_dir is None or init_dir == '' \
            else get_text_from_dir(init_dir)

        tokens = [clear_text(word) for word in text.split()]
        while '' in tokens:
            tokens.remove('')

        bigrams = gen_bigrams(tokens)

        self.bigrams_counts = count_bigrams(bigrams)

        # Generating words with possible next words
        self.prev_next_words = gen_prev_next(tokens)

        return self.gen_text('о', 14)

    # Generating word like a key and all possible words like value

    # Calculating probability for the next word
    def calc_prob(self, prev, next):
        bigram_count = self.bigrams_counts[(prev, next)]
        next_word_count = float(len(self.prev_next_words[prev]))
        probability = bigram_count / next_word_count

        return probability

    def gen_word(self, begin_word):

        probs_next_words = dict()

        for next_word in self.prev_next_words[begin_word]:
            probs_next_words[next_word] = self.calc_prob(begin_word, next_word)

        # Get word with max probability
        word, word_prob = sorted(probs_next_words.items())[-1]

        # To use different words except from the word with max probability
        # we add random.choice
        if word_prob < random.uniform(0, 1.3):
            word = random.choice(list(probs_next_words.keys()))

        return word

    def gen_text(self, begin_word, length):
        text = f'{begin_word} '

        for i in range(length):
            next_word = self.gen_word(begin_word)
            text += f'{next_word} '
            begin_word = next_word

        return text
