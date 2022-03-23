import itertools
from typing import Iterable, List

from numpy import random

from deck.card_encoding import PLAYING_CARDS, SUITS


class Card:
    """Data class of a card"""

    def __init__(self, card_representation: tuple):
        # Copy the list, to avoid mutating the wrong list by accident
        self.face = card_representation[0]
        self.suit = card_representation[1]

    def __lt__(self, other: "Card"):
        return self.face < other.face

    def __gt__(self, other: "Card"):
        return self.face > other.face
=======
def visualise_set_of_cards(
    card_list: Iterable[card_type], sort_cards: bool = False
) -> str:
    """set of card encodings to string for visualisation
    Args:
        card_list: Iterable containing cards
        sort_cards: Flag to choose if visualisation should be sorted
        (hand cards are easier to look at sorted, while the card stack should not be sorted when represented)

    def __eq__(self, other: "Card"):
        return self.face == other.face and self.suit == other.suit

    def __str__(self):
        return f"{PLAYING_CARDS[self.face]}{SUITS[self.suit]}"


    def __repr__(self):
        return f"Card({self.face},{self.suit})"
    return str(
        [f"{idx}: {card}" for idx, card in enumerate(card_list_to_viz)]
    )


class Deck:
    """Represents a standard deck of cards built using Constants from card_encoding
    Args:
        card_list: list of cards for deck to consist of"""

    def __init__(self, card_list: List[Card]):
        # Copy the list, to avoid mutating the wrong list by accident
        self.deck = card_list.copy()
        self.init_deck = card_list.copy()

    def __str__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def shuffle(self):
        """Shuffles deck"""
        random.shuffle(self.deck)

    def deal(self, no_cards: int = 1) -> List[Card]:
        """Deals no_cards of cards by removing them from the deck"""
        return [self.deck.pop() for _ in range(no_cards)]

    def reset_deck(self):
        """Resets deck to contain all cards"""
        self.deck = self.init_deck.copy()



def visualise_set_of_cards(card_list: Iterable[Card]) -> str:
    """set of card encodings to string for visualisation
    Args:
        card_list: Iterable containing cards

    Returns:
        String representation of a list of cards
    """

    return str([f"{idx+1}: {card}" for idx, card in enumerate(card_list)])


ENCODED_CARDS = [Card(c) for c in itertools.product(PLAYING_CARDS, SUITS)]
QUEEN_OF_SPADES = Card((12, 1))
NINES = [Card(c) for c in [(9, 1), (9, 2), (9, 3), (9, 4)]]
class Card:
    """Data class of a card"""

    def __init__(self, card_representation: tuple):
        # Copy the list, to avoid mutating the wrong list by accident
        self.face = card_representation[1]
        self.suit = card_representation[0]

    def __lt__(self, other: "Card"):
        return self.face < other.face  # To get called on comparison using < operator.

    def __gt__(self, other: "Card"):
        return self.face > other.face  # To get called on comparison using > operator.

    def __str__(self):
        return f"{PLAYING_CARDS[self.face]}{SUITS[self.suit]}"
