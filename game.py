from card import *
import random
from hand import *
# random.seed(123)
from math import sqrt
import numpy as np

deck = get_deck() * 8
random.shuffle(deck)
# donedeck = []
# deck = [Card(5), Card(11), Card(2), Card(3), Card(10), Card(4), Card(10), Card(1), Card(1), Card(10), Card(1)]
# print("deck: ", deck)
bet = 5


def getaction(hand, dealervalue):
    # if(len(hand.getCards()) == 2 and Card(1) not in hand.getCards() and (hand.getSum() == 16 and dealervalue in [9,
    # 10, 1] or hand.getSum() == 15 and dealervalue == 10)): return "surrender"
    if hand.getCards()[0] == hand.getCards()[1]:  # pair splitting
        cardvalue = hand.getCards()[0].bjValue()
        if cardvalue == 1 or cardvalue == 8:
            return "split"
        elif (cardvalue == 9 and dealervalue in [2, 3, 4, 5, 6, 8, 9]) or (cardvalue == 7 and 1 < dealervalue < 8) or (
                cardvalue == 6 and 2 < dealervalue < 7) or (2 <= cardvalue <= 3 and 4 <= dealervalue <= 7):
            return "split"
        elif (cardvalue == 6 and dealervalue == 2) or (1 < cardvalue < 4 and 1 < dealervalue < 4) or (
                cardvalue == 4 and 4 < dealervalue < 7):
            return "split"  # if DAS is offered, otherwise don't split
        else:
            pass
            # print("Don't split!")

    if Card(1) in hand.getCards() and len(hand.getCards()) == 2:  # soft totals
        othercard = [card for card in hand.getCards() if card.bjValue() != 1][0].bjValue()
        if (othercard >= 9) or (othercard == 8 and dealervalue != 6) or (othercard == 7 and 6 < dealervalue < 9):
            return "stand"
        if (1 < othercard < 7 and 4 < dealervalue < 7) or (3 < othercard < 7 and dealervalue == 4) or (
                othercard == 6 and dealervalue == 3):
            return "double"  # if allowed, otherwise hit
        if (othercard == 8 and dealervalue == 6) or (othercard == 7 and 1 < dealervalue < 7):
            return "double"  # if allowed, otherwise stand
        else:
            return "hit"

    if (hand.getSum() == 10 and 1 < dealervalue <= 9) or hand.getSum() == 11 or (
            hand.getSum() == 9 and 2 < dealervalue < 7):  # hard totals
        return "double"
    elif (hand.getSum() >= 13 and 1 < dealervalue < 7) or (hand.getSum() == 12 and 3 < dealervalue < 7) or (
            hand.getSum() >= 17):
        return "stand"
    else:
        return "hit"


def merge(a, b):
    c = a.copy()
    c.append(b[0])
    return c


def playhand(hand, dealercards):
    global bankroll
    stand = False
    while not stand and hand.getSum() <= 21:
        action = getaction(hand, dealercards[0].bjValue())
        if action == "hit":
            hand.addCard(deck.pop())
        elif action == "stand":
            return [hand]
        elif action == "double":
            hand.addCard(deck.pop())
            hand.setDouble()
            bankroll -= bet
            # print(hand, hand.getSum())
            return [hand]
        elif action == "split":
            hand2 = Hand([hand.takeCard()], bet)
            bankroll -= bet
            hand.addCard(deck.pop())
            hand2.addCard(deck.pop())
            # print("pair split into %s and %s" % (hand, hand2))
            # print("play first pair")
            a = playhand(hand, dealercards)
            # print("play second pair")
            b = playhand(hand2, dealercards)
            # print("a =",a,"b =",b)
            return merge(a, b)
        elif action == "surrender":
            hand.setSurrender()
            return [hand]
        if hand.getSum() >= 21:
            return [hand]


def playround():
    global bankroll
    bankroll -= bet
    dealercards = []
    playercards = []
    # print("your first and second card is:")
    playercards.append(deck.pop())
    playercards.append(deck.pop())
    starthand = Hand(playercards, bet)
    # print(starthand, starthand.getSum())
    # print("dealer card is:")
    dealercards.append(deck.pop())
    # print(dealercards, sum([card.bjValue() for card in dealercards]))
    playedhands = playhand(starthand, dealercards)
    # print("playedhand:", playedhands, playedhands[0].getSum())

    while get_cards_sum(dealercards) < 17:  # Dealer keeps hitting until 17 or higher
        # print("dealer takes another card:")
        dealercards.append(deck.pop())
        # print(dealercards, get_cards_sum(dealercards))
    else:
        for hand in playedhands:
            if hand.isSurrendered():
                bankroll += 0.5 * hand.getBet()
            elif hand.getSum() > 21:
                pass
            elif hand == Hand([Card(1), Card(10)]) and get_cards_sum(dealercards) != 21:  # blackajack!
                bankroll += (1 + 1.5) * hand.getBet()
            elif get_cards_sum(dealercards) > 21:
                bankroll += (1 + 1) * hand.getBet()
            elif hand.getSum() == get_cards_sum(dealercards):
                bankroll += hand.getBet()
            elif hand.getSum() > get_cards_sum(dealercards):  # hmmm
                bankroll += (1 + 1) * hand.getBet()
            else:
                pass
            for card in hand.getCards():  # put all cards back in deck
                deck.insert(0, card)
    for card in dealercards:
        deck.insert(0, card)
    # print("##############################################")


if __name__ == "__main__":
    # while 1:
    #     bankroll = 100
    #     playround()
    #     random.shuffle(deck)
    #     if bankroll > 100:
    #         print(bankroll)
    #         input()

    for j in range(3):
        print("starting 100 000 sets of 100 games...")
        bankrollist = []
        for i in range(10):
            print(i)
            for k in range(10000):
                bankroll = 100
                for p in range(100):
                    playround()
                bankrollist.append(bankroll)
                random.shuffle(deck)
        print("after 100000 sets of 100 games you ended op on avg with", np.mean(bankrollist), "euro")
        print("with stdev of", sqrt(np.var(bankrollist)))

    # result = []

    # bankroll = 100
    # for i in range(1000):
    #     playround()
    #     random.shuffle(deck)
    # # print(bankroll)
    # # result.append(bankroll)
    # # print("mean:",np.mean(result))
    # # print("stdev:",sqrt(np.var(result)))
    # print(bankroll)
