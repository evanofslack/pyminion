from pyminion.bots.optimized_bot import OptimizedBot
from pyminion.expansions.base import (
    artisan,
    bureaucrat,
    cellar,
    chapel,
    copper,
    duchy,
    estate,
    gold,
    harbinger,
    library,
    militia,
    mine,
    moneylender,
    poacher,
    province,
    remodel,
    sentry,
    silver,
    smithy,
    throne_room,
    vassal,
    village,
    workshop,
)
from pyminion.expansions.intrigue import (
    baron,
    courtier,
    courtyard,
    diplomat,
    ironworks,
    lurker,
    masquerade,
    mill,
    mining_village,
    minion,
    nobles,
    patrol,
    pawn,
    replace,
    secret_passage,
    steward,
    swindler,
    torturer,
    trading_post,
    upgrade,
    wishing_well,
)
from pyminion.core import CardType
from pyminion.game import Game


def test_artisan_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(artisan)
    bot.play(artisan, game)
    assert bot.deck.cards[-1].name == "Silver"


def test_artisan_bot_actions(bot: OptimizedBot, game: Game):
    bot.hand.add(artisan)
    bot.hand.add(village)
    bot.play(artisan, game)
    assert bot.deck.cards[-1].name == "Village"


def test_bureaucrat_bot(bot: OptimizedBot, multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]
    bot.hand.add(bureaucrat)
    opponent = multiplayer_bot_game.players[1]
    victory_cards = [card for card in opponent.hand.cards if CardType.Victory in card.type]
    for card in victory_cards:
        opponent.hand.remove(card)
    opponent.hand.add(duchy)
    bot.play(bureaucrat, multiplayer_bot_game)
    assert opponent.deck.cards[-1].name == "Duchy"


def test_cellar_bot_no_discard(bot: OptimizedBot, game: Game):
    bot.hand.add(cellar)
    bot.play(target_card=cellar, game=game)
    assert len(bot.discard_pile) == 0


def test_cellar_bot_yes_discard(bot: OptimizedBot, game: Game):
    bot.hand.add(cellar)
    bot.hand.add(copper)  # discard me
    bot.hand.add(estate)  # discard me
    bot.hand.add(duchy)  # discard me
    bot.hand.add(silver)
    bot.hand.add(cellar)
    bot.play(target_card=cellar, game=game)
    assert len(bot.discard_pile) == 3


def test_chapel_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(chapel)
    bot.hand.add(estate)
    bot.hand.add(copper)
    bot.play(chapel, game)
    assert len(game.trash) == 2


def test_chapel_bot_no_money(bot: OptimizedBot, game: Game):
    bot.hand.add(chapel)
    for i in range(4):
        bot.hand.add(copper)
    for i in range(7):
        bot.deck.remove(copper)

    bot.play(chapel, game)
    assert len(game.trash) == 1


def test_chapel_bot_late_game(bot: OptimizedBot, game: Game):
    bot.hand.add(chapel)
    for i in range(3):
        bot.hand.add(estate)

    game.supply.gain_card(province)
    bot.play(chapel, game)
    assert len(game.trash) == 0


def test_harbinger_bot_no_topdeck_victory(bot: OptimizedBot, game: Game):
    bot.hand.add(harbinger)
    bot.discard_pile.add(estate)
    bot.discard_pile.add(duchy)
    bot.discard_pile.add(province)
    bot.discard_pile.add(copper)
    bot.play(harbinger, game)
    assert len(bot.discard_pile) == 4


def test_harbinger_bot_topdeck_expensive_card(bot: OptimizedBot, game: Game):
    bot.hand.add(harbinger)
    bot.discard_pile.add(silver)
    bot.discard_pile.add(gold)  # Topdeck me
    bot.discard_pile.add(province)
    bot.play(harbinger, game)
    assert len(bot.discard_pile) == 2
    assert bot.deck.cards[-1].name == "Gold"


def test_library_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(library)
    bot.play(library, game)
    assert len(bot.hand) == 7
    assert len(bot.playmat) == 1
    assert bot.state.actions == 0


def test_library_bot_no_action(bot: OptimizedBot, game: Game):
    bot.hand.add(library)
    bot.deck.add(smithy)
    bot.play(library, game)
    assert len(bot.hand) == 7
    assert len(bot.discard_pile) == 1


def test_library_bot_extra_action(bot: OptimizedBot, game: Game):
    bot.hand.add(library)
    bot.state.actions = 2
    bot.deck.add(smithy)
    bot.play(library, game)
    assert len(bot.hand) == 7
    assert len(bot.discard_pile) == 0


def test_militia_bot_opponent_discards(multiplayer_bot_game: Game):
    player = multiplayer_bot_game.players[0]
    player.hand.add(militia)
    opponent = multiplayer_bot_game.players[1]
    opponent.hand.cards = []
    for i in range(3):
        opponent.hand.add(gold)
    opponent.hand.add(copper)
    opponent.hand.add(estate)
    assert len(opponent.discard_pile) == 0

    player.play(militia, multiplayer_bot_game)
    assert len(opponent.hand) == 3
    assert len(opponent.discard_pile) == 2
    assert copper in opponent.discard_pile.cards
    assert estate in opponent.discard_pile.cards


def test_mine_bot_no_treasure(bot: OptimizedBot, game: Game):
    bot.hand.add(mine)
    bot.play(mine, game)
    assert len(game.trash) == 0


def test_mine_bot_copper(bot: OptimizedBot, game: Game):
    bot.hand.add(mine)
    bot.hand.add(copper)
    bot.play(mine, game)
    assert bot.hand.cards[-1].name == "Silver"


