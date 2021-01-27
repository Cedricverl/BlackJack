from game import *

deck = [Card(4), Card(5), Card(2), Card(6), Card(3), Card(4), Card(6), Card(3), Card(3), Card(1), Card(1), Card(4), Card(1), Card(1)]

bankroll = 100
playhand = Hand([Card(1), Card(6)], 5)
assert (playhand.isSoftTotal())
print(playhand.softSum())
assert (playhand.softSum() == 6)
a = getaction(playhand, 4)
print(a)