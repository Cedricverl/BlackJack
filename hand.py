# from collections import Counter
from card import get_cards_sum
class Hand:
    def __init__(self, cards, bet=0, isdouble=False, surrender=False):
        self.cards = cards
        self.bet = bet
        self.isdouble = isdouble
        self.surrendered = surrender

    def setDouble(self):
        self.isdouble = True
        self.bet = self.bet*2

    def isSurrendered(self):
        return self.surrendered

    def setSurrender(self):
        self.surrendered = True

    def isDouble(self):
        return self.isdouble

    def addCard(self, card):
        self.cards.append(card)

    def split(self):
        return [Hand([self.cards[0]], self.bet), Hand([self.cards[1]], self.bet)]

    def getSum(self):
        return get_cards_sum(self.getCards())
        # return sum([card.bjValue() for card in self.cards])

    def getCards(self):
        return self.cards

    def getBet(self):
        return self.bet

    def takeCard(self):
        return self.cards.pop()

    def __eq__(self, other):  # only used to check for a blackjack hand
        if not(len(self.getCards()) == len(other.getCards()) == 2):
            return False
        return (self.getCards()[0] == other.getCards()[0] and self.getCards()[1] == other.getCards()[1]) or (self.getCards()[0] == other.getCards()[1] and self.getCards()[1] == other.getCards()[0])


    # def __ne__(self, other):
    #     return not self.__eq__(other)

    def __repr__(self):
        return "%s {%s}" % (self.cards, self.bet)

    # def __copy__(self):
    #     return Hand(self.cards.copy(), self.bet, self.isdouble)
    #
    # def __deepcopy__(self):
    #     return Hand(self.cards.copy(), self.bet, self.isdouble)


# def equal_ignore_order(a, b):
#     """ Use only when elements are neither hashable nor sortable! """
#     unmatched = list(b)
#     for element in a:
#         try:
#             unmatched.remove(element)
#         except ValueError:
#             return False
#     return not unmatched

