from pyminion.models.base import Hand, DiscardPile, Player, Playmat


def test_create_player(deck):
    discard = DiscardPile()
    hand = Hand()
    playmat = Playmat()

    player = Player(deck=deck, discard=discard, hand=hand, playmat=playmat)
    assert len(player.deck) == 10
    assert len(player.discard) == 0
    assert len(player.hand) == 0
    assert len(player.playmat) == 0


def test_draw_deck_to_hand(player: Player):
    drawn_card = player.deck.draw()
    player.hand.add(drawn_card)
    assert len(player.hand) == 1
    assert len(player.deck) == 9


def test_draw_multiple_to_hand(player: Player):
    for i in range(5):
        player.hand.add(player.deck.draw())
    assert len(player.hand) == 5
    assert len(player.deck) == 5
