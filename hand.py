from card import Card, get_cards_sum

"""
    Implementation of playing hand at Blackjack table. Initially consists of 2 cards and a bet.
"""


class Hand:
    def __init__(self, cards, bet=0, isdouble=False, surrender=False):
        self.cards = cards
        self.bet = bet
        self.isdouble = isdouble
        self.surrendered = surrender

    def setDouble(self):
        self.isdouble = True
        self.bet = self.bet * 2

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

    def getCards(self):
        return self.cards

    def getBet(self):
        return self.bet

    def takeCard(self):
        return self.cards.pop()

    def __eq__(self, other):  # only used to check for a blackjack hand
        if not (len(self.getCards()) == len(other.getCards()) == 2):
            return False
        return (self.getCards()[0] == other.getCards()[0] and self.getCards()[1] == other.getCards()[1]) or (
                    self.getCards()[0] == other.getCards()[1] and self.getCards()[1] == other.getCards()[0])

    def containsAce(self):
        return Card(1) in self.getCards()

    def isSoftTotal(self):
        lowsum = sum([card.bjValue() for card in self.getCards()])
        return self.containsAce() and lowsum + 10 <= 21

    def softSum(self):
        return sum([card.bjValue() for card in self.getCards() if card != Card(1)])

    def __repr__(self):
        return "%s(%s){€%s}" % (self.cards, self.getSum(), self.bet)
