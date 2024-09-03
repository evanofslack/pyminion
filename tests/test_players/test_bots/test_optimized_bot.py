from pyminion.bots.optimized_bot import OptimizedBot
from pyminion.core import CardType, DeckCounter
from pyminion.expansions.base import (
    Smithy,
    artisan,
    bandit,
    base_set,
    bureaucrat,
    cellar,
    chapel,
    copper,
    curse,
    duchy,
    estate,
    gold,
    harbinger,
    library,
    militia,
    mine,
    moat,
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
    witch,
    workshop,
)
from pyminion.expansions.intrigue import (
    baron,
    courtier,
    courtyard,
    diplomat,
    intrigue_set,
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
    shanty_town,
    steward,
    swindler,
    torturer,
    trading_post,
    upgrade,
    wishing_well,
)
from pyminion.expansions.seaside import (
    blockade,
    fishing_village,
    haven,
    island,
    lookout,
    native_village,
    pirate,
    sailor,
    salvager,
    sea_witch,
    seaside_set,
    smugglers,
    tide_pools,
    treasury,
    warehouse,
)
from pyminion.expansions.alchemy import (
    alchemist,
    alchemy_set,
    apothecary,
    apprentice,
    golem,
    herbalist,
    potion,
    scrying_pool,
    transmute,
    university,
)
from pyminion.game import Game
import pytest


def test_artisan_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(artisan)
    bot.play(artisan, game)
    assert bot.deck.cards[-1].name == "Silver"


def test_artisan_bot_actions(bot: OptimizedBot, game: Game):
    bot.hand.add(artisan)
    bot.hand.add(village)
    bot.play(artisan, game)
    assert bot.deck.cards[-1].name == "Village"


def test_bureaucrat_bot(multiplayer_bot_game: Game):
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


