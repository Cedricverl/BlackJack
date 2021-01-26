import game
from card import *
from hand import *

handslist = []
for i in range(2, 10):
    handslist.append(Hand([Card(1), Card(i)], 5))

for hand in handslist:
    print("HAND: ", hand)
    print([(dealervalue, game.getaction(hand, dealervalue)) for dealervalue in range(1, 11)])
