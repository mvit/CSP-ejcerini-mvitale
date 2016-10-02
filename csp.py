#System Files
import sys, math

#Local Files
import Classes as cs

def checkFinalState(ctx):                                         #Checks whether this is valid for the final state.
    for i in ctx['items']:                                        #Since all of the data is in the items, let's loop through that.
        item = ctx['items'][i];                                   #For shorthand purposes
        b = ctx['bags'][ctx['items'][i].currentBag]               #For shorthand purposes

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
                if ctx['items'][it].currentBag in mutual_inclusivity_bag_copy:          #If the bag is in the list, remove the first instance.
                    mutual_inclusivity_bag_copy.remove(ctx['items'][it].currentBag)
                else:                                                                   #Otherwise, mutual inclusivity failed.
                    return False

    for b in ctx['bags']:                                          #Loop through the bags to make sure they're all ok.
        if not ctx['bags'][b].validBag():                          #Check them.
            return False

    return True



def readargs(ctx, cursor, args):
    if args[0] == '#####':
        return cursor + 1

    if (cursor == 1):
        readvariables(ctx, args)
    elif (cursor == 2):
        readvalues(ctx, args)
    elif (cursor == 3):
        readlimits(ctx, args)
    elif (cursor == 4):
        readunaryinc(ctx, args)
    elif (cursor == 5):
        readunaryex(ctx, args)
    elif (cursor == 6):
        readbinaryeq(ctx, args)
    elif (cursor == 7):
        readbinarynoteq(ctx, args)
    elif (cursor == 8):
        readmutual(ctx, args)

    return cursor

def readbinaryeq(ctx, args):
    for arg in args:
        for a in args:
            if a is not arg:
                ctx['items'][arg].addEquality(a)

def readbinarynoteq(ctx, args):
    for arg in args:
        for a in args:
            if a is not arg:
                ctx['items'][arg].addInequality(a)

def readmutual(ctx, args):
    for arg in args:
        for a in args:
            if a is not arg and arg.isupper():
                if a.isupper():
                    ctx['items'][arg].addMutualIncItem(a)
                else:
                    ctx['items'][arg].addMutualIncBag(a)


def readunaryex(ctx, args):
    for arg in args[1:]:
        ctx['items'][args[0]].addUnaryEx(arg)

def readunaryinc(ctx, args):
    for arg in args[1:]:
        ctx['items'][args[0]].addUnaryIn(arg)

def readlimits(ctx, args):
    for b in ctx['bags']:
        ctx['bags'][b].setMinMax(int(args[0]), int(args[1]))

def readvariables(ctx, args):
    ctx['items'][args[0]] = cs.Item(args[0], int(args[1]))

def readvalues(ctx, args):
    ctx['bags'][args[0]] = cs.Bag(args[0], int(args[1]))

def main(argv):

    ctx = {
        'bags': {},
        'items': {},
    }

    with open(argv[0], 'r') as file:

        cursor = 0

        for line in file:
            args = line.strip().split()
            cursor = readargs(ctx, cursor, args)


    if ctx['bags']['b'].addToBag(ctx['items']['G']) is -1:
        print()
        print("G could not be added to b")

    if ctx['bags']['b'].addToBag(ctx['items']['E']) is -1:
        print()
        print("E could not be added to b")

    if ctx['bags']['c'].addToBag(ctx['items']['G']) is -1:
        print()
        print("G could not be added to c")

    if ctx['bags']['a'].addToBag(ctx['items']['C']) is -1:
        print()
        print("C could not be added to a")

    print()

    for b in ctx['bags']:
        ctx['bags'][b].printBag()
        print()

    for i in ctx['items']:
        ctx['items'][i].printItem()
        print()

if __name__ == "__main__":
    main(sys.argv[1:])