@pytest.mark.expansions([base_set])
@pytest.mark.kingdom_cards([moat])
def test_moat(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    p1.hand.add(moat)
    p2.hand.add(militia)

    assert len(p1.hand) == 6

    p2.play(militia, multiplayer_bot_game)

    assert len(p1.hand) == 6


def test_moneylender_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(moneylender)
    bot.hand.add(copper)
    assert len(bot.hand) == 2
    assert len(game.trash) == 0

    bot.play(moneylender, game)
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
    bot.hand.add(copper)
    bot.play(remodel, game)
    assert bot.discard_pile.cards[-1].name == "Estate"


def test_remodel_bot_gold(bot: OptimizedBot, game: Game):
    bot.hand.add(remodel)
    bot.hand.add(gold)
    bot.hand.add(gold)
    bot.play(remodel, game)
    assert bot.discard_pile.cards[-1].name == "Province"


def test_bandit_bot(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    p1.hand.add(bandit)

    p2.deck.add(gold)
    p2.deck.add(silver)

    p1.play(bandit, multiplayer_bot_game)

    assert p2.discard_pile.cards[-1].name == "Gold"
    assert multiplayer_bot_game.trash.cards[0].name == "Silver"


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


@pytest.mark.expansions([intrigue_set])
@pytest.mark.kingdom_cards([diplomat])
def test_diplomat_bot(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    while len(p1.hand) > 0:
        p1.hand.remove(p1.hand.cards[0])
    p1.hand.add(copper)
    p1.hand.add(estate)
    p1.hand.add(estate)
    p1.hand.add(estate)
    p1.deck.add(diplomat)
    p1.draw()
    assert len(p1.hand) == 5

    p2.hand.add(witch)
    p2.play(witch, multiplayer_bot_game)

    assert len(p1.hand) == 4
    assert len(p1.discard_pile) == 4
    for i in range(3):
        assert p1.discard_pile.cards[i].name == "Estate"
    assert p1.discard_pile.cards[3].name == "Curse" # from witch


def test_ironworks_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(ironworks)
    bot.play(ironworks, game)
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[-1].name == "Silver"


def test_lurker_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(lurker)
    bot.hand.add(lurker)
    assert len(game.trash) == 0
    assert len(bot.discard_pile) == 0

    bot.play(lurker, game)
    assert len(game.trash) == 1
    card = game.trash.cards[0]
    assert CardType.Action in card.type
    assert len(bot.discard_pile) == 0

    bot.play(lurker, game)
    assert len(game.trash) == 0
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[0].name == card.name


def test_masquerade_bot(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    p1.hand.add(masquerade)
    p1.hand.add(estate)

    p2.hand.add(curse)
    p2_estate_count_before = sum(1 for c in p2.hand.cards if c.name == "Estate")

    p1.play(masquerade, multiplayer_bot_game)

    assert len(multiplayer_bot_game.trash) == 1
    assert multiplayer_bot_game.trash.cards[0].name == "Curse"

    p2_estate_count_after = sum(1 for c in p2.hand.cards if c.name == "Estate")
    assert p2_estate_count_after == p2_estate_count_before + 1


def test_mill_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(mill)
    bot.hand.add(estate)
    bot.hand.add(copper)
    bot.deck.add(copper) # playing mill will draw this copper
    bot.play(mill, game)
    assert len(bot.discard_pile) == 2
    assert set(c.name for c in bot.discard_pile.cards) == {"Copper", "Estate"}
    assert bot.state.money == 2


def test_mining_village_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(mining_village)
    bot.hand.add(mining_village)
    bot.play(mining_village, game)
    assert len(game.trash) == 0

    province_pile = game.supply.get_pile("Province")
    while len(province_pile) >= 3:
        province_pile.remove(province)

    bot.play(mining_village, game)
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Mining Village"


def test_minion_bot(multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]
    while len(bot.hand) > 0:
        bot.hand.cards.pop()

    bot.hand.add(minion)
    bot.hand.add(minion)
    bot.hand.add(copper)
    bot.play(minion, multiplayer_bot_game)
    assert len(bot.discard_pile) == 0
    assert bot.state.money == 2

    bot.play(minion, multiplayer_bot_game)
    assert len(bot.discard_pile) == 1
    assert bot.state.money == 2


def test_nobles_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(nobles)
    bot.hand.add(nobles)
    bot.play(nobles, game)
    assert len(bot.hand) == 1
    assert bot.state.actions == 2

    bot.play(nobles, game)
    assert len(bot.hand) == 3
    assert bot.state.actions == 1


def test_patrol_bot(bot: OptimizedBot, game: Game):
    bot.deck.add(patrol)
    bot.deck.add(silver)
    bot.deck.add(gold)
    bot.deck.add(copper)
    for _ in range(3):
        bot.deck.add(copper)

    bot.hand.add(patrol)
    bot.play(patrol, game)
    assert len(bot.deck) >= 4
    assert bot.deck.cards[-1].name == "Gold"
    assert bot.deck.cards[-2].name == "Patrol"
    assert bot.deck.cards[-3].name == "Silver"
    assert bot.deck.cards[-4].name == "Copper"


def test_pawn_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(pawn)
    bot.hand.add(pawn)
    bot.hand.add(copper)
    bot.play(pawn, game)
    assert len(bot.hand) == 2
    assert bot.state.actions == 1
    assert bot.state.buys == 1
    assert bot.state.money == 1

    bot.play(pawn, game)
    assert len(bot.hand) == 2
    assert bot.state.actions == 0
    assert bot.state.buys == 1
    assert bot.state.money == 2


def test_pawn_bot_buy(bot: OptimizedBot, game: Game):
    bot.hand.add(pawn)
    for _ in range(3):
        bot.hand.add(gold)
    bot.play(pawn, game)
    assert len(bot.hand) == 4
    assert bot.state.actions == 0
    assert bot.state.buys == 2
    assert bot.state.money == 0


def test_replace_bot(multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]
    while len(bot.hand) > 0:
        bot.hand.cards.pop()

    province_pile = multiplayer_bot_game.supply.get_pile("Province")
    while len(province_pile) >= 3:
        province_pile.remove(province_pile.cards[0])

    bot.hand.add(replace)
    bot.hand.add(copper)
    bot.play(replace, multiplayer_bot_game)
    assert len(bot.hand) == 0
    assert len(multiplayer_bot_game.trash) == 1
    assert multiplayer_bot_game.trash.cards[0].name == "Copper"
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[0].name == "Estate"


def test_replace_bot_trash_gold(multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]
    while len(bot.hand) > 0:
        bot.hand.cards.pop()

    province_pile = multiplayer_bot_game.supply.get_pile("Province")
    while len(province_pile) >= 3:
        province_pile.remove(province_pile.cards[0])

    bot.hand.add(replace)
    bot.hand.add(gold)
    bot.play(replace, multiplayer_bot_game)
    assert len(bot.hand) == 0
    assert len(multiplayer_bot_game.trash) == 1
    assert multiplayer_bot_game.trash.cards[0].name == "Gold"
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[0].name == "Province"


def test_replace_bot_trash_curse(multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]
    while len(bot.hand) > 0:
        bot.hand.cards.pop()

    province_pile = multiplayer_bot_game.supply.get_pile("Province")
    while len(province_pile) >= 3:
        province_pile.remove(province_pile.cards[0])

    bot.hand.add(replace)
    bot.hand.add(curse)
    bot.play(replace, multiplayer_bot_game)
    assert len(bot.hand) == 0
    assert len(multiplayer_bot_game.trash) == 1
    assert multiplayer_bot_game.trash.cards[0].name == "Curse"
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[0].name == "Estate"


def test_secret_passage_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(secret_passage)
    bot.deck.add(silver)
    bot.deck.add(silver)
    bot.play(secret_passage, game)
    assert len(bot.hand) == 1
    assert bot.hand.cards[0].name == "Silver"
    assert len(bot.deck) >= 1
    assert bot.deck.cards[-1].name == "Silver"


def test_steward_bot_cards(bot: OptimizedBot, game: Game):
    bot.hand.add(steward)
    bot.hand.add(shanty_town)
    bot.play(shanty_town, game)
    bot.play(steward, game)
    assert len(bot.hand) == 2
    assert len(game.trash) == 0
    assert bot.state.money == 0


def test_steward_bot_trash(bot: OptimizedBot, game: Game):
    bot.hand.add(steward)
    bot.hand.add(copper)
    bot.hand.add(copper)
    bot.hand.add(silver)
    bot.play(steward, game)
    assert len(bot.hand) == 1
    assert bot.hand.cards[0].name == "Silver"
    assert len(game.trash) == 2
    assert game.trash.cards[0].name == "Copper"
    assert game.trash.cards[1].name == "Copper"
    assert bot.state.money == 0


def test_steward_bot_money(bot: OptimizedBot, game: Game):
    bot.hand.add(steward)
    bot.play(steward, game)
    assert len(bot.hand) == 0
    assert len(game.trash) == 0
    assert bot.state.money == 2


def test_swindler_bot(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    p1.hand.add(swindler)
    p2.deck.add(copper)
    p1.play(swindler, multiplayer_bot_game)
    assert len(multiplayer_bot_game.trash) == 1
    assert multiplayer_bot_game.trash.cards[0].name == "Copper"
    assert len(p2.discard_pile) == 1
    assert p2.discard_pile.cards[0].name == "Curse"


def test_torturer_bot_no_curses(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    curses_pile = multiplayer_bot_game.supply.get_pile("Curse")
    while len(curses_pile) > 0:
        curses_pile.remove(curses_pile.cards[0])

    p1.hand.add(torturer)
    p1.play(torturer, multiplayer_bot_game)
    assert len(p2.hand) == 5
    assert len(p2.discard_pile) == 0


def test_torturer_bot_no_cards(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    while len(p2.hand) > 0:
        p2.hand.remove(p2.hand.cards[0])

    p1.hand.add(torturer)
    p1.play(torturer, multiplayer_bot_game)
    assert len(p2.hand) == 0
    assert len(p2.discard_pile) == 0


def test_torturer_bot_discard(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    while len(p2.hand) > 0:
        p2.hand.remove(p2.hand.cards[0])
    for _ in range(3):
        p2.hand.add(copper)
    for _ in range(2):
        p2.hand.add(estate)

    p1.hand.add(torturer)
    p1.play(torturer, multiplayer_bot_game)
    assert len(p2.hand) == 3
    for i in range(3):
        assert p2.hand.cards[i].name == "Copper"
    assert len(p2.discard_pile) == 2
    for i in range(2):
        assert p2.discard_pile.cards[i].name == "Estate"


def test_torturer_bot_gain_curse(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    while len(p2.hand) > 0:
        p2.hand.remove(p2.hand.cards[0])
    for _ in range(3):
        p2.hand.add(copper)

    p1.hand.add(torturer)
    p1.play(torturer, multiplayer_bot_game)
    assert len(p2.hand) == 4
    counter = DeckCounter(p2.hand.cards)
    assert counter[copper] == 3
    assert counter[curse] == 1
    assert len(p2.discard_pile) == 0


def test_trading_post_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(trading_post)
    bot.hand.add(silver)
    bot.hand.add(estate)
    bot.hand.add(copper)
    bot.hand.add(curse)

    bot.play(trading_post, game)
    hand_counter = DeckCounter(bot.hand.cards)
    assert sum(hand_counter.values()) == 3
    assert hand_counter[silver] == 2
    assert hand_counter[copper] == 1
    trash_counter = DeckCounter(game.trash.cards)
    assert sum(trash_counter.values()) == 2
    assert trash_counter[estate] == 1
    assert trash_counter[curse] == 1


def test_upgrade_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(upgrade)
    bot.deck.add(estate)

    bot.play(upgrade, game)
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[0].get_cost(bot, game) == 3


def test_wishing_well_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(wishing_well)
    bot.deck.add(copper)
    bot.deck.add(copper)

    bot.play(wishing_well, game)
    assert len(bot.hand) == 2
    assert bot.hand.cards[0].name == "Copper"
    assert bot.hand.cards[1].name == "Copper"


def test_blockade_bot(multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]

    bot.hand.add(blockade)
    bot.play(blockade, multiplayer_bot_game)
    assert len(bot.set_aside) == 1
    assert bot.set_aside.cards[-1].name == "Silver"


def test_haven_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(haven)
    bot.hand.add(smithy)
    bot.hand.add(smithy)

    bot.play(haven, game)
    assert len(bot.set_aside) == 1
    assert type(bot.set_aside.cards[0]) is Smithy


def test_island_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(island)
    bot.hand.add(estate)
    bot.hand.add(copper)
    bot.hand.add(curse)
    bot.hand.add(haven)

    bot.play(island, game)
    mat = bot.get_mat("Island")
    assert len(mat) == 2
    mat_names = set(card.name for card in mat)
    assert "Island" in mat_names
    assert "Estate" in mat_names


def test_lookout_bot(bot: OptimizedBot, game: Game):
    bot.deck.add(silver)
    bot.deck.add(curse)
    bot.deck.add(estate)

    bot.hand.add(lookout)

    bot.play(lookout, game)
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Curse"
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[0].name == "Estate"
    assert len(bot.deck) >= 1
    assert bot.deck.cards[-1].name == "Silver"


def test_native_village_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(native_village)
    bot.hand.add(native_village)
    bot.hand.add(native_village)

    bot.play(native_village, game)
    mat = bot.get_mat("Native Village")
    assert len(mat) == 1

    bot.play(native_village, game)
    assert len(mat) == 2

    bot.play(native_village, game)
    assert len(mat) == 0


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([pirate])
def test_pirate_bot(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    p1.hand.add(pirate)

    p2.gain(silver, multiplayer_bot_game)
    assert len(p1.playmat) == 1
    assert p1.playmat.cards[0].name == "Pirate"

    p2.start_cleanup_phase(multiplayer_bot_game)
    p2.end_turn(multiplayer_bot_game)

    p1.start_turn(multiplayer_bot_game)
    assert len(p1.hand) == 6
    assert "Gold" in (c.name for c in p1.hand)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([sailor, fishing_village])
def test_sailor_bot(multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]

    bot.deck.add(curse)
    for _ in range(4):
        bot.deck.add(copper)

    bot.hand.add(sailor)

    bot.play(sailor, multiplayer_bot_game)

    bot.gain(fishing_village, multiplayer_bot_game)

    assert len(bot.playmat) == 2
    assert bot.playmat.cards[0].name == "Sailor"
    assert bot.playmat.cards[1].name == "Fishing Village"

    bot.start_cleanup_phase(multiplayer_bot_game)
    bot.end_turn(multiplayer_bot_game)
    bot.start_turn(multiplayer_bot_game)

    assert len(bot.hand) == 4
    assert len(multiplayer_bot_game.trash) == 1
    assert multiplayer_bot_game.trash.cards[0].name == "Curse"


def test_salvager_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(salvager)
    bot.hand.add(estate)
    bot.hand.add(silver)

    bot.play(salvager, game)
    assert bot.state.money == 2
    assert len(bot.hand) == 1
    assert bot.hand.cards[0].name == "Silver"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Estate"


def test_sea_witch_bot(multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]

    bot.deck.add(silver)
    bot.deck.add(silver)
    bot.deck.add(silver)
    bot.deck.add(silver)
    bot.deck.add(silver)
    bot.deck.add(copper)
    bot.deck.add(estate)
    bot.deck.add(silver)
    bot.deck.add(silver)

    bot.hand.add(sea_witch)

    bot.play(sea_witch, multiplayer_bot_game)

    bot.start_cleanup_phase(multiplayer_bot_game)
    counter = DeckCounter(bot.hand.cards)
    assert counter[silver] == 3
    assert counter[copper] == 1
    assert counter[estate] == 1

    bot.start_turn(multiplayer_bot_game)
    counter = DeckCounter(bot.hand.cards)
    assert counter[silver] == 5
    assert counter[copper] == 0
    assert counter[estate] == 0


def test_smugglers_bot(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    p1.start_turn(multiplayer_bot_game)
    p1.gain(silver, multiplayer_bot_game)
    p1.gain(gold, multiplayer_bot_game)
    p1.end_turn(multiplayer_bot_game)

    p2.start_turn(multiplayer_bot_game)
    p2.hand.add(smugglers)
    p2.play(smugglers, multiplayer_bot_game)
    assert len(p2.discard_pile) == 1
    assert p2.discard_pile.cards[0].name == "Gold"


def test_tide_pools_bot(bot: OptimizedBot, game: Game):
    bot.deck.add(silver)
    bot.deck.add(silver)
    bot.deck.add(silver)
    bot.deck.add(copper)
    bot.deck.add(estate)
    bot.deck.add(silver)
    bot.deck.add(silver)
    bot.deck.add(silver)

    bot.hand.add(tide_pools)

    bot.play(tide_pools, game)

    bot.start_cleanup_phase(game)
    counter = DeckCounter(bot.hand.cards)
    assert counter[silver] == 3
    assert counter[copper] == 1
    assert counter[estate] == 1

    bot.start_turn(game)
    counter = DeckCounter(bot.hand.cards)
    assert counter[silver] == 3
    assert counter[copper] == 0
    assert counter[estate] == 0


def test_treasury_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(treasury)

    bot.play(treasury, game)

    game.effect_registry.on_buy_phase_end(bot, game)
    assert bot.deck.cards[-1].name == "Treasury"


def test_warehouse_bot(bot: OptimizedBot, game: Game):
    bot.deck.add(estate)
    bot.deck.add(copper)
    bot.deck.add(gold)

    bot.hand.add(duchy)
    bot.hand.add(silver)
    bot.hand.add(warehouse)

    bot.play(warehouse, game)

    counter = DeckCounter(bot.hand)
    assert counter[silver] == 1
    assert counter[gold] == 1

    counter = DeckCounter(bot.discard_pile)
    assert counter[estate] == 1
    assert counter[duchy] == 1
    assert counter[copper] == 1


def test_alchemist_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(alchemist)
    bot.hand.add(potion)

    bot.play(alchemist, game)
    bot.play(potion, game)

    bot.start_cleanup_phase(game)
    assert "Alchemist" in [card.name for card in bot.hand]


def test_apothecary_bot(bot: OptimizedBot, game: Game):
    bot.deck.add(silver)
    bot.deck.add(gold)
    bot.deck.add(smithy)
    bot.deck.add(patrol)
    bot.deck.add(estate)

    bot.hand.add(apothecary)
    bot.play(apothecary, game)
    assert len(bot.deck) >= 4
    assert bot.deck.cards[-1].name == "Gold"
    assert bot.deck.cards[-2].name == "Patrol"
    assert bot.deck.cards[-3].name == "Smithy"
    assert bot.deck.cards[-4].name == "Silver"


def test_apprentice_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(apprentice)
    bot.hand.add(copper)
    bot.hand.add(estate)

    bot.play(apprentice, game)
    assert len(bot.hand) == 3
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Estate"


def test_golem_bot(bot: OptimizedBot, game: Game):
    bot.deck.add(chapel)
    bot.deck.add(mill)

    bot.hand.add(golem)
    bot.play(golem, game)

    assert len(bot.playmat) == 3
    assert sorted(card.name for card in bot.playmat) == ["Chapel", "Golem", "Mill"]


@pytest.mark.expansions([alchemy_set])
@pytest.mark.kingdom_cards([herbalist])
def test_herbalist_bot(multiplayer_bot_game: Game):
    bot = multiplayer_bot_game.players[0]

    for _ in range(5):
        bot.deck.add(estate)

    bot.hand.add(herbalist)
    bot.hand.add(copper)
    bot.hand.add(gold)

    bot.play(herbalist, multiplayer_bot_game)
    bot.play(copper, multiplayer_bot_game)
    bot.play(gold, multiplayer_bot_game)

    bot.start_cleanup_phase(multiplayer_bot_game)

    assert "Gold" in (card.name for card in bot.hand)
    assert "Copper" not in (card.name for card in bot.hand)


def test_scrying_pool_bot(multiplayer_bot_game: Game):
    p1 = multiplayer_bot_game.players[0]
    p2 = multiplayer_bot_game.players[1]

    p1.deck.add(duchy)
    p1.hand.add(scrying_pool)

    p2.deck.add(duchy)

    p1.play(scrying_pool, multiplayer_bot_game)

    assert p1.discard_pile.cards[-1].name == "Duchy"

    assert p2.deck.cards[-1].name == "Duchy"


def test_transmute_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(transmute)
    bot.hand.add(estate)
    bot.hand.add(silver)

    bot.play(transmute, game)
    assert len(bot.hand) == 1
    assert bot.hand.cards[0].name == "Silver"
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[0].name == "Gold"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Estate"


def test_university_bot(bot: OptimizedBot, game: Game):
    bot.hand.add(university)

    bot.play(university, game)
    assert len(bot.discard_pile) == 1
    assert CardType.Action in bot.discard_pile.cards[0].type
