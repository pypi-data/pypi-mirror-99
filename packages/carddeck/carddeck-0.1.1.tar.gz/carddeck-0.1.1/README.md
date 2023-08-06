# Poker Hands from a Deck of Cards
 _An object model of cards is loaded into a deck, that is shuffled and dealt out as hands is packaged in the python module **carddeck**._
 
 Carddeck is composed of four python classes: 1) cards, 2) deck, 3) pokerhands, and 4) errors.  It is a concept used to exercise python setup, coding, documenting and packaging for pypi distribution. 
## Example
The defult of five cards in four hands are dealt after creating a deck, and shuffling it.

    from carddeck.deck import deck
    myD = deck()
    myD.shuffle()
    myD.deal()
    myD.printHands()
    --------
    Outout:
    ['Q♥', '8♥', 'A♥', '2♠', '7♣'] 
    ['4♣', 'K♣', 'J♦', 'J♠', '4♦'] 
    ['4♥', '7♦', '9♥', '2♦', '10♠'] 
    ['2♥', 'Q♣', 'A♦', 'J♣', '5♦'] 
The four hands are evaluated using the PokerHands object.

    from carddeck.pokerhands import PokerHands
    myPH = PokerHands()
    for i in range(0,len(myD.hands)):
        theCards = myD.hands[i]
        theHand = myPH.getHand(theCards)
        print(theCards, theHand)
    --------
    ['Q♥', '8♥', 'A♥', '2♠', '7♣'] High card: A
    ['4♣', 'K♣', 'J♦', 'J♠', '4♦'] Two pair: 4 and J
    ['4♥', '7♦', '9♥', '2♦', '10♠'] High card: 10
    ['2♥', 'Q♣', 'A♦', 'J♣', '5♦'] High card: A
The next deal from the remaining cards can then be evaluated.

    myD.deal()
    for i in range(0,len(myD.hands)):
        theCards = myD.hands[i]
        theHand = myPH.getHand(theCards)
        print(theCards, theHand)
    --------
    ['Q♥', '8♥', 'A♥', '2♠', '7♣'] High card: A
    ['4♣', 'K♣', 'J♦', 'J♠', '4♦'] Two pair: 4 and J
    ['4♥', '7♦', '9♥', '2♦', '10♠'] High card: 10
    ['2♥', 'Q♣', 'A♦', 'J♣', '5♦'] High card: A