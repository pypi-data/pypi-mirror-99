class cards():        
  def __init__(self):
    self.sutes = ["♠", "♣", "♥", "♦"]
    self.kind = ["A", "2", "3", "4", "5", "6",
                 "7", "8", "9", "10", "J", "Q", "K"]
    self.cards = self.getcards()
          
  def getcards(self):
    listCards = []
    for i in self.sutes:
      for j in self.kind:
        listCards.append(j+i)
    return listCards

  def ccopy(self):
    return self.getcards()

  def __getitem__(self, item):
    return self.cards[item]

  def __repr__(self):
    return str(self.cards)

  def __str__(self):
    return str(self.cards)
