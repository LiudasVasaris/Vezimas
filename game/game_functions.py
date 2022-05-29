from typing import Optional, List

from deck.card_encoding import SUITS
from deck.deck_functions import Deck, Card, QUEEN_OF_SPADES, NINES
from player.bot_classes import PlayerType
from player.player_functions import Player, MyCycle, card_play_input
from collections import deque


class Vezimas:
    """Represents the class used to play the game Vezimas
    Args:
        deck_of_cards: deck to be used for the game
        player_count: number of players that will start the game
        player_names: (Optional) provide names for players, otherwise they will be numbered
        include_bots: flag if bots should be included in game
        bot_level: bot class for bots to play as
    """

    def __init__(
        self,
        deck_of_cards: Deck,
        player_count: int,
        include_bots: bool,
        bot_level: PlayerType,
        player_names: Optional[List[str]] = None,
    ):
        self.deck = deck_of_cards
        self.player_count = player_count
        self.include_bots = include_bots
        self.bot_level = bot_level

        if player_names and player_count != len(player_names):
            raise ValueError(
                f"Incorrect number of names provided, expected {player_count}, got {len(player_names)}"
            )

        self.player_names = player_names or [f"Player {i}" for i in range(player_count)]
        self.bot_list = [False] + [True] * (player_count - 1)
        self.players = [
            Player(name, bot_flag, self.bot_level)
            for name, bot_flag in zip(self.player_names, self.bot_list)
        ]

    def set_player_reference(self):
        """Method that sets player references"""
        shifted_players_forward, shifted_players_back = (
            deque(self.players.copy()),
            deque(self.players.copy()),
        )
        shifted_players_forward.rotate(1)
        shifted_players_back.rotate(-1)
        [
            player.add_player_reference(prev_player, next_player)
            for player, prev_player, next_player in zip(
                self.players, shifted_players_back, shifted_players_forward
            )
        ]

    def deal_cards(self):
        """Method that shuffles and deals cards to the players"""
        cards_per_player = int(len(self.deck) / self.player_count)
        self.deck.shuffle()
        for player in self.players:
            player.add_cards(self.deck.deal(cards_per_player))

    def set_trumps(self):
        """Setting trumps for the players using Queen of spades start of game method

        Returns:
            Player who got the Queen of spades (to start off the first game)"""
        suit_list = list(SUITS.keys())
        for player in self.players:
            if player.has_card(QUEEN_OF_SPADES):
                player.suit = suit_list[0]  # First suit is spades
                player.starting_player = True  #  Queen of spades starts game
                next_player = player.next_player

                for set_suit in suit_list[1:]:
                    if next_player.suit:
                        break
                    next_player.suit = set_suit
                    next_player = next_player.next_player
                return player

    def share_nines(self):
        """Method for `returning` each nine card to its suits owner"""
        for player in self.players:
            player.remove_cards(NINES)
            nine_to_add = Card((9, player.suit))
            player.add_cards([nine_to_add])

    def remove_starting_player_flags(self):
        """Method for resetting starting player flag"""
        for player in self.players:
            player.starting_player = False

    def get_starting_player(self) -> Player:
        """Method for retrieving starting player"""
        for player in self.players:
            if player.starting_player:
                return player
        raise ValueError("Starting player not set")

    def sort_cards(self):
        """Method for sorting cards of each player"""
        [player.sort_cards() for player in self.players]

    def check_worst_player(self) -> Player:
        """Method for checking score of worst player"""
        return max(self.players, key=lambda p: p.score)

    def reset_cards(self):
        """Method for resetting deck and player hands after the trick"""
        self.deck = self.deck.reset_deck()
        [player.remove_all_cards() for player in self.players]


