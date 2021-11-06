from pyminion.models.core import Player, Deck, Card
from pyminion.game import Game
from pyminion.exceptions import InvalidCardPlay


class Bot(Player):
    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "bot",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def exact_play(self, card: Card, game: Game, generic_play: bool = True) -> None:
        try:
            if card.type == "Action":
                card.bot_play(player=self, game=game, generic_play=generic_play)
            elif card.type == "Treasure":
                card.play(player=self, game=game)
        except:
            raise InvalidCardPlay(f"Invalid play, cannot play {card}")
