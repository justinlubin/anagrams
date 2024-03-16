#!/usr/bin/env python3

import itertools
import random
import sys

from collections import defaultdict

CLI_COLS = 4

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <dictionary file>")
    sys.exit(1)

DICTIONARY_PATH = sys.argv[1]


def canon(s):
    return "".join(sorted(s.lower()))


def combinations(s, k):
    for x in itertools.combinations(s, k):
        yield "".join(x)


main_map = defaultdict(list)

with open(DICTIONARY_PATH, "r") as f:
    for word in f:
        word = word.strip()
        c = canon(word)
        main_map[c].append(word.lower())


def anagrams(s):
    res = defaultdict(set)
    for k in range(1, len(s) + 1):
        for t in combinations(s, k):
            res[k].update(main_map[canon(t)])
        res[k] = sorted(res[k])
        if not res[k]:
            del res[k]
    return res


def cli_init():
    return input("phrase> ")


def cli_display(choices, word, anas):
    for size, options in anas.items():
        if not options:
            continue
        print(f"\nSize {size}")
        for i, option in enumerate(options):
            if i % CLI_COLS == 0 and i > 0:
                print()
            print(f"  [{size}.{i}: {option}]", end=" ")
        print()
    letters_remaining = len(word.replace(" ", ""))
    print()
    print("Choices:", choices)
    print(f"Remaining ({letters_remaining}):", word)
    print()


def cli_choose(choices, word, anas):
    response = input("choice> ")
    if not response:
        return None
    if "." not in response:
        size = len(response)
        option = anas[size].index(response)
        return size, option
    return map(int, response.split("."))


def rand_init(word=None):
    seed = random.randint(0, 1000000)
    random.seed(seed)
    print("Seed:", seed)
    return word if word else cli_init()


def rand_display(choices, word, anas):
    pass


def rand_choose(choices, word, anas):
    size = random.choice(list(anas.keys()))
    option = random.randint(0, len(anas[size]) - 1)
    return size, option


def interact(init, display, choose):
    word = init()
    word_history = []
    choices = []
    while word.strip():
        anas = anagrams(word)
        display(choices, word, anas)
        response = choose(choices, word, anas)
        if not response:
            choices.pop()
            word = word_history.pop()
            continue
        size, option = response
        choice = anas[size][option]
        choices.append(choice)
        word_history.append(word)
        for c in choice:
            word = word.replace(c, "", 1)
    return choices


print(interact(cli_init, cli_display, cli_choose))
