import sys, math

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
    ctx['notequals'].append(args)

def readbinarynoteq(ctx, args):
    ctx['equals'].append(args)

def readmutual(ctx, args):
    ctx['mutuals'].append(args)

def readunaryex(ctx, args):
    ctx['exclusives'].append(args)

def readunaryinc(ctx, args):
    ctx['inclusives'].append((args))

def readlimits(ctx, args):
    ctx['min'] = args[0]
    ctx['max'] = args[1]

def readvariables(ctx, args):
    ctx['items'][args[0]] = int(args[1])

def readvalues(ctx, args):
    ctx['bags'][args[0]] = int(args[1])

def main(argv):

    ctx = {
        'bags': {},
        'items': {},
        'inclusives': [],
        'exclusives': [],
        'mutuals': [],
        'equals': [],
        'notequals': [],
        'min': 0,
        'max': 0,
    }

    with open(argv[0], 'r') as file:

        cursor = 0

        for line in file:
            args = line.strip().split()
            cursor = readargs(ctx, cursor, args)

    print(ctx)

if __name__ == "__main__":
    main(sys.argv[1:])