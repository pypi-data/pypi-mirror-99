from .cards import cards
import random


class deck():
  def __init__(self):
    self.cards = cards()
    self.deck = self.cards.getcards()
    self.hands = dict()

  def shuffle(self, deck=None):
    # no hands are dealt when shuffleing
    self.hands.clear()
    if deck is None:
      deck = self.cards.getcards()
    # split the deck in two
    cardsindex = list(range(0, len(deck)))
    for i in range(0, 100):
      random.shuffle(cardsindex)
    suffleddeck = []
    for i in cardsindex:
      suffleddeck.append(deck[i])
    self.deck = suffleddeck.copy()

  def deal(self, cards=5, hands=4, verbose=False):
    if len(self.deck) < cards * hands:
      print('New Deck')
      self.deck = self.cards.getcards()
      self.shuffle()
    for j in range(0, hands):
      self.hands[j] = []
    for _ in range(0, cards):
      for j in range(0, hands):
        self.hands[j].append(self.deck.pop(0))

  def printHands(self):
    rtnStr = ""
    if len(self.hands) > 0:
      for i in range(0, len(self.hands)-1):
        rtnStr = rtnStr + str(self.hands[i]) + "\n"
      rtnStr = rtnStr + str(self.hands[i+1])
    else:
        rtnStr = "No hands have been dealt."
    print(rtnStr)

  def __iter__(self):
    ''' Returns the Iterator object '''
    return __DeckIterator__(self)

  def __repr__(self):
    return str(self.deck)
  def __str__(self):
    return str(self.deck)


class __DeckIterator__:
  ''' Iterator class '''
  def __init__(self, deck):
    # deck object reference
    self._deck = deck
    # member variable to keep track of current index
    self._index = 0

  def __next__(self):
    ''''Returns the next value from team object's lists '''
    if self._index < (len(self._deck.deck)):
      result = self._deck.deck[self._index]
      self._index += 1
      return result
    # End of Iteration
    raise StopIteration
