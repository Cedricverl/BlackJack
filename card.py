class Card:
    def __init__(self, rank):
        self.ranks = [None, "Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
        self.rank = self.ranks[rank]
        self.value = -1

    def getRank(self):
        return self.rank

    def bjValue(self):
        if self.rank == "Ace":
            self.value = 1
        elif self.rank == "Jack" or self.rank == "Queen" or self.rank == "King":
            self.value = 10
        elif type(self.rank) is int:
            if self.rank > 1 and self.rank < 11:
                self.value = self.ranks[self.rank]
        return self.value

    def __repr__(self):
        return "(%s)" % (self.bjValue())

    def __eq__(self, other):
        if self.bjValue() == other.bjValue():
            return True
        return False


# deck = [Card(rank, suit) for rank in ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"] for suit in ["d","c","h","s"]]
def get_deck():
    return [Card(rank) for rank in range(1, 14) for _ in range(4)]


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
            if sum + 11 + 1*(1-i) > 21:
                sum += 1
            else:
                sum += 11
        return sum
