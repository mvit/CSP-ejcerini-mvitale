#System Files
import sys, math

#Local Files
import Classes as cs

def checkFinalState(csp):                                         #Checks whether this is valid for the final state.
    for i in csp['items']:                                        #Since all of the data is in the items, let's loop through that.
        item = csp['items'][i];                                   #For shorthand purposes
        b = csp['bags'][csp['items'][i].currentBag]               #For shorthand purposes

        if b.name not in item.unary_inclusive:                    #Check if the object is in a bag it isn't technically allowed in
            return False

        if b.name in item.unary_exclusive:                        #Same as the last one.
            return False

        for e in item.equality:                                   #Check if all objects that should be in this bag are there.
            if e not in b.items:
                return False                                      #If not, return false

        for e in item.inequality:                                 #Check if any objects that SHOULDN'T be there are there
            if e in b.items:
                return False                                      #If they are, return false

        mutual_inclusivity_bag_copy = item.mutual_inclusive_bags            #Copy these arrays so we can manipulate them without data loss
        mutual_inclusivity_items_copy = item.mutual_inclusive_items

        while b.name in mutual_inclusivity_bag_copy:
            mutual_inclusivity_bag_copy.remove(b.name)                      #Remove all instances of the current bag from the list.

        for it in mutual_inclusivity_items_copy:                            #Loop through the mutually inclusive items.
            if it in b.items:                                               #If it's in the current bag, return false.
                return False
            else:
                if csp['items'][it].currentBag in mutual_inclusivity_bag_copy:          #If the bag is in the list, remove the first instance.
                    mutual_inclusivity_bag_copy.remove(csp['items'][it].currentBag)
                else:                                                                   #Otherwise, mutual inclusivity failed.
                    return False

    for b in csp['bags']:                                          #Loop through the bags to make sure they're all ok.
        if not csp['bags'][b].validBag():                          #Check them.
            return False

    return True

def readargs(csp, cursor, args):
    if args[0] == '#####':
        return cursor + 1

    if (cursor == 1):
        readvariables(csp, args)
    elif (cursor == 2):
        readvalues(csp, args)
    elif (cursor == 3):
        readlimits(csp, args)
    elif (cursor == 4):
        readunaryinc(csp, args)
    elif (cursor == 5):
        readunaryex(csp, args)
    elif (cursor == 6):
        readbinaryeq(csp, args)
    elif (cursor == 7):
        readbinarynoteq(csp, args)
    elif (cursor == 8):
        readmutual(csp, args)

    return cursor

def readbinaryeq(csp, args):
    for arg in args:
        for a in args:
            if a is not arg:
                csp['items'][arg].addEquality(a)

def readbinarynoteq(csp, args):
    for arg in args:
        for a in args:
            if a is not arg:
                csp['items'][arg].addInequality(a)

def readmutual(csp, args):
    for arg in args:
        for a in args:
            if a is not arg and arg.isupper():
                if a.isupper():
                    csp['items'][arg].addMutualIncItem(a)
                else:
                    csp['items'][arg].addMutualIncBag(a)


def readunaryex(csp, args):
    for arg in args[1:]:
        csp['items'][args[0]].addUnaryEx(arg)

def readunaryinc(csp, args):
    for arg in args[1:]:
        csp['items'][args[0]].addUnaryIn(arg)

def readlimits(csp, args):
    for b in csp['bags']:
        csp['bags'][b].setMinMax(int(args[0]), int(args[1]))

def readvariables(csp, args):
    csp['items'][args[0]] = cs.Item(args[0], int(args[1]))

def readvalues(csp, args):
    csp['bags'][args[0]] = cs.Bag(args[0], int(args[1]))

def main(argv):

    csp = {
        'bags': {},
        'items': {},
    }

    with open(argv[0], 'r') as file:

        cursor = 0

        for line in file:
            args = line.strip().split()
            cursor = readargs(csp, cursor, args)


    if csp['bags']['b'].addToBag(csp['items']['G']) is -1:
        print()
        print("G could not be added to b")

    if csp['bags']['b'].addToBag(csp['items']['E']) is -1:
        print()
        print("E could not be added to b")

    if csp['bags']['c'].addToBag(csp['items']['G']) is -1:
        print()
        print("G could not be added to c")

    if csp['bags']['a'].addToBag(csp['items']['C']) is -1:
        print()
        print("C could not be added to a")

    print()

    for b in csp['bags']:
        csp['bags'][b].printBag()
        print()

    for i in csp['items']:
        csp['items'][i].printItem()
        print()

if __name__ == "__main__":
    main(sys.argv[1:])