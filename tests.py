from game import *

bj0 = Hand([Card(1), Card(10)])
bj1 = Hand([Card(10), Card(1)])
tens = Hand([Card(10), Card(10)], 5)

assert bj0 == bj1
assert bj1 == bj0
assert bj0 != tens
assert tens != bj0
assert bj1 != tens
assert tens != bj1
assert bj1.getAmountOfAces() == 1
assert bj0.getAmountOfAces() == 1

twoa = Hand([Card(1), Card(5), Card(1)])
assert twoa.getAmountOfAces() == 2

assert bj0.getSum() == 21
assert bj1.getSum() == 21
assert tens.getSum() == 20

assert Card(10) == Card(11)
assert Card(11) == Card(12)
assert Card(12) == Card(13)
assert Card(1) != Card(10)

h1 = [Card(2), Card(3)]
assert get_cards_sum(h1) == 5
h2 = [Card(1), Card(1)]
assert get_cards_sum(h2) == 12
h3 = [Card(1), Card(9)]
assert get_cards_sum(h3) == 20
h0 = [Card(1), Card(1), Card(10)]
assert get_cards_sum(h0) == 12
h4 = [Card(1), Card(1), Card(1)]
assert get_cards_sum(h4) == 13
h5 = [Card(1), Card(1), Card(1), Card(1), Card(6)]
assert get_cards_sum(h5) == 20
h5 = [Card(1), Card(9), Card(9)]
assert get_cards_sum(h5) == 19

assert(Card(1) == Card(1))
assert(Card(1) != Card(6))
assert(Card(6) != Card(1))
exit()