from pyminion.expansions.base import artisan, base_set, copper, curse, silver, throne_room
from pyminion.expansions.seaside import Sailor, bazaar, fishing_village, seaside_set, sailor
from pyminion.game import Game
import pytest


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([sailor])
def test_sailor_trash(multiplayer_game: Game, monkeypatch):
    responses = ["y", "curse"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]

    human.deck.add(curse)

    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Sailor
    assert human.state.actions == 1
    assert human.state.money == 0
    assert human.playmat_persist_counts[sailor.name] == 1
    assert "Sailor: Trash card" in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)

    human.start_cleanup_phase(multiplayer_game)
    human.end_turn(multiplayer_game)

    human.start_turn(multiplayer_game)

    assert len(responses) == 0
    assert human.state.money == 2
    assert len(human.hand) == 4
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Curse"
    assert human.playmat_persist_counts[sailor.name] == 0
    assert "Sailor: Trash card" not in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([sailor])
def test_sailor_no_trash(multiplayer_game: Game, monkeypatch):
    responses = ["n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]

    human.deck.add(curse)

    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Sailor
    assert human.state.actions == 1
    assert human.state.money == 0
    assert human.playmat_persist_counts[sailor.name] == 1
    assert "Sailor: Trash card" in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)

    human.start_cleanup_phase(multiplayer_game)
    human.end_turn(multiplayer_game)

    human.start_turn(multiplayer_game)

    assert len(responses) == 0
    assert human.state.money == 2
    assert len(human.hand) == 5
    assert len(multiplayer_game.trash) == 0
    assert human.playmat_persist_counts[sailor.name] == 0
    assert "Sailor: Trash card" not in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([sailor])
def test_sailor_one_card_trash(multiplayer_game: Game, monkeypatch):
    responses = ["y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]

    while len(human.hand) > 0:
        human.hand.cards.pop()
    while len(human.deck) > 0:
        human.deck.cards.pop()
    while len(human.discard_pile) > 0:
        human.discard_pile.cards.pop()

    human.deck.add(curse)

    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Sailor
    assert human.state.actions == 1
    assert human.state.money == 0
    assert human.playmat_persist_counts[sailor.name] == 1
    assert "Sailor: Trash card" in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)

    human.start_cleanup_phase(multiplayer_game)
    human.end_turn(multiplayer_game)

    human.start_turn(multiplayer_game)

    assert len(responses) == 0
    assert human.state.money == 2
    assert len(human.hand) == 0
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Curse"
    assert human.playmat_persist_counts[sailor.name] == 0
    assert "Sailor: Trash card" not in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([bazaar, fishing_village, sailor])
def test_sailor_play(multiplayer_game: Game, monkeypatch):
    responses = ["y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]
    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)

    # ensure gaining a non-duration card will not be played
    human.gain(bazaar, multiplayer_game)
    assert len(responses) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1

    # gain a duration card and play it
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 0
    assert len(human.playmat) == 2
    assert human.playmat.cards[0].name == "Sailor"
    assert human.playmat.cards[1].name == "Fishing Village"
    assert len(human.discard_pile) == 1
    assert human.state.actions == 3
    assert human.state.money == 1

    # ensure gaining another duration card will not be played
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 0
    assert len(human.playmat) == 2
    assert len(human.discard_pile) == 2


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([bazaar, fishing_village, sailor])
def test_two_sailors_play(multiplayer_game: Game, monkeypatch):
    responses = ["y", "y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]
    human.hand.add(sailor)
    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)
    human.play(sailor, multiplayer_game)

    # ensure gaining a non-duration card will not be played
    human.gain(bazaar, multiplayer_game)
    assert len(responses) == 2
    assert len(human.playmat) == 2
    assert len(human.discard_pile) == 1

    # gain a duration card and play it
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 1
    assert len(human.playmat) == 3
    assert human.playmat.cards[0].name == "Sailor"
    assert human.playmat.cards[1].name == "Sailor"
    assert human.playmat.cards[2].name == "Fishing Village"
    assert len(human.discard_pile) == 1
    assert human.state.actions == 3
    assert human.state.money == 1

    # gain a 2nd duration card and play it
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 0
    assert len(human.playmat) == 4
    assert human.playmat.cards[0].name == "Sailor"
    assert human.playmat.cards[1].name == "Sailor"
    assert human.playmat.cards[2].name == "Fishing Village"
    assert human.playmat.cards[3].name == "Fishing Village"
    assert len(human.discard_pile) == 1
    assert human.state.actions == 5
    assert human.state.money == 2

    # ensure gaining a 3rd duration card will not be played
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 0
    assert len(human.playmat) == 4
    assert len(human.discard_pile) == 2


