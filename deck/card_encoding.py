import itertools
from typing import Tuple

SUITS = {1: "♣️", 2: "♦️", 3: "♥️", 4: "♠️"}

# Ace gets pushed to the end to indicate it being higher
PLAYING_CARDS = {
    9: 9,
    10: 10,
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}

ENCODED_CARDS = list(itertools.product(PLAYING_CARDS, SUITS))
QUEEN_OF_SPADES = (12, 1)

card_type = Tuple[int, int]