def check_play_validity(
    card_stack: List[Card], card_to_beat: Optional[Card], player: Player
) -> bool:
    """Checks if played card obeys the game rules
    Args:
        card_stack: stack of cards already played
        card_to_beat: card played to beat the stack
        player: player that is making the play

    Returns: True if play is correct (or no card provided), False otherwise
    """
    if not card_to_beat:
        return True
    last_card = card_stack[-1]
    next_player_suit = None
    next_player_to_play = player.next_player

    while next_player_suit is None:
        if next_player_to_play.hand:
            next_player_suit = next_player_to_play.suit
        else:
            next_player_to_play = next_player_to_play.next_player

    if last_card.suit == player.suit and card_to_beat.suit != player.suit:
        return False

    if last_card.suit == player.suit and last_card > card_to_beat:
        return False

    if last_card.suit == next_player_suit and card_to_beat.suit != player.suit:
        return False

    if last_card.suit != next_player_suit and last_card.suit != player.suit:
        if card_to_beat.suit != player.suit:
            if card_to_beat.suit != last_card.suit:
                return False
            if last_card > card_to_beat:
                return False

    return True


def get_available_play_card(card_stack: List[Card], player: Player) -> List[Card]:
    """Returns list of cards in hand available for legal play
    Args:
        card_stack: stack of cards already played
        player: player that is making the play

    Returns: List of legal play cards
    """

    legal_card_idx_to_play = [
        card for card in player.hand if check_play_validity(card_stack, card, player)
    ]

    return legal_card_idx_to_play


class VezimasSubgame:
    """Class of playing the trick/subgame of Vezimas"""

    def __init__(self, main_game: Vezimas):
        self.main_game = main_game

        # creates cycle list starting from player who has its starting player flag set
        _player_to_add = self.main_game.get_starting_player()
        _player_list = []
        for i in range(self.main_game.player_count):
            _player_list.append(_player_to_add)
            _player_to_add = _player_to_add.next_player

        self.player_cycle = MyCycle(_player_list)
        self.card_stack = []

    def pickup_cards(self, player: Player):
        """Method for picking up cards and resetting card stack"""
        player.add_cards(self.card_stack)
        self.card_stack = []

    def start_game(self):
        """Method for starting the trick of Vezimas"""

        for player_turn in self.player_cycle:

            # If card stack is empty play one card
            if not self.card_stack:
                card_to_play_first = card_play_input(
                    player=player_turn,
                    card_stack=self.card_stack,
                    legal_cards_to_play=player_turn.hand,
                    play_no=1,
                    allow_pickup=False,
                )

                player_turn.remove_cards([card_to_play_first])
                self.card_stack.append(card_to_play_first)

            # If card stack is not empty play cards
            else:
                legal_cards_to_play = get_available_play_card(
                    self.card_stack, player_turn
                )
                card_to_beat = card_play_input(
                    player=player_turn,
                    card_stack=self.card_stack,
                    legal_cards_to_play=legal_cards_to_play,
                    play_no=1,
                )

                if card_to_beat:
                    player_turn.remove_cards([card_to_beat])
                    self.card_stack.append(card_to_beat)

                    if player_turn.hand:
                        # If still cards in hand, continue play
                        card_to_play = card_play_input(
                            player=player_turn,
                            card_stack=self.card_stack,
                            legal_cards_to_play=player_turn.hand,
                            play_no=2,
                        )
                        if card_to_play:
                            player_turn.remove_cards([card_to_play])
                            self.card_stack.append(card_to_play)
                        else:
                            # Pickup cards
                            self.pickup_cards(player_turn)
                            player_turn.sort_cards()
                else:
                    # Pickup cards
                    self.pickup_cards(player_turn)
                    player_turn.sort_cards()

            # Remove player from playing trick if he has no more cards and adjust references
            if not player_turn.hand:
                self.player_cycle.remove(player_turn)
                player_turn.previous_player.next_player = player_turn.next_player
                player_turn.next_player.previous_player = player_turn.previous_player
                print(f"{player_turn.name} won")

            # End game when there is only one person left
            if len(self.player_cycle) == 1:
                self.main_game.players[player_turn.name].score += 1
                print(f"{player_turn.name} lost the game")
                return player_turn

            if len(self.player_cycle) == 0:
                print(f"Game was tied")
                break
