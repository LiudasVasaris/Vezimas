import itertools

suits = {1: "♣️", 2: "♦️", 3: "♥️", 4: "♠️"}

# Ace gets pushed to the end to indicate it being higher
playing_cards = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}

encoded_cards = itertools.product(playing_cards, suits)
