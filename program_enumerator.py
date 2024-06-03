import itertools

# opcodeList = bytearray([12, 11, 9, 8, 7, 5, 4, 3, 2, 1])
# operandList = bytearray(list(range(1, 256)))
# sum 2050^n, n=1 to 128 to scientific notation   # wolfram alpha code

opcodeList = [0xc, 0xb, 9, 8, 7, 5, 4, 3, 2, 1]
operandList = list(range(1, 256))
# operandList = list(range(0, 10))

oneSymbolList = list(itertools.product(opcodeList, operandList))
twoSymbolList = list(itertools.product(oneSymbolList, oneSymbolList))
# threesymbolList = list(itertools.product(twoSymbolList, oneSymbolList))
combinedSymbolList = oneSymbolList + twoSymbolList

# perms = [''.join(p) for p in itertools.permutations(oneSymbolList)]

# print(oneSymbolList)
print(len(oneSymbolList))
# print(len(oneSymbolList))
# print(twoSymbolList)
print(len(twoSymbolList))
# print(len(threesymbolList))
print(len(combinedSymbolList))

# perm = list(itertools.permutations(operandList))
# print(perm)
# print(twoSymbolList)