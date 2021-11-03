# def test_autoplay_treasures(player: Player):
#     for i in range(3):
#         player.hand.add(estate)
#         player.hand.add(copper)
#         player.hand.add(copper)
#     assert len(player.hand) == 9

#     player.autoplay_treasures()

#     assert len(player.hand) == 3
#     assert len(player.playmat) == 6
#     assert player.state.money == 6


# def test_player_cleanup(player: Player):
#     player.draw(5)
#     assert len(player.hand) == 5
#     assert len(player.discard_pile) == 0
#     assert len(player.playmat) == 0
#     player.autoplay_treasures()
#     assert len(player.playmat) > 0
#     player.cleanup()
#     assert len(player.discard_pile) == 5
#     assert len(player.hand) == 5
#     assert len(player.playmat) == 0
