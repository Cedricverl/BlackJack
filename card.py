"""
    Implementation for playing cards. Blackjack only cares about the rank and not the suit of a card.
    Ace represents a 1 or an 11
    Numbers represent their corresponding value
    Jack, Queen, King represent a 10
"""
from random import shuffle


class Card:
    def __init__(self, rank):
        self.rank = rank  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.value = -1

    def getCount(self):
        if self.rank in (1, 10, 11, 12, 13):
            return -1
        if self.rank <= 6:
            return +1
        return 0

    def getRank(self):
        return self.rank

    def bjValue(self):
        if self.rank >= 10:
            return 10
        return self.rank

    def __repr__(self):
        return "(%s)" % (self.bjValue())

    def __eq__(self, other):
        return self.bjValue() == other.bjValue()


def get_deck(shuffled, amount):
    deck = [Card(rank) for rank in range(1, 14) for _ in range(4)] * amount
    if shuffled:
        shuffle(deck)
    return deck


def get_cards_sum(cards):
    sum = 0
    aces = 0
    for card in cards:
        if card.bjValue() != 1:
            sum += card.bjValue()
        else:
            aces += 1
    if sum == 10 and aces == 1:
        return 21
    else:
        for i in range(aces):
            if sum + 11 + 1 * (1 - i) > 21:
                sum += 1
            else:
                sum += 11
        return sum
