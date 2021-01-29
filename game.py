import os
import sys
from math import sqrt

from numpy import mean, var

from card import *
from hand import Hand


class Game:
    def __init__(self, bankroll, unit, blockstdout):
        self.bankroll = bankroll
        self.unit = unit
        self.rc = 0
        self.deck = get_deck(True, 8)
        self.DAS = True
        self.bet = 0
        sys.stdout = open(os.devnull, 'w') if blockstdout else sys.__stdout__  # block printing statements

    def getBet(self):
        if self.rc == 1:
            return 1*self.unit
        elif self.rc == 2:
            return 2*self.unit
        elif self.rc == 3:
            return 4*self.unit
        elif self.rc >= 4:
            return 8*self.unit
        return 0

    def takeCard(self):
        card = self.deck.pop(0)
        self.rc += card.getCount()
        return card

    def getAction(self, hand, dealervalue):
        # if(len(hand.getCards()) == 2 and Card(1) not in hand.getCards() and (hand.getSum() == 16 and dealervalue in
        # [9, 10, 1] or hand.getSum() == 15 and dealervalue == 10)): return "surrender"
        if hand.getCards()[0] == hand.getCards()[1]:  # pair splitting
            cardvalue = hand.getCards()[0].bjValue()
            if cardvalue == 1 or cardvalue == 8:
                return "split"
            elif (cardvalue == 9 and dealervalue in [2, 3, 4, 5, 6, 8, 9]) or (cardvalue == 7 and 1 < dealervalue < 8) or (
                    cardvalue == 6 and 2 < dealervalue < 7) or (2 <= cardvalue <= 3 and 4 <= dealervalue <= 7):
                return "split"
            elif (cardvalue == 6 and dealervalue == 2) or (1 < cardvalue < 4 and 1 < dealervalue < 4) or (
                    cardvalue == 4 and 4 < dealervalue < 7):
                if self.DAS:
                    return "split"  # if DAS is offered, otherwise don't split

        if hand.isSoftTotal():  # soft totals
            othercard = hand.softSum()
            if (othercard >= 9) or (othercard == 8 and dealervalue != 6) or (othercard == 7 and 6 < dealervalue < 9):
                return "stand"
            if (1 < othercard < 7 and 4 < dealervalue < 7) or (3 < othercard < 7 and dealervalue == 4) or (
                    othercard == 6 and dealervalue == 3):
                if len(hand.getCards()) == 2:
                    return "double"  # if allowed, otherwise hit
                else:
                    return "hit"
            if (othercard == 8 and dealervalue == 6) or (othercard == 7 and 1 < dealervalue < 7):
                if len(hand.getCards()) == 2:
                    return "double"  # if allowed, otherwise stand
                else:
                    return "stand"
            else:
                return "hit"

        if (hand.getSum() == 10 and 1 < dealervalue <= 9) or hand.getSum() == 11 or (
                hand.getSum() == 9 and 2 < dealervalue < 7):  # hard totals
            if len(hand.getCards()) == 2:
                return "double"
            else:
                return "hit"
        elif (hand.getSum() >= 13 and 1 < dealervalue < 7) or (hand.getSum() == 12 and 3 < dealervalue < 7) or (
                hand.getSum() >= 17):
            return "stand"
        else:
            return "hit"

    def playHand(self, hand, dealercards):
        stand = False
        while not stand and hand.getSum() <= 21:
            action = self.getAction(hand, dealercards[0].bjValue())
            # print(hand)
            if action == "hit":
                # print("hit")
                hand.addCard(self.takeCard())
            elif action == "stand":
                # print("stand")
                return [hand]
            elif action == "double":
                # print("double")
                hand.addCard(self.takeCard())
                hand.setDouble()
                self.bankroll -= self.bet
                # print(hand, hand.getSum())
                return [hand]
            elif action == "split":
                hand2 = Hand([hand.takeCard()], self.bet)
                self.bankroll -= self.bet
                hand.addCard(self.takeCard())
                hand2.addCard(self.takeCard())
                # print("pair split into %s and %s" % (hand, hand2))
                # print("play first pair")
                a = self.playHand(hand, dealercards)
                # print("play second pair")
                b = self.playHand(hand2, dealercards)
                # print("a =",a,"b =",b)
                a.extend(b)
                return a
            elif action == "surrender":
                hand.setSurrender()
                return [hand]
            if hand.getSum() >= 21:
                return [hand]
        return [hand]


    def playround(self):
        self.bet = self.getBet()
        self.bankroll -= self.bet
        print("rc is %s, i'm betting %s" % (self.rc, self.bet))
        dealercards = []
        startcards = []
        print("your first and second card is:")
        startcards.append(self.takeCard())
        startcards.append(self.takeCard())
        playerhands = Hand(startcards, self.bet)
        print(playerhands)
        print("dealer card is:")
        dealercards.append(self.takeCard())
        print(dealercards)
        playedhands = self.playHand(playerhands, dealercards)
        print("playedhand:", playedhands)
        # print("rc: ", self.rc)

        while get_cards_sum(dealercards) < 17:  # Dealer keeps hitting until 17 or higher
            print("dealer takes another card:")
            dealercards.append(self.takeCard())
            print(dealercards)
        else:
            for hand in playedhands:
                if hand.isSurrendered():
                    self.bankroll += 0.5 * hand.getBet()
                elif hand.getSum() > 21:
                    pass
                elif hand == Hand([Card(1), Card(10)]) and get_cards_sum(dealercards) != 21:  # blackajack!
                    self.bankroll += (1 + 1.5) * hand.getBet()
                elif get_cards_sum(dealercards) > 21:
                    self.bankroll += (1 + 1) * hand.getBet()
                elif hand.getSum() == get_cards_sum(dealercards):
                    self.bankroll += hand.getBet()
                elif hand.getSum() > get_cards_sum(dealercards):
                    self.bankroll += (1 + 1) * hand.getBet()
                else:
                    pass
        #         for card in hand.getCards():  # put all cards back in deck
        #             self.deck.insert(0, card)
        # for card in dealercards:
        #     self.deck.insert(0, card)
        print("##############################################")


if __name__ == "__main__":
    print("Starting game...")
    bankrollresult = []
    for i in range(100):
        print(i)
        for k in range(100000):  # Play 10 000 000 shoes
            game = Game(100, 5, True)
            while len(game.deck) > 15:
                game.playround()
            bankrollresult.append(game.bankroll)
            # print(game.bankroll)
    sys.stdout = sys.__stdout__
    print("Game finished!")
    print("mean after 10 000 shoes played: %s" % mean(bankrollresult))
    print("stdev: %s" % sqrt(var(bankrollresult)))
    exit()