@pytest.mark.expansions([base_set, seaside_set])
@pytest.mark.kingdom_cards([artisan, fishing_village, sailor])
def test_sailor_play_gain_deck(multiplayer_game: Game, monkeypatch):
    responses = ["Fishing Village", "y", "Silver"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]
    human.hand.add(silver)
    human.hand.add(sailor)
    human.hand.add(artisan)

    human.play(sailor, multiplayer_game)

    # play artisan to gain a duration card to player's hand, then play it with sailor
    human.play(artisan, multiplayer_game)

    # gain a duration card and play it
    assert len(responses) == 0
    assert len(human.playmat) == 3
    assert human.playmat.cards[0].name == "Sailor"
    assert human.playmat.cards[1].name == "Artisan"
    assert human.playmat.cards[2].name == "Fishing Village"
    assert len(human.discard_pile) == 0
    assert human.deck.cards[-1].name == "Silver"
    assert human.state.actions == 2
    assert human.state.money == 1



@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([fishing_village, sailor])
def test_sailor_no_play_next_turn(multiplayer_game: Game, monkeypatch):
    # don't trash a card
    responses = ["n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]
    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)

    human.start_cleanup_phase(multiplayer_game)
    human.end_turn(multiplayer_game)
    human.start_turn(multiplayer_game)
    assert len(responses) == 0

    # ensure gaining a duration card on the next turn will not be played
    human.gain(fishing_village, multiplayer_game)
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Sailor"
    assert "Fishing Village" in (c.name for c in human.discard_pile)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([fishing_village, sailor])
def test_sailor_no_play(multiplayer_game: Game, monkeypatch):
    responses = ["n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]
    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)

    # ensure gained duration card will not be played
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Sailor"
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Fishing Village"


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([fishing_village, sailor])
def test_sailor_throne_room(multiplayer_game: Game, monkeypatch):
    responses = ["sailor", "y", "y", "y", "curse", "y", "copper"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]
    human.deck.add(curse)
    human.deck.add(copper)
    human.deck.add(silver)
    human.deck.add(silver)
    human.deck.add(silver)
    human.hand.add(throne_room)
    human.hand.add(sailor)

    human.play(throne_room, multiplayer_game)
    assert len(responses) == 6
    assert len(human.playmat) == 2
    assert set(c.name for c in human.playmat) == {"Throne Room", "Sailor"}
    assert human.state.actions == 2

    # ensure gained duration card will be played
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 5
    assert len(human.playmat) == 3
    assert sum(1 for c in human.playmat if c.name == "Fishing Village") == 1
    assert len(human.discard_pile) == 0

    # ensure 2nd gained duration card will be played
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 4
    assert len(human.playmat) == 4
    assert sum(1 for c in human.playmat if c.name == "Fishing Village") == 2
    assert len(human.discard_pile) == 0

    human.start_cleanup_phase(multiplayer_game)
    human.end_turn(multiplayer_game)

    assert len(human.hand) == 5
    assert len(multiplayer_game.trash) == 0

    human.start_turn(multiplayer_game)

    assert len(human.hand) == 3
    assert set(c.name for c in human.hand) == {"Silver"}
    assert len(multiplayer_game.trash) == 2
    assert set(c.name for c in multiplayer_game.trash) == {"Copper", "Curse"}
