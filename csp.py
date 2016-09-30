#System Files
import sys, math

#Local Files
import Classes as cs

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