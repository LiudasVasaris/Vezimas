from unittest.mock import MagicMock

import pytest

from deck.deck_functions import visualise_card, visualise_set_of_cards, Deck

card2 = (9, 4)
card3 = (10, 3)
bad_card = (99, 99)

rep2 = "9♦️"
rep3 = "10♥️"


def test_visualise_card_with_correct_input_visualisation_is_returned():
    assert visualise_card(card2) == rep2


def test_visualise_card_with_incorrect_input_error_is_raised():
    with pytest.raises(KeyError):
        visualise_card(bad_card)


def test_visualise_set_card_with_correct_input_visualisation_is_returned():
    assert visualise_set_of_cards([card2, card3]) == f"['0: {rep2}', '1: {rep3}']"


def test_visualise_set_card_with_incorrect_input_error_is_raised():
    with pytest.raises(KeyError):
        visualise_set_of_cards([card2, bad_card])


def test_deck_shuffle_is_called():
    test_deck = Deck([card2, card3])
    test_deck.shuffle = MagicMock()
    test_deck.shuffle()

    test_deck.shuffle.assert_called_once()


def test_deck_deal_is_called():
    test_deck = Deck([card2, card3])
    test_deck.deal = MagicMock()
    test_deck.deal()

    test_deck.deal.assert_called_once()


def test_deck_deal_removes_a_card():
    test_deck = Deck([card2, card3])

    assert len(test_deck.deal()) == 1
    assert len(test_deck.deck) == 1
