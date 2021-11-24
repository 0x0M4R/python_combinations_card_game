import random
from itertools import groupby
from operator import itemgetter


class Card:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        x = ['♦', '♥', '♠', '♣'][int(self.value / 13)]
        names = {0: 'A', 10: 'J', 11: 'Q', 12: 'K'}
        rank = (self.value + 1) % 13
        y = names[rank] if rank in names else rank + 1
        return '{} of {} - {}'.format(y, x, self.value)

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return str(self)

    def show(self):
        print(self)


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for v in range(0, 52):
            self.cards.append(Card(v))
            self.cards.append(Card(v))

    def show(self):
        for c in self.cards:
            c.show()
        print(len(self.cards))

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i],  self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.dropped = []
        self.rank = []
        self.suit = []
        self.scores = []
        self.points = 0
        self.k = 0

    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def showHand(self):
        for card in self.hand:
            card.show()

    def sortHand(self):
        self.hand.sort(reverse=True, key=lambda self: self.value % 13)

    def samerank(self):
        # Create list of same rank different suit cards
        self.rank=[]
        for i in range(14):
            self.rank.append([])
        hand1 = [c.value for c in self.hand]
        hand2 = list(hand1)
        for i in hand2:
            self.rank[i % 13].append(i)

    def samesuit(self):
        # Create list of same suit consecutive cards
        self.suit=[]
        hand1 = [c.value for c in self.hand]
        hand2 = list(hand1)
        hand3 = sorted(set(hand2))
        for k, g in groupby(enumerate(hand3), lambda ix: ix[0] - ix[1]):
            o = list(map(itemgetter(1), g))
            if o[0] <= 12 and o[-1] > 12:
                b = o.index(12)
                if b == 0:
                    self.suit.append(o[0])
                    self.suit.append(o[1:-1])
                    break
                else:
                    self.suit.append(o[0:b])
                    self.suit.append(o[b:-1])
                    break
            elif o[0] <= 25 and o[-1] > 25:
                c = o.index(25) + 1
                if c == 0:
                    self.suit.append(o[0])
                    self.suit.append(o[1:-1])
                    break
                else:
                    self.suit.append(o[0:c])
                    self.suit.append(o[c:-1])
            elif o[0] <= 38 and o[-1] > 38:
                a = o.index(38) + 1
                if a == 0:
                    self.suit.append(o[0])
                    self.suit.append(o[1:-1])
                    break
                else:
                    self.suit.append(o[0:a])
                    self.suit.append(o[a:-1])
            else:
                self.suit.append(o)

        print(self.rank)
        print(self.suit)

    def comboscores(self):
        # Create list of all valid combination of scores
        self.scores=[]
        for i in range(len(self.rank)):
            if len(set(self.rank[i])) > 2:
                self.scores.append(self.rank[i])
        for i in range(len(self.suit)):
            if len(self.suit[i]) > 2:
                self.scores.append(self.suit[i])
        print(self.scores)

    def countScore(self):
        # Convert to rank
        self.points=0
        self.samerank()
        self.samesuit()
        self.comboscores()
        self.removeduplicate()
        score = []
        scoree = []
        for i in range(len(self.scores)):
            points = [(int(x) +2) % 13 for x in self.scores[i]]
            score.append(points)
        # Calculate score for each combo
        for i in range(len(score)):
            for j in range(len(score[i])):
                #K,A,Q,J
                if score[i][j] == 0 or score[i][j] == 1 or score[i][j] == 12 or score[i][j] == 11:
                    score[i][j] = 10
        for i in range(len(score)):
            scoree.append(sum(score[i]))

        print(score)
        print(scoree)
        print(sum(scoree))
        self.points = sum(scoree)
        return

# change to remove the lesser score sublist
    def removeduplicate(self):
        # if you have for ex. [[33, 46, 7], [7, 8, 9, 10]] the 7 should be removed from 2nd and treated as two sets.
        seen = set()
        for sublist in self.scores:
            for item in sublist:
                if item in seen:
                    print('Duplicate')
                    self.scores.remove(sublist)
                    break
                seen.add(item)
            else:
                continue
            break
        else:
            print('No duplicate')
    def dropcards(self):
        # Put down cards if more than 51 score
        #FIXX
        for i in range(len(self.scores)):
            self.dropped.append([])
        for i in self.scores:
            for j in i:
                self.dropped[k].append(self.hand.pop(self.getindex(j)))
            self.k+=1
        print(k)
    def getindex(self, value):
        for i, e in enumerate(self.hand):
            if e.value == value:
                return i
        return -1

    def nextturn(self):
        #ask which card to remove
        print(self.hand)
        print(self.dropped)
        discard = input("which card would you like to discard:")
        for i, e in enumerate(self.hand):
            if e.value == int(discard):
                del self.hand[i]
                return
    # Fix rank and suit and removedup to avoid set of 4 with three unique cards to be ignored.
    # Add another function which adds cards to dropped set if it belongs there
    #after cards dropped score should not reset.
    #game should end when no more cards in deck before last last card is dealt
    #should actually end when no more cards in players hand

# RULES 3+ consecutive same suit gets counted, 3+ same rank different suit gets counted, joker can be anything

deck = Deck()
deck.shuffle()
bob = Player("Bob")
for _ in range(15):
    bob.draw(deck)
while len(bob.hand) != 0:
    print(len(bob.hand))
    bob.sortHand()
    bob.showHand()
    bob.countScore()
    if bob.points > 50: #or if already dropped
    #first ask if want to drop combinations
        bob.dropcards()
    bob.nextturn()
    bob.draw(deck)
print("Congrats you have finished!")