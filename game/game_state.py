from functools import reduce
from typing import List

from deck.deck_functions import Card, ENCODED_CARDS
from player.player_functions import Player, OptionalCardList


class GameState:
    """Game state representation class, containing adjustment functions and array output
    Args:
        players: players in a given game
        card_stack: stack of cards on table
        card_to_beat: flag to determine if last card on stack must be beaten
    """

    def __init__(
        self, players: List["Player"], card_stack: OptionalCardList, card_to_beat: bool
    ):
        self.players = players
        self.player_state = {
            player.name: {
                "is_active": True,
                "suit": player.suit,
                "no_cards": len(player.hand),
                "known_cards": [Card((9, player.suit))],
            }
            for player in players
        }
        self.play_state = {"card_stack": card_stack, "card_to_beat": card_to_beat}

    def add_known_cards(
        self, player: "Player", list_of_cards: List[Card]
    ):
        """Marks cards as known in player hands"""
        self.player_state[player.name]["known_cards"] += list_of_cards
        self.player_state[player.name]["no_cards"] += len(list_of_cards)
        self.play_state["card_stack"] = []

    def remove_known_cards(
        self, player: "Player", list_of_cards: List[Card], card_stack: OptionalCardList
    ):
        """Removes card as known in player hands"""
        [
            self.player_state[player.name]["known_cards"].remove(card)
            for card in list_of_cards
            if card in self.player_state[player.name]["known_cards"]
        ]
        self.player_state[player.name]["no_cards"] -= len(list_of_cards)
        self.play_state["card_stack"] = card_stack

    def remove_player(self, player: "Player"):
        """Marks player as inactive"""
        self.player_state[player.name]["is_active"] = False

    def adjust_card_to_beat(self, card_to_beat: bool):
        """Adjust card_to_beat flag"""
        self.play_state["card_to_beat"] = card_to_beat

    def __repr__(self):
        known_cards = (
            reduce(
                lambda a, b: a + b["known_cards"], self.player_state.values(), list()
            )
            + self.play_state["card_stack"]
        )
        unk_cards = [card for card in ENCODED_CARDS if card not in known_cards]

        return f"""player state: {self.player_state}
play state: {self.play_state}
known_cards: {len(known_cards)}
unknown_cards: {len(unk_cards)}"""
