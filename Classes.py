import math

class Bag:
    name = ""                          #The name of the bag
    max_capacity = 0                   #The weight limit of the bag
    current_weight = 0                 #The current weight of the bag
    items = []                         #The items that are in the bag
    minimum_items = 0                  #The minimum number of items in the bag
    maximum_items = 0                  #The maximum number of items in the bag

    def __init__(self, name, max_capacity):
        self.name = name
        self.max_capacity = max_capacity
        self.current_weight = 0
        self.items = []
        self.minimum_items = 0
        self.maximum_items = 0

    def addToBag(self, item):
        if item.weight + self.current_weight > self.max_capacity:
            return -1

        if len(self.items) + 1 > self.maximum_items:
            return -1

        if item.addValid(self):
            self.items.append(item)
            self.current_weight += item.weight
            item.setCurrentBag(self.name)
        else:
            return -1

        return 0

    def getPercentFull(self):
        return math.round(self.current_weight/self.max_capacity)

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

        print("Bag", self.name)
        print("Max Capacity", self.max_capacity)
        print("Current Weight", self.current_weight)
        print("Items", names)
        print("Max Items", self.maximum_items)
        print("Min Items", self.minimum_items)

    def validBag(self):
        if self.current_weight > self.max_capacity:
            return False

        if self.getPercentFull() < .9:
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
            if i.name in bag.items:
                return False

        if bag.name in self.mutual_inclusive_bags:
            for i in self.mutual_inclusive_items:
                if i.name in bag.items:
                    return False

        return True

    def setCurrentBag(self, bagName):
        self.currentBag = bagName

    def printItem(self):
        print("Item", self.name)
        print("Weight", self.weight)
        print("Inclusive Bags", self.unary_inclusive)
        print("Exclusive Bags", self.unary_exclusive)
        print("Equalities", self.equality)
        print("Inequalities", self.inequality)
        print("Mutually Inclusive Items", self.mutual_inclusive_items)
        print("Mutually Inclusive Bags", self.mutual_inclusive_bags)

