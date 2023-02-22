"""
Initial thought vomit to getting all possible word fits for a line in a crossword puzzle.
Can definitely be improved...
"""
import enchant
import itertools
from tqdm import tqdm

alphabet = "abcdefghijklmnopqrstuvwxyz"

d = enchant.Dict("en_US")

word = input("Input the word (spaces are missing characters): ").lower()
print("Input word: '{}'".format(word.replace(' ', '_')))
word_len = len(word)
print("{} ({}^{}) character possibilities...".format((len(alphabet) ** word_len), len(alphabet), word_len))


def compare_words(in_word: str, orig_word: str):
    all_good = True
    for pc, c in zip(in_word, orig_word):
        if c != ' ' and pc != c:
            all_good = False
            break
    return all_good


# TODO: Instead of entire words, make fillers for all the empty spaces. (saves memory and time)
character_possibilities = [''.join(i) for i in itertools.product(alphabet, repeat=word_len)]
answer_possibilities = []
for w in tqdm(character_possibilities):
    if compare_words(w, word):
        if d.check(w):
            answer_possibilities.append(w)
print(answer_possibilities)