def test_mine_bot_silver(bot: OptimizedBot, game: Game):
    bot.hand.add(mine)
    bot.hand.add(silver)
    bot.play(mine, game)
    assert bot.hand.cards[-1].name == "Gold"


def test_mine_bot_gold(bot: OptimizedBot, game: Game):
    bot.hand.add(mine)
    bot.hand.add(gold)
    bot.play(mine, game)
    assert bot.hand.cards[-1].name == "Gold"


def test_moneylender_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(moneylender)
    bot.hand.add(copper)
    assert len(bot.hand) == 2
    assert len(game.trash) == 0

    bot.hand.cards[0].play(bot, game)
    assert len(bot.hand) == 0
    assert len(bot.playmat) == 1
    assert bot.playmat.cards[0].name == "Moneylender"
    assert bot.state.actions == 0
    assert bot.state.money == 3
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Copper"


def test_poacher_bot_no_empty_pile(bot: OptimizedBot, game: Game):
    bot.hand.add(poacher)
    bot.play(poacher, game)
    assert len(bot.discard_pile) == 0


def test_bot_one_empty_pile(bot: OptimizedBot, game: Game):
    bot.hand.add(poacher)
    bot.hand.add(estate)
    for i in range(5):
        game.supply.gain_card(card=estate)
    assert game.supply.num_empty_piles() == 1
    bot.play(poacher, game)
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[-1].name == "Estate"


def test_bot_one_empty_pile_prioritize_victory(bot: OptimizedBot, game: Game):
    bot.hand.add(poacher)
    bot.hand.add(estate)
    bot.hand.add(copper)
    for i in range(5):
        game.supply.gain_card(card=estate)
    assert game.supply.num_empty_piles() == 1
    bot.play(poacher, game)
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[-1].name == "Estate"


def test_remodel_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(remodel)
    bot.hand.add(copper)
    bot.play(remodel, game)
    assert bot.discard_pile.cards[-1].name == "Estate"


def test_remodel_bot_gold(bot: OptimizedBot, game: Game):
    bot.hand.add(remodel)
    bot.hand.add(gold)
    bot.play(remodel, game)
    assert bot.discard_pile.cards[-1].name == "Province"


def test_sentry_bot_no_response(bot: OptimizedBot, game: Game):
    bot.deck.cards = []
    bot.deck.add(gold)
    bot.deck.add(smithy)
    bot.deck.add(copper)
    bot.hand.add(sentry)
    assert len(bot.discard_pile) == 0
    assert len(game.trash) == 0
    assert bot.deck.cards[1].name == "Smithy"
    assert bot.deck.cards[0].name == "Gold"

    bot.play(sentry, game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 1
    assert len(bot.discard_pile) == 0
    assert len(game.trash) == 0
    assert bot.state.actions == 1

    assert len(bot.deck) == 2
    assert bot.deck.cards[1].name == "Smithy"
    assert bot.deck.cards[0].name == "Gold"


def test_bot_trash_two(bot: OptimizedBot, game: Game):
    bot.deck.cards = []
    bot.deck.add(gold)
    bot.deck.add(copper)
    bot.deck.add(estate)
    bot.deck.add(copper)
    bot.hand.add(sentry)
    assert len(game.trash) == 0

    bot.play(sentry, game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 1
    assert len(bot.discard_pile) == 0
    assert len(game.trash) == 2
    assert len(bot.deck) == 1


def test_bot_discard_two(bot: OptimizedBot, game: Game):
    bot.deck.cards = []
    bot.deck.add(duchy)
    bot.deck.add(duchy)
    bot.deck.add(copper)
    bot.hand.add(sentry)
    assert len(bot.discard_pile) == 0

    bot.play(sentry, game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 1
    assert len(bot.discard_pile) == 2
    assert len(bot.deck) == 0


def test_bot_discard_one_trash_one(bot: OptimizedBot, game: Game):
    bot.deck.cards = []
    bot.deck.add(duchy)
    bot.deck.add(estate)
    bot.deck.add(copper)
    bot.hand.add(sentry)
    assert len(game.trash) == 0
    assert len(bot.discard_pile) == 0

    bot.play(sentry, game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 1
    assert len(bot.discard_pile) == 1
    assert len(game.trash) == 1
    assert len(bot.deck) == 0


def test_throne_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(throne_room)
    bot.hand.add(village)
    bot.hand.add(smithy)
    bot.play(throne_room, game)
    assert len(bot.playmat) == 2
    assert smithy in bot.playmat.cards


def test_vassal_bot(bot: OptimizedBot, game: Game):
    bot.deck.add(village)
    bot.hand.add(vassal)
    bot.play(target_card=vassal, game=game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 2
    assert len(bot.discard_pile) == 0
    assert bot.state.actions == 2
    assert bot.state.money == 2


def test_workshop_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(workshop)
    bot.play(workshop, game)
    assert bot.discard_pile.cards[-1].name == "Silver"


def test_workshop_bot_late_game(bot: OptimizedBot, game: Game):
    bot.hand.add(workshop)
    for i in range(4):
        game.supply.gain_card(province)
    bot.play(workshop, game)
    assert bot.discard_pile.cards[-1].name == "Estate"


def test_baron_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(baron)
    bot.hand.add(estate)
    bot.play(baron, game)
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[-1].name == "Estate"


def test_courtier_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(courtier)
    bot.hand.add(copper)
    bot.hand.add(torturer)
    bot.play(courtier, game)
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[-1].name == "Gold"
    assert bot.state.actions == 1
    assert bot.state.money == 0


def test_courtyard_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(courtyard)
    bot.hand.add(torturer)
    bot.play(courtyard, game)
    assert bot.deck.cards[-1].name == "Torturer"
