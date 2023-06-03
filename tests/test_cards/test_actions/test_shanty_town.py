from pyminion.expansions.base import copper, estate, smithy
from pyminion.expansions.intrigue import shanty_town
from pyminion.game import Game
from pyminion.player import Player


def test_shanty_town_empty_hand(player: Player, game: Game):
    player.hand.add(shanty_town)

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert player.state.actions == 2


def test_shanty_town_no_actions(player: Player, game: Game):
    player.hand.add(shanty_town)
    player.hand.add(copper)
    player.hand.add(estate)

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 4
    assert len(player.playmat) == 1
    assert player.state.actions == 2


def test_shanty_town_other_actions(player: Player, game: Game):
    player.hand.add(shanty_town)
    player.hand.add(copper)
    player.hand.add(smithy)

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert player.state.actions == 2
