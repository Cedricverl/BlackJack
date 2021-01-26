class Hand:
    def __init__(self, cards, bet, isdouble = False, surrender = False):
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
        sum = 0
        aces = 0
        for card in self.cards:
            if card.bjValue() != 1:
                sum += card.bjValue()
            else:
                aces += 1
        for i in range(aces):
            if sum + 11 > 21:
                sum += 1
            else:
                sum += 11
        return sum
        # return sum([card.bjValue() for card in self.cards])

    def getCards(self):
        return self.cards

    def getBet(self):
        return self.bet

    def takeCard(self):
        return self.cards.pop()

    def __repr__(self):
        return "%s {%s}" % (self.cards, self.bet)

    def __eq__(self, other):
        if len(self.getCards()) != len(other.getCards()):
            return False
        return all([card in other.getCards() for card in self.getCards()])


    # def __copy__(self):
    #     return Hand(self.cards.copy(), self.bet, self.isdouble)
    #
    # def __deepcopy__(self):
    #     return Hand(self.cards.copy(), self.bet, self.isdouble)



