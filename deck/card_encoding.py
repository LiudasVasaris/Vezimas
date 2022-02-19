import itertools
from typing import Tuple

suits = {1: "♣️", 2: "♦️", 3: "♥️", 4: "♠️"}

# Ace gets pushed to the end to indicate it being higher
playing_cards = {
    9: 9,
    10: 10,
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}

ENCODED_CARDS = list(itertools.product(playing_cards, suits))

card_type = Tuple[int, int]
