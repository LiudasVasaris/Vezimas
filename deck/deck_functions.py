from typing import Iterable, List

from numpy.random import shuffle

from card_encoding import encoded_cards, playing_cards, suits


def visualise_card(card: tuple) -> str:
    """Converts card encoding to string for visualisation
    Args:
        card: tuple that represents a card

    Returns:
        String representation of a card with emoji
    """
    return f"{playing_cards[card[0]]}{suits[card[1]]}"


def visualise_set_of_cards(card_list: Iterable, sort_cards: bool = False) -> str:
    """set of card encodings to string for visualisation
    Args:
        card_list: Iterable containing cards
        sort_cards: Flag to choose if visualisation should be sorted
        (hand cards are easier to look at sorted, while the card stack should not be sorted when represented)

    Returns:
        String representation of a list of cards
    """
    if sort_cards:
        card_list_to_viz = sorted(card_list, key=lambda card: (card[1], card[0]))
    else:
        card_list_to_viz = card_list

    return str([visualise_card(card) for card in card_list_to_viz])


class Deck:
    """Represents a standard deck of cards built using Constants from card_encoding"""

    def __init__(self):
        self.deck = list(encoded_cards)

    def __str__(self):
        return str(self.deck)

    def shuffle(self):
        """Shuffles deck"""
        shuffle(self.deck)

    def deal(self, no_cards: int = 1) -> List[tuple]:
        """Deals no_cards of cards by removing them from the deck"""
        return [self.deck.pop() for _ in range(no_cards)]

