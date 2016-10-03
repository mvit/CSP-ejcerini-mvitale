import math

class Bag:
    name = ""                          #The name of the bag
    max_capacity = 0                   #The weight limit of the bag
    current_weight = 0                 #The current weight of the bag
    items = []                         #The items that are in the bag
    minimum_items = 0                  #The minimum number of items in the bag
    maximum_items = 9999                  #The maximum number of items in the bag

    def __init__(self, name, max_capacity):
        self.name = name
        self.max_capacity = float(max_capacity)
        self.current_weight = 0.0
        self.items = []
        self.minimum_items = 0
        self.maximum_items = 9999

    def addToBag(self, item):

        if self.isConsistent(item):
            self.items.append(item)
            self.current_weight += item.weight
            item.setCurrentBag(self.name)
        else:
            return -1
        return 0

    def isConsistent(self, item):

        if item.weight + self.current_weight > self.max_capacity:
            return False

        if len(self.items) + 1 > self.maximum_items:
            return False

        if not item.addValid(self):
            return False

        return True

    def getPercentFull(self):
        return math.floor(self.current_weight/float(self.max_capacity) * 100)

    def setMinMax(self, min, max):
        self.minimum_items = min
        self.maximum_items = max

    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            self.current_weight -= item.weight
            item.setCurrentBag('0')

    def printBag(self):
        names = []
        for i in self.items:
            names.append(i.name)

        print("{} {}".format(self.name, names))
        print("Number of Items: {}".format(len(self.items)))
        print("Total Weight: {}/{}".format(self.current_weight, self.max_capacity))
        print("Wasted Capacity: {}".format(self.max_capacity - self.current_weight))


    def validBag(self):
        if self.current_weight > self.max_capacity:
            print('weight exceeded{} {}'.format(self.current_weight, self.max_capacity))
            return False

        if self.getPercentFull() < 90:
            print('percent not enough {}'.format(self.getPercentFull()))
            return False

        if len(self.items) > self.maximum_items or len(self.items) < self.minimum_items:
            return False

        return True

class Item:
    name = 'A'                         #The Name of the Item
    weight = 0                         #How much it weighs
    unary_inclusive = []               #The list of bags that the Item is ALLOWED in
    unary_exclusive = []               #The list of bags that the Item is NOT ALLOWED in
    equality = []                      #Items that this object MUST BE IN THE SAME BAG AS
    inequality = []                    #Items that this object MUST NOT BE IN THE SAME BAG AS
    mutual_inclusive_items = []        #The Items that this Item is in an Inclusivity Group with
    mutual_inclusive_bags = []         #The bags for this Item's Mutual Inclusivity
    currentBag = '0'                   #The name of the bag the item is currently in. Initialied to 0
    possibleBags = [];

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.unary_inclusive = []
        self.unary_exclusive = []
        self.equality = []
        self.inequality = []
        self.mutual_inclusive_items = []
        self.mutual_inclusive_bags = []
        self.currentBag = '0'
        self.possibleBags = []

    def addUnaryIn(self, bagName):
        self.unary_inclusive.append(bagName)

    def addUnaryEx(self, bagName):
        self.unary_exclusive.append(bagName)

    def addEquality(self, itemName):
        self.equality.append(itemName)

    def addInequality(self, itemName):
        self.inequality.append(itemName)

    def addMutualIncItem(self, itemName):
        self.mutual_inclusive_items.append(itemName)

    def addMutualIncBag(self, bagName):
        self.mutual_inclusive_bags.append(bagName)

    def addValid(self, bag):

        if self.currentBag is not '0':
            return False

        if bag.name in self.unary_exclusive :
            return False

        for i in self.inequality:
            for item in bag.items:
                if item.name == i:
                    return False

        if bag.name in self.mutual_inclusive_bags:
            for i in self.mutual_inclusive_items:
                for item in bag.items:
                    if item.name == i:
                        return False

        return True

    def setCurrentBag(self, bagName):
        self.currentBag = bagName

    def addPossibleBag(self, bag):
        if bag.isConsistent(self):
            self.possibleBags.append(bag.name)
            return 0

        return -1

    def updatePossibleBags(self, ctx):
        for b in self.possibleBags:
            if not ctx['bags'][b].isConsistent(self):
                self.possibleBags.remove(b)
        sortBags = []
        for s in self.possibleBags:
            sortBags.append(ctx['bags'][s])
        sortBags = sorted(sortBags, key=getPercentage)
        self.possibleBags = []
        for s in sortBags:
            self.possibleBags.append(s.name)

    def getPossibleBags(self, ctx):
        sortBags = []
        nameBags = []

        for s in self.possibleBags:
            sortBags.append(ctx['bags'][s])
        sortBags = sorted(sortBags, key=getPercentage)
        for s in sortBags:
            nameBags.append(s.name)
        return nameBags
    
    def printItem(self):
        print("Item", self.name)
        print("Weight", self.weight)
        print("Inclusive Bags", self.unary_inclusive)
        print("Exclusive Bags", self.unary_exclusive)
        print("Equalities", self.equality)
        print("Inequalities", self.inequality)
        print("Mutually Inclusive Items", self.mutual_inclusive_items)
        print("Mutually Inclusive Bags", self.mutual_inclusive_bags)


def getPercentage(bag):
    return float(bag.getPercentFull())
