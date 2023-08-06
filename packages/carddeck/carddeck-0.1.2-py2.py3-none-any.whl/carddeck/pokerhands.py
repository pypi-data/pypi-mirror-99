from .cards import cards

class PokerHands():
  '''
  look for poker hands:
    01	Royak fluch
    02	Straight flush
    03	Four of a kind
    04	Full house
    05	Flush
    06	Straight
    07	Three of a kind
    08  Two pair
    09  One pair
    10	High card
  '''
  def __init__(self):
    self.cards = cards()

  def getHand(self, aHand):
    self.aHand = aHand
    self.theSutes, self.theKinds = self.getSutesAndKinds(aHand)
    self.orderedKinds = self.getOrderOfKinds(self.theKinds)
    i = 1
    while i <= 10:
      caseResult = getattr(self, 'case_' + str(i))()
      if caseResult:
        break
      i += 1
    return caseResult
  
  # Royal flush
  def case_1(self):
    rtnStr = ""
    theRoyals = self.cards[-4:].copy()
    theRoyals.insert(0,self.cards[-13])
    _, theRoyalsKinds = self.getSutesAndKinds(theRoyals)
    orderdRoyalsKinds = self.getOrderOfKinds(theRoyalsKinds)
    if (len(self.theSutes) == 1) & (self.orderedKinds == orderdRoyalsKinds):
      rtnStr = "Royal flush: " + list(self.theSutes.keys())[0]
    return rtnStr
  # Straight flush
  def case_2(self):
    rtnStr = ""
    if (len(self.theSutes) == 1):
      if self.isStraight(self.theKinds):
        rtnStr = "Straight flush: " + \
            str(self.cards.kind[self.orderedKinds[-1]]) + " high " + list(self.theSutes.keys())[0]
    return rtnStr
  # "Four of a kind"
  def case_3(self):
    rtnStr = ""
    if len(self.theKinds) == 2:
      myAny = []
      for i in self.theKinds:
        if self.theKinds[i] == 4:
          myAny.append(i)
      if myAny:
        rtnStr = "Four of a kind: " + myAny[0]    
    return rtnStr
  # "Full house"
  def case_4(self):
    rtnStr = ""
    if len(self.theKinds) == 2:
      myAny = []
      for i in self.theKinds:
        if self.theKinds[i] > 1:
          myAny.append(i)
      if any(myAny):
        rtnStr = "Full house: " + myAny[0] + " and " + myAny[1]
    return rtnStr
  # "Flush"
  def case_5(self):
    rtnStr = ""
    if (len(self.theSutes) == 1):
      rtnStr = "Flush: " + list(self.theSutes.keys())[0]
    return rtnStr
  # "Straight"
  def case_6(self):
    rtnStr = ""
    if (self.theKinds) == 5:
      #print(self.theKinds)
      if(self.isStraight(self.theKinds)):
        for i in self.theKinds:
          rtnStr = rtnStr + "," + i
      rtnStr = "Straight: " + rtnStr
    return rtnStr
  # "Three of a kind"
  def case_7(self):  
    rtnStr = ""
    if len(self.theKinds) == 3:
      myAny = []
      for i in self.theKinds:
        if self.theKinds[i] == 3:
          myAny.append(i)
      if any(myAny):
        rtnStr = "Three of a kind: " + myAny[0]
    return rtnStr
  # "Two pair"
  def case_8(self):   
    rtnStr = ""
    if len(self.theKinds) == 3:
      myAny = []
      for i in self.theKinds:
        if self.theKinds[i] == 2:
          myAny.append(i)
      if len(myAny) == 2:
        rtnStr = "Two pair: " + myAny[0] + " and " + myAny[1]
    return rtnStr
  def case_9(self):   # "One pair"
    rtnStr = ""
    if len(self.theKinds) == 4:
      myAny = []
      for i in self.theKinds:
        if self.theKinds[i] == 2:
          myAny.append(i)
      if myAny:
        rtnStr = "One pair of: " + myAny[0]
    return rtnStr
  def case_10(self):  # "High card"
    rtnStr = ""
    if len(self.theKinds) == 5:
      orderdKinds = self.getOrderOfKinds(self.theKinds)
      if orderdKinds[0] == 0:
        highCard = self.cards.kind[0]
      else:
        highCard = self.cards.kind[orderdKinds[4]]  
      rtnStr = "High card: " + highCard
    return rtnStr

  def getSutesAndKinds(self, aHand, verbose=False):
    handSutes = {}
    handKinds = {}
    if verbose:
      print(aHand)
    for card in aHand:
        aSute, aKind = card[-1], card[:-1]
        if aSute not in handSutes:
            handSutes[aSute] = 1
        else:
            handSutes[aSute] = handSutes[aSute] + 1
        if aKind not in handKinds:
            handKinds[aKind] = 1
        else:
            handKinds[aKind] = handKinds[aKind] + 1
    if verbose:
      print("handKinds:", handKinds)
    if verbose:
      print("handSutes:", handSutes)
    return handSutes, handKinds

  def getOrderOfKinds(self, aHandKinds, verbose=False):
    rtnList = []
    if verbose:
      print(aHandKinds)
    for key in aHandKinds:
      keyIndex = self.cards.kind.index(key)
      if rtnList:
        i = 0
        while i < len(rtnList):
          if keyIndex < rtnList[i]:
            for j in range(0, aHandKinds[key]):
              rtnList.insert(i, keyIndex)
            break
          i += 1
        if i == len(rtnList):
          rtnList.append(keyIndex)
      else:
        rtnList.append(keyIndex)
    if verbose:
      print(rtnList)
    return rtnList


  def isStraight(self, aHandKinds, verbose=False):
    # this may change is a hand is more then five cards
    rtnBln = (len(aHandKinds) == 5)
    if rtnBln:
      #if verbose: print("chenking cards")
      orderdKinds = self.getOrderOfKinds(aHandKinds)
      for i in range(0, len(orderdKinds)-1):
        if orderdKinds[i+1] != orderdKinds[i] + 1:
          rtnBln = False
          break
    if verbose:
      print("isStraight", orderdKinds)
    return rtnBln

  def __repr__(self):
      return 'Use to find poker hands with carddeck.deck'
  def __str__(self):
      return 'Use to find poker hands with carddeck.deck'